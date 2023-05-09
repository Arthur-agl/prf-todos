from api.models import Todo, TodoItem, User
from api.schemas import TodoListItemSchema, TodoListSchema, UserSchema
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from flask_restful import Api, Resource
from marshmallow import ValidationError
from prftodosapi.extensions import db
from werkzeug.security import check_password_hash

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint)


class TodoItemResource(Resource):
    @login_required
    def get(self, todo_id):
        curr_user_id = int(current_user.get_id())
        curr_user_todos = db.session.scalars(
            db.select(Todo.id).filter_by(user_id=curr_user_id)).all()

        if not (todo_id in curr_user_todos):
            return "Todo not found", 404

        todo_items = db.session.scalars(
            db.select(TodoItem).filter_by(todo_id=todo_id)).all()

        return TodoListItemSchema().dump(todo_items, many=True)

    @login_required
    def post(self, todo_id):
        curr_user_id = int(current_user.get_id())
        curr_user_todos = db.session.scalars(
            db.select(Todo.id).filter_by(user_id=curr_user_id)).all()

        if not (todo_id in curr_user_todos):
            return "Todo not found", 404

        try:
            data = TodoListItemSchema().load(request.json)
            todo_item = TodoItem(**data)
            db.session.add(todo_item)
            db.session.commit()
        except ValidationError as err:
            return err.messages, 400
        return None

    @login_required
    def patch(self, todo_id, item_id):
        curr_user_id = int(current_user.get_id())
        curr_user_todos = db.session.scalars(
            db.select(Todo.id).filter_by(user_id=curr_user_id)).all()

        if not (todo_id in curr_user_todos):
            return "Todo not found", 404

        schema = TodoListItemSchema(partial=True, exclude=['todo_id'])
        todo_item: TodoItem = TodoItem.query.get_or_404(item_id)

        if not (todo_item.todo_id in curr_user_todos):
            return "Item not found", 404

        data = schema.load(request.json)
        for key, value in data.items():
            if hasattr(todo_item, key):
                setattr(todo_item, key, value)
        db.session.commit()
        return None

    @login_required
    def delete(self, todo_id, item_id):
        curr_user_id = int(current_user.get_id())
        curr_user_todos = db.session.scalars(
            db.select(Todo.id).filter_by(user_id=curr_user_id)).all()

        if not (todo_id in curr_user_todos):
            return "Todo not found", 404

        item = TodoItem.query.get_or_404(item_id)

        if not (item.todo_id in curr_user_todos):
            return "Item not found", 404

        db.session.delete(item)
        db.session.commit()
        return None


class TodoResource(Resource):
    @login_required
    def get(self, user_id):
        todos = db.session.scalars(
            db.select(Todo).filter_by(user_id=user_id)).unique().all()
        return TodoListSchema(many=True).dump(todos)

    @login_required
    def post(self):
        try:
            data = TodoListSchema().load(data=request.json)
            todo = Todo(**data)
            db.session.add(todo)
            db.session.commit()
        except ValidationError as err:
            return err.messages, 400
        return None

    @login_required
    def patch(self, todo_id):
        curr_user_id = int(current_user.get_id())
        curr_user_todos = db.session.scalars(
            db.select(Todo.id).filter_by(user_id=curr_user_id)).all()

        if not (todo_id in curr_user_todos):
            return "Todo not found", 404

        schema = TodoListSchema(partial=True)
        todo = Todo.query.get_or_404(todo_id)
        data = schema.load(data=request.json)
        for key, value in data.items():
            if hasattr(todo, key):
                setattr(todo, key, value)
        db.session.commit()
        return None

    @login_required
    def delete(self, todo_id):
        curr_user_id = int(current_user.get_id())
        curr_user_todos = db.session.scalars(
            db.select(Todo.id).filter_by(user_id=curr_user_id)).all()

        if not (todo_id in curr_user_todos):
            return "Todo not found", 404

        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return None


class UserResource(Resource):
    @login_required
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return jsonify(user)

    def post(self):
        try:
            data = UserSchema().load(data=request.json)
            user = User(**data)
            db.session.add(user)
            db.session.commit()

        except ValidationError as err:
            return err.messages
        return None

    @login_required
    def patch(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        data = schema.load(data=request.json)
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return None

    @login_required
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()


class AuthLoginResource(Resource):
    def post(self):
        data = UserSchema().load(request.json)
        user = db.session.execute(
            db.select(User).filter_by(username=data["username"])).scalar_one()
        if not user or not check_password_hash(user.password_hash, data["password"]):
            return 'Login fail', 404
        login_user(user)
        return "Login success", 200


class AuthLogoutResource(Resource):
    def post(self):
        logout_user()
        return "logout success", 200


api.add_resource(TodoItemResource, "/todos/<int:todo_id>/items",
                 "/todos/<int:todo_id>/items/<int:item_id>")
api.add_resource(TodoResource, "/users/<int:user_id>/todos",
                 "/todos", "/todos/<int:todo_id>")
api.add_resource(UserResource, "/users", "/users/<int:user_id>")

api.add_resource(AuthLoginResource, "/login")
api.add_resource(AuthLogoutResource, "/logout")

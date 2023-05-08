from api.models import Todo, TodoItem, User
from api.schemas import TodoListItemSchema, TodoListSchema, UserSchema
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from prftodosapi.extensions import db

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint)


class TodoItemResource(Resource):
    # @checkPermission()
    def get(self, todo_id):
        todo_items = db.session.scalars(
            db.select(TodoItem).filter_by(todo_id=todo_id)).all()
        return TodoListItemSchema().dump(todo_items, many=True)

    def post(self, todo_id):
        try:
            data = TodoListItemSchema().load(request.json)
            todo_item = TodoItem(**data)
            db.session.add(todo_item)
            db.session.commit()
        except ValidationError as err:
            return err.messages, 400
        return None

    def patch(self, todo_id, item_id):
        schema = TodoListItemSchema(partial=True, exclude=['todo_id'])
        todo_item = TodoItem.query.get_or_404(item_id)
        data = schema.load(request.json)
        for key, value in data.items():
            if hasattr(todo_item, key):
                setattr(todo_item, key, value)
        db.session.commit()
        return None

    def delete(self, todo_id, item_id):
        item = TodoItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return None


class TodoResource(Resource):

    def get(self, user_id):
        todos = db.session.scalars(
            db.select(Todo).filter_by(user_id=user_id)).unique().all()
        return TodoListSchema(many=True).dump(todos)

    def post(self):
        try:
            data = TodoListSchema().load(data=request.json)
            todo = Todo(**data)
            db.session.add(todo)
            db.session.commit()
        except ValidationError as err:
            return err.messages, 400
        return None

    def patch(self, todo_id):
        schema = TodoListSchema(partial=True)
        todo = Todo.query.get_or_404(todo_id)
        data = schema.load(data=request.json)
        for key, value in data.items():
            if hasattr(todo, key):
                setattr(todo, key, value)
        db.session.commit()
        return None

    def delete(self, todo_id):
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return None


class UserResource(Resource):

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

    def patch(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        data = schema.load(data=request.json)
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return None

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()


api.add_resource(TodoItemResource, "/todos/<int:todo_id>/items",
                 "/todos/<int:todo_id>/items/<int:item_id>")
api.add_resource(TodoResource, "/users/<int:user_id>/todos",
                 "/todos", "/todos/<int:todo_id>")
api.add_resource(UserResource, "/users", "/users/<int:user_id>")

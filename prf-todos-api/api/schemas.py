from marshmallow import Schema, fields, post_load
from api.models import Todo, TodoItem


class TodoListItemSchema(Schema):
    id = fields.Integer()
    todo_id = fields.Integer(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    due = fields.Date()
    completed = fields.Bool(required=True)


class TodoListSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer(required=True)
    title = fields.Str(requied=True)
    items = fields.List(fields.Nested(TodoListItemSchema()))


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.Str(required=True)
    todo_lists = fields.List(fields.Nested(TodoListSchema()))

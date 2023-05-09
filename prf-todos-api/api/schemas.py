from marshmallow import Schema, fields


class TodoItemSchema(Schema):
    id = fields.Integer()
    title = fields.Str(required=True)
    description = fields.Str()
    due = fields.Date()
    completed = fields.Bool(required=True)


class TodoSchema(Schema):
    id = fields.Integer()
    title = fields.Str(requied=True)
    items = fields.List(fields.Nested(TodoItemSchema()))


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    todo_lists = fields.List(fields.Nested(TodoSchema()))

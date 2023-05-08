from dataclasses import dataclass
from prftodosapi.extensions import db


@dataclass
class Todo(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title: str = db.Column(db.String(100), nullable=False)
    items = db.relationship(
        'TodoItem', lazy='joined', cascade="all, delete")


@dataclass
class TodoItem(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    todo_id = db.Column(db.Integer, db.ForeignKey(
        'todo.id'), nullable=False)
    title: str = db.Column(db.String, nullable=False)
    description: str = db.Column(db.String)
    due = db.Column(db.DateTime)
    completed: bool = db.Column(db.Boolean, nullable=False, default=False)


@dataclass
class User(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String, nullable=False)
    todos = db.relationship('Todo', cascade="all, delete")

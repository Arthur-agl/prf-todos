from api.schemas import UserSchema
from flask import Blueprint, request

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.route("/login")
def login():
    data = UserSchema().load(request.json)
    return data

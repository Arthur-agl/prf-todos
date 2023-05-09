from flask import Flask

# Blueprints
import api
import auth

# Extensions
from prftodosapi.extensions import db, login_manager


def create_app(config_object="prftodosapi.settings"):
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(api.resources.blueprint)
    app.register_blueprint(auth.views.blueprint)
    return None


def register_errorhandlers(app):
    def validation_error(error):
        return "Invalidation"

    app.register_error_handler(400, validation_error)
    return None

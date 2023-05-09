from prftodosapi.extensions import db, login_manager
from api.models import User
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    print("user_id: " + user_id)
    user = db.session.execute(
        db.select(User).filter_by(id=user_id)).scalar_one()
    return user or None


def check_pw_hash(hash, password):
    return check_password_hash(hash, password)


def hash_pw(password):
    return generate_password_hash(password, method='md5')

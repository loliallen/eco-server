from flask_login import LoginManager

from src.models import UserModel


login_manager = LoginManager()

@login_manager.user_loader
def user_load(user_id):
    user = UserModel.find_user_by_id(user_id)
    return user
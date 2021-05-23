from flask_login import LoginManager

from src.models.user.UserModel import User


login_manager = LoginManager()

@login_manager.user_loader
def user_load(user_id):
    user = User.find_by_id_(user_id)
    return user
from flask import Flask
from flask_restful import Api

from config import Configuration
from src.controllers.FilterController import FilterController
from src.controllers.RecPointController import RecPointController
from src.controllers.MarkerController import MarkerController, MarkerControllerList, MarkerControllerListAll
from src.controllers.UserController import UserController, TokenAuthentication, UserConfirmController, UserLogoutController
from send_email import mail
import src.services.Database as Database
import login as login

Database.global_connect()


app = Flask(__name__)
app.config.from_object(Configuration)
api = Api(app)
mail.init_app(app)
login.login_manager.init_app(app)


api.add_resource(FilterController, '/api/filters')
api.add_resource(RecPointController, '/api/rec_points')
api.add_resource(MarkerController, '/api/markers')
api.add_resource(MarkerControllerList, '/api/markers/list')
api.add_resource(MarkerControllerListAll, '/api/markers/list/all')
api.add_resource(UserController, '/api/users')
api.add_resource(TokenAuthentication, '/api/login')
api.add_resource(UserLogoutController, '/api/logout')
api.add_resource(UserConfirmController, '/api/confirm/<string:token>')




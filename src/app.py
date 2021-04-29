from flask import Flask
from flask_restful_swagger_3 import Api
from flask_swagger_ui import get_swaggerui_blueprint

from src.config import Configuration
from src.controllers.filter.user import FilterController, FilterControllerList
# from src.controllers.RecPointController import RecPointController
# from src.controllers.MarkerController import MarkerController, MarkerControllerList, MarkerControllerListAll
# from src.controllers.UserController import UserController, TokenAuthentication, UserConfirmController, UserLogoutController, UserForgetPwdController
# from src.controllers.PartnerController import PartnerController
# from src.controllers.InvitationController import InvitationController
# from src.controllers.RecPointOfferController import RecPointOfferController
# from src.controllers.RecycleController import RecycleController
# from src.controllers.StatisticController import StatisticController, ModlesStaticController
# from src.controllers.ConfirmUser import ConfirmUserController
# from src.controllers.QuestionController import QuestionList
from src.send_email import mail
from src.middleware.collect_statistics import Collector
import src.services.Database as Database
import src.login as login

Database.global_connect()

app = Flask(__name__, static_url_path="/statics", static_folder='statics')
app.config.from_object(Configuration)
app.wsgi_app = Collector(app.wsgi_app)
api = Api(app)

mail.init_app(app)
login.login_manager.init_app(app)

# print(current_app

api.add_resource(FilterController, '/api/filters/<filter_id>')
api.add_resource(FilterControllerList, '/api/filters')

# api.add_resource(RecPointController, '/api/rec_points')
# api.add_resource(RecPointOfferController, '/api/recoff')
# api.add_resource(MarkerController, '/api/markers')
# api.add_resource(PartnerController, '/api/partners')
# api.add_resource(MarkerControllerList, '/api/markers/list')
# api.add_resource(MarkerControllerListAll, '/api/markers/list/all')
# api.add_resource(UserController, '/api/users')
# api.add_resource(TokenAuthentication, '/api/login')
# api.add_resource(UserLogoutController, '/api/logout')
# api.add_resource(UserForgetPwdController, '/api/forget')
# api.add_resource(ConfirmUserController, '/api/enable/coins')
# api.add_resource(UserConfirmController, '/api/confirm')
# api.add_resource(QuestionList, '/api/questions')
# api.add_resource(InvitationController, '/api/invitation')
# api.add_resource(RecycleController, '/api/recycle')
# api.add_resource(StatisticController, '/api/admin/stats')
# api.add_resource(ModlesStaticController, '/api/admin/stats/models')


SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://127.0.0.1:5000/api/doc/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)

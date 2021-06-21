from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful_swagger_3 import Api
from flask_swagger_ui import get_swaggerui_blueprint

import src.services.Database as Database
from src.config import Configuration
from src.controllers.filter.user import FilterController, FilterControllerList
from src.controllers.news.news_user import NewsListController, NewsController
from src.controllers.product.product_user import ProductController, ProductListController
from src.controllers.product.buy_product_user import BuyProductController
from src.controllers.recpoint.rec_point_user import RecPointController, RecPointListController
from src.controllers.recycle.recycle_transaction_user import RecycleTransactionListController, \
    RecycleTransactionController
from src.controllers.test.user.answere_user_controller import UserAnswerController
from src.controllers.test.user.attempts_user_controller import UserAttemptsListController, UserAttemptsController
from src.controllers.test.user.question_user_controller import QuestionListController, QuestionController
from src.controllers.test.user.test_user_controller import TestListController, TestController
from src.controllers.transaction.transaction_user import AdmissionTransactionListController, \
    AdmissionTransactionTransactionController
from src.controllers.user.confirm import ConfirmController
from src.controllers.user.login import LoginController
from src.controllers.user.recovery_password.chage_password import ChangePasswordController
from src.controllers.user.recovery_password.get_recovery_token import RecoveryTokenController
from src.controllers.user.recovery_password.send_check_code import RecoverySendCheckCodeController
from src.controllers.user.register import RegisterController
from src.controllers.user.user_info import UserInfoController
from src.middleware.collect_statistics import Collector
from src.send_email import mail

app = Flask(__name__, static_url_path="/statics", static_folder='statics')
app.config.from_object(Configuration)
app.wsgi_app = Collector(app.wsgi_app)
jwt = JWTManager(app)
Database.global_connect()
api = Api(app, title="EcoApi for User",
          authorizations={"JWT": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}})
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
mail.init_app(app)

# User
api.add_resource(RegisterController, '/api/register')
api.add_resource(ConfirmController, '/api/confirm')
api.add_resource(LoginController, '/api/login')
api.add_resource(UserInfoController, '/api/user_info')
api.add_resource(RecoverySendCheckCodeController, '/api/send_check_code')
api.add_resource(RecoveryTokenController, '/api/get_recovery_token')
api.add_resource(ChangePasswordController, '/api/change_password')

# Filters and Rec Points
api.add_resource(FilterControllerList, '/api/filters')
api.add_resource(FilterController, '/api/filters/<filter_id>')
api.add_resource(RecPointListController, '/api/rec_points')
api.add_resource(RecPointController, '/api/rec_points/<rec_point_id>')

# Recycle
api.add_resource(RecycleTransactionListController, '/api/recycle')
api.add_resource(RecycleTransactionController, '/api/recycle/<recycle_id>')

# Transactions
api.add_resource(AdmissionTransactionListController, '/api/transactions')
api.add_resource(AdmissionTransactionTransactionController, '/api/transactions/<transaction_id>')

# Products
api.add_resource(ProductListController, '/api/products')
api.add_resource(ProductController, '/api/products/<product_id>')
api.add_resource(BuyProductController, '/api/buy_product')

# Tests
api.add_resource(TestListController, '/api/tests')
api.add_resource(TestController, '/api/tests/<tests_id>')
api.add_resource(UserAttemptsListController, '/api/tests/<test_id>/attempts')
api.add_resource(UserAttemptsController, '/api/tests/<test_id>/attempts/<attempt_id>')
api.add_resource(UserAnswerController, '/api/tests/<test_id>/attempts/<attempt_id>/answer')
# Временные роуты, удалить после перехода фронта на новую версию
api.add_resource(QuestionListController, '/api/tests/<test_id>/questions')
api.add_resource(QuestionController, '/api/tests/<test_id>/questions/<question_id>')

# News
api.add_resource(NewsListController, '/api/news')
api.add_resource(NewsController, '/api/news/<news_id>')

# swagger
swagger_ui_blueprint = get_swaggerui_blueprint(
    Configuration.USER_SWAGGER_URL,
    Configuration.USER_SCHEMA_URL,
    config={
        'app_name': 'Eco Api',
    }
)
app.register_blueprint(swagger_ui_blueprint)

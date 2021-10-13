from flask import Flask, request
from flask_babel import Babel
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

import src.services.Database as Database
from controllers.partner.user import PartnerListController
from src.config import Configuration
from src.controllers.filter.filter_user import FilterController, FilterControllerList
from src.controllers.lookups.user.lookup_controller import LookupsControllerList
from src.controllers.news.news_img_upload import NewsUserImageUploaderController
from src.controllers.news.news_user import NewsListController, NewsController
from src.controllers.product.product_user import ProductController, ProductListController
from src.controllers.product.buy_product_user import BuyProductController
from src.controllers.recpoint.user.comment_img_update import RecPointCommentImageUploaderController
from src.controllers.recpoint.user.comment_user import RecPointCommentController
from src.controllers.recpoint.user.rec_point_user_img_update import RecPointImageUploaderController
from src.controllers.recpoint.user.rec_point_user import RecPointController, RecPointListController
from src.controllers.recycle.recycle_transaction_user import RecycleTransactionListController, \
    RecycleTransactionController
from src.controllers.recycle.recycle_transaction_user_img_update import RecycleImageUploaderController
from src.controllers.statistics.user.get_recycle_stat import RecycleStatisticController
from src.controllers.test.user.answere_user_controller import UserAnswerController
from src.controllers.test.user.attempts_user_controller import UserAttemptsListController, UserAttemptsController
from src.controllers.transaction.transaction_user import AdmissionTransactionListController, \
    AdmissionTransactionTransactionController
from src.controllers.user.confirm import ConfirmController
from src.controllers.user.login import LoginController
from src.controllers.user.recovery_password.chage_password import ChangePasswordController
from src.controllers.user.recovery_password.get_recovery_token import RecoveryTokenController
from src.controllers.user.recovery_password.send_check_code import RecoverySendCheckCodeController
from src.controllers.user.register import RegisterController
from src.controllers.user.upload_profile_image import UserImageUploaderController
from src.controllers.user.user_info import UserInfoController
from src.send_email import mail
from src.utils.custom_swagger import CustomApi


app = Flask(__name__,
            static_url_path=Configuration.STATIC_URL_PATH,
            static_folder=Configuration.STATIC_FOLDER)
app.config.from_object(Configuration)
jwt = JWTManager(app)
babel = Babel(app, configure_jinja=False)
Database.global_connect(app.logger)
api = CustomApi(app, title="EcoApi for User",
                authorizations={"JWT": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}})
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
mail.init_app(app)

# User
api.add_resource(RegisterController, '/api/register')
api.add_resource(ConfirmController, '/api/confirm')
api.add_resource(LoginController, '/api/login')
api.add_resource(UserInfoController, '/api/user_info')
api.add_resource(UserImageUploaderController, '/api/update_profile_image')
api.add_resource(RecoverySendCheckCodeController, '/api/send_check_code')
api.add_resource(RecoveryTokenController, '/api/get_recovery_token')
api.add_resource(ChangePasswordController, '/api/change_password')

# Filters and Rec Points
api.add_resource(FilterControllerList, '/api/filters')
api.add_resource(FilterController, '/api/filters/<filter_id>')

api.add_resource(RecPointListController, '/api/rec_points')
api.add_resource(RecPointController, '/api/rec_points/<rec_point_id>')
api.add_resource(RecPointImageUploaderController, '/api/rec_points/<rec_point_id>/images')
api.add_resource(RecPointCommentController, '/api/rec_comment')
api.add_resource(RecPointCommentImageUploaderController, '/api/rec_comment/<comment_id>/images')

# api.add_resource(RecPointOfferController, '/api/rec_offer')
# api.add_resource(RecPointOfferUpdateController, '/api/rec_offer/<rec_point_id>')


# Recycle
api.add_resource(RecycleTransactionListController, '/api/recycle')
api.add_resource(RecycleTransactionController, '/api/recycle/<recycle_id>')
api.add_resource(RecycleImageUploaderController, '/api/recycle/<recycle_id>/images')

# Transactions
api.add_resource(AdmissionTransactionListController, '/api/transactions')
api.add_resource(AdmissionTransactionTransactionController, '/api/transactions/<transaction_id>')

# Partner
api.add_resource(PartnerListController, '/api/partners')

# Products
api.add_resource(ProductListController, '/api/products')
api.add_resource(ProductController, '/api/products/<product_id>')
api.add_resource(BuyProductController, '/api/buy_product')

# Tests
api.add_resource(UserAttemptsListController, '/api/test_attempts')
api.add_resource(UserAttemptsController, '/api/test_attempts/<attempt_id>')
api.add_resource(UserAnswerController, '/api/test_attempts/<attempt_id>/answer')

# News
api.add_resource(NewsListController, '/api/news')
api.add_resource(NewsController, '/api/news/<news_id>')
api.add_resource(NewsUserImageUploaderController, '/api/news/<news_id>/image')


# Stats
api.add_resource(RecycleStatisticController, '/api/stats')

# Lookups
api.add_resource(LookupsControllerList, '/admin/lookups')

# swagger
swagger_ui_blueprint = get_swaggerui_blueprint(
    Configuration.USER_SWAGGER_URL,
    Configuration.USER_SCHEMA_URL,
    config={
        'app_name': 'Eco Api',
    }
)
app.register_blueprint(swagger_ui_blueprint)


# babel
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['ru', 'en'])

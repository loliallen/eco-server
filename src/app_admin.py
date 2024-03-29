from flask import Flask
from flask_babel import Babel
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

import src.services.Database as Database
from src.controllers.product.product_admin_image_upload import ProductAdminImageUploaderController
from src.config import Configuration
from src.controllers.filter.filter_admin import FilterController, FilterControllerList
from src.controllers.filter.filter_admin_image_update import FilterImageUploaderController
from src.controllers.lookups.admin.lookup_controller import LookupsControllerList
from src.controllers.news.news_admin import NewsListController, NewsController
from src.controllers.news.news_img_upload import NewsAdminImageUploaderController
from src.controllers.partner.admin import PartnerController, PartnerListController
from src.controllers.product.buy_product_admin import BuyProductController, BuyProductListController
from src.controllers.product.product_admin import ProductController, ProductListController
from src.controllers.product.product_item_admin import ProductItemController, \
    ProductItemListController
from src.controllers.recpoint.admin.comment import RecPointCommentListController, \
    RecPointCommentController
from src.controllers.recpoint.admin.comment_approve import CommentsApproveController
from src.controllers.recpoint.admin.rec_point_admin import RecPointController, \
    RecPointListController
from src.controllers.recpoint.admin.rec_point_admin_img_update import \
    RecPointImageUploaderController
from src.controllers.recpoint.admin.offer_admin import RecPointOfferApproveController
from src.controllers.recycle.recycle_transaction_admin import RecycleTransactionListController, \
    RecycleTransactionController
from src.controllers.statistics.admin.get_recycle_district_stat import \
    RecycleStatisticDistrictController
from src.controllers.statistics.admin.get_recycle_stat import RecycleStatisticController
from src.controllers.statistics.admin.get_unique_users import UsersStatisticController
from src.controllers.test.admin.attempts_admin_controller import AdminAttemptsListController, \
    AdminAttemptsController
from src.controllers.test.admin.question_admin_controller import QuestionListController, \
    QuestionController
from src.controllers.test.admin.question_admin_img_uploader import QuestionImageUploaderController
from src.controllers.test.admin.test_admin_controller import TestListController, TestController
from src.controllers.transaction.transaction_admin import (
    AdmissionTransactionListController,
    AdmissionTransactionTransactionController
)
from src.controllers.user.admin.login import LoginController
from src.controllers.user.admin.users import UsersListController, UsersController
from src.controllers.user.admin.users_img_upload import UserImageUploaderController
from src.send_email import mail
from src.utils.custom_swagger import CustomApi

app = Flask(__name__,
            static_url_path=Configuration.STATIC_URL_PATH,
            static_folder=Configuration.STATIC_FOLDER)
app.config.from_object(Configuration)
babel = Babel(app, configure_jinja=False)
Database.global_connect(app.logger)
jwt = JWTManager(app)
api = CustomApi(app, title='EcoApi for Admins',
                authorizations={"JWT": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}})
cors = CORS(app, resources={ "/admin/*": {"origins": "*"}, "/api/*": {"origins": "*"}})

mail.init_app(app)

# Auth
api.add_resource(LoginController, '/admin/login')

# Users
api.add_resource(UsersListController, '/admin/users')
api.add_resource(UsersController, '/admin/users/<user_id>')
api.add_resource(UserImageUploaderController, '/admin/users/<user_id>/image')

# Filters
api.add_resource(FilterControllerList, '/admin/filters')
api.add_resource(FilterImageUploaderController, '/admin/filters/<filter_id>/image')
api.add_resource(FilterController, '/admin/filters/<filter_id>')

# Partners
api.add_resource(PartnerListController, '/admin/partners')
api.add_resource(PartnerController, '/admin/partners/<partner_id>')

# Recycle Points
api.add_resource(RecPointListController, '/admin/rec_points')
api.add_resource(RecPointController, '/admin/rec_points/<rec_point_id>')
api.add_resource(RecPointImageUploaderController, '/admin/rec_points/<rec_point_id>/images')
api.add_resource(RecPointOfferApproveController, '/admin/rec_offer/<rec_point_id>')

# Comments
api.add_resource(RecPointCommentListController, '/admin/comments')
api.add_resource(RecPointCommentController, '/admin/comments/<comment_id>')
api.add_resource(CommentsApproveController, '/admin/comments/<comment_id>/approve')

# Recycle
api.add_resource(RecycleTransactionListController, '/admin/recycle')
api.add_resource(RecycleTransactionController, '/admin/recycle/<recycle_id>')

# Transactions
api.add_resource(AdmissionTransactionListController, '/admin/transactions')
api.add_resource(AdmissionTransactionTransactionController, '/admin/transactions/<transaction_id>')

# Products
api.add_resource(ProductListController, '/admin/products')
api.add_resource(ProductController, '/admin/products/<product_id>')
api.add_resource(ProductAdminImageUploaderController, '/admin/products/<product_id>/image')
api.add_resource(ProductItemListController, '/admin/product_items')
api.add_resource(ProductItemController, '/admin/product_items/<product_item_id>')
api.add_resource(BuyProductListController, '/admin/buy_product')
api.add_resource(BuyProductController, '/admin/buy_product/<transaction_id>')

# Tests
api.add_resource(TestListController, '/admin/tests')
api.add_resource(TestController, '/admin/tests/<test_id>')
api.add_resource(QuestionListController, '/admin/questions')
api.add_resource(QuestionController, '/admin/questions/<question_id>')
api.add_resource(QuestionImageUploaderController, '/admin/questions/<question_id>/image')
api.add_resource(AdminAttemptsListController, '/admin/attempts')
api.add_resource(AdminAttemptsController, '/admin/attempts/<attempt_id>')

# News
api.add_resource(NewsListController, '/admin/news')
api.add_resource(NewsController, '/admin/news/<news_id>')
api.add_resource(NewsAdminImageUploaderController, '/admin/news/<news_id>/image')

# Statistics
api.add_resource(RecycleStatisticController, '/admin/recycle_stat')
api.add_resource(RecycleStatisticDistrictController, '/admin/recycle_stat_district')
api.add_resource(UsersStatisticController, '/admin/users_stat')

# Lookups
api.add_resource(LookupsControllerList, '/admin/lookups')

# swagger
swagger_ui_blueprint = get_swaggerui_blueprint(
    Configuration.SWAGGER_URL,
    Configuration.SCHEMA_URL,
    config={
        'app_name': "Eco Admin"
    }
)
app.register_blueprint(swagger_ui_blueprint)

from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

import src.services.Database as Database
from src.config import Configuration
from src.controllers.filter.filter_admin import FilterController, FilterControllerList
from src.controllers.filter.filter_admin_image_update import FilterImageUploaderController
from src.controllers.news.news_admin import NewsListController, NewsController
from src.controllers.news.news_img_upload import NewsAdminImageUploaderController
from src.controllers.partner.admin import PartnerController, PartnerListController
from src.controllers.product.product_admin import ProductController, ProductListController
from src.controllers.product.product_item_admin import ProductItemController, ProductItemListController
from src.controllers.product.buy_product_admin import BuyProductController, BuyProductListController
from src.controllers.recpoint.rec_point_admin import RecPointController, RecPointListController
from src.controllers.recpoint.offer_admin import RecPointOfferApproveController
from src.controllers.recpoint.rec_point_admin_img_update import RecPointImageUploaderController
from src.controllers.recycle.recycle_transaction_admin import RecycleTransactionListController, RecycleTransactionController
from src.controllers.test.admin.attempts_admin_controller import AdminAttemptsListController, AdminAttemptsController
from src.controllers.test.admin.question_admin_controller import QuestionListController, QuestionController
from src.controllers.test.admin.question_admin_img_uploader import QuestionImageUploaderController
from src.controllers.test.admin.test_admin_controller import TestListController, TestController
from src.controllers.transaction.transaction_admin import AdmissionTransactionListController, \
    AdmissionTransactionTransactionController
from src.middleware.collect_statistics import Collector
from src.send_email import mail
from src.utils.custom_swagger import CustomApi

app = Flask(__name__,
            static_url_path=Configuration.STATIC_URL_PATH,
            static_folder=Configuration.STATIC_FOLDER)
app.config.from_object(Configuration)
app.wsgi_app = Collector(app.wsgi_app)
Database.global_connect()
api = CustomApi(app, title='EcoApi for Admins')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

mail.init_app(app)

# Filters and Recycle Points
api.add_resource(FilterControllerList, '/admin/filters')
api.add_resource(FilterImageUploaderController, '/admin/filters/<filter_id>/image')
api.add_resource(FilterController, '/admin/filters/<filter_id>')
api.add_resource(PartnerListController, '/admin/partners')
api.add_resource(PartnerController, '/admin/partners/<partner_id>')
api.add_resource(RecPointListController, '/admin/rec_points')
api.add_resource(RecPointController, '/admin/rec_points/<rec_point_id>')
api.add_resource(RecPointImageUploaderController, '/admin/rec_points/<rec_point_id>/images')
api.add_resource(RecPointOfferApproveController, '/admin/rec_offer/<rec_point_id>')


# Recycle
api.add_resource(RecycleTransactionListController, '/admin/recycle')
api.add_resource(RecycleTransactionController, '/admin/recycle/<recycle_id>')

# Transactions
api.add_resource(AdmissionTransactionListController, '/admin/transactions')
api.add_resource(AdmissionTransactionTransactionController, '/admin/transactions/<transaction_id>')

# Products
api.add_resource(ProductListController, '/admin/products')
api.add_resource(ProductController, '/admin/products/<product_id>')
api.add_resource(ProductItemListController, '/admin/product_items')
api.add_resource(ProductItemController, '/admin/product_items/<product_item_id>')
api.add_resource(BuyProductListController, '/admin/buy_product')
api.add_resource(BuyProductController, '/admin/buy_product/<transaction_id>')

# Tests
api.add_resource(TestListController, '/admin/tests')
api.add_resource(TestController, '/admin/tests/<tests_id>')
api.add_resource(QuestionListController, '/admin/tests/<test_id>/questions')
api.add_resource(QuestionController, '/admin/tests/<test_id>/questions/<question_id>')
api.add_resource(QuestionImageUploaderController, '/admin/tests/<test_id>/questions/<question_id>/image')
api.add_resource(AdminAttemptsListController, '/admin/tests/<test_id>/attempts')
api.add_resource(AdminAttemptsController, '/admin/tests/<test_id>/attempts/<attempt_id>')

# News
api.add_resource(NewsListController, '/admin/news')
api.add_resource(NewsController, '/admin/news/<news_id>')
api.add_resource(NewsAdminImageUploaderController, '/admin/news/<news_id>/image')

# swagger
swagger_ui_blueprint = get_swaggerui_blueprint(
    Configuration.ADMIN_SWAGGER_URL,
    Configuration.ADMIN_SCHEMA_URL,
    config={
        'app_name': "Eco Admin"
    }
)
app.register_blueprint(swagger_ui_blueprint)

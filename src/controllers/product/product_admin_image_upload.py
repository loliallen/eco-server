from flask_restful_swagger_3 import swagger

from models.product.ProductModel import Product
from src.controllers.utils.BaseController import BaseController
from src.controllers.utils.img_saver import save_img
from src.utils import custom_swagger
from src.utils.roles import jwt_reqired_backoffice

root = "products"


class ProductAdminImageUploaderController(BaseController):

    @jwt_reqired_backoffice('product', 'edit')
    @swagger.security(JWT=[])
    @swagger.tags('Products')
    @swagger.response(response_code=201, schema=custom_swagger.OkSchema,
                      summary='Загрузить изображение продукта (купона)', description='-')
    @custom_swagger.mark_files_request()
    def post(self, product_id):
        product = Product.find_by_id_(product_id)
        if product is None:
            return {'error': f'Product not found'}, 404
        save_img(product, root)
        return {'status': 'ok'}, 201

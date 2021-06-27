from flask_jwt_extended import jwt_required
from flask_restful_swagger_3 import swagger

from src.controllers.utils.BaseController import BaseController
from src.controllers.utils.img_saver import save_img
from src.models.news.NewsModel import News
from src.models.user.UserModel import User
from src.utils import custom_swagger
from src.utils.roles import role_need, Roles

root = "news"


class NewsAdminImageUploaderController(BaseController):

    @swagger.tags('News')
    @swagger.response(response_code=201, schema=custom_swagger.OkSchema,
                      summary='Загрузить изображение новости', description='-')
    @custom_swagger.mark_files_request()
    def post(self, news_id):
        news = News.find_by_id_(news_id)
        if news is None:
            return {'error': f'News not found'}, 404
        save_img(news, root)
        return {'status': 'ok'}, 201


class NewsUserImageUploaderController(BaseController):

    @jwt_required()
    @role_need([Roles.admin_pp])
    @swagger.security(JWT=[])
    @swagger.tags('News')
    @swagger.response(response_code=201, schema=custom_swagger.OkSchema,
                      summary='Загрузить изображение новости (Только для админов ПП)', description='-')
    @custom_swagger.mark_files_request()
    def post(self, news_id):
        admin_pp = User.get_user_from_request()
        news = News.objects.filter(id=news_id, author=admin_pp)
        if news is None:
            return {'error': f'News not found'}, 404
        save_img(news, root)
        return {'status': 'ok'}, 201

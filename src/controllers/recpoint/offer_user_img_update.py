from flask_jwt_extended import jwt_required
from flask_restful_swagger_3 import swagger

from src.controllers.utils.BaseController import BaseController
from src.controllers.utils.img_saver import save_imgs
from src.models.recpoint.RecPointModel import RecPoint
from src.models.user.UserModel import User
from src.models.utils.enums import Status
from src.utils import custom_swagger

root = "rec_points"


class RecPointImageUploaderController(BaseController):

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=201, schema=custom_swagger.OkSchema,
                      summary='Загрузить изображения для предложенного ПП', description='-')
    @custom_swagger.mark_files_request(is_list=True)
    def post(self, rec_point_id):
        user = User.get_user_from_request()
        rec_point = RecPoint.objects.filter(id=rec_point_id).first()
        if rec_point is None:
            return {'error': 'RecycleTransaction not found'}, 404
        if rec_point.author.id != user.id:
            return {'error': 'Permission denied'}, 403
        if rec_point.approve_status != Status.idle.value:
            return {'error': 'Permission denied'}, 403
        save_imgs(rec_point, root)
        return {'status': 'ok'}, 201

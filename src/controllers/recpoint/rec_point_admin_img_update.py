from flask_restful_swagger_3 import swagger

from src.controllers.utils.BaseController import BaseController
from src.controllers.utils.img_saver import save_imgs
from src.models.recpoint.RecPointModel import RecPoint
from src.utils import custom_swagger

root = "rec_points"


class RecPointImageUploaderController(BaseController):

    @swagger.tags('Recycle Points')
    @swagger.response(response_code=201, schema=custom_swagger.OkSchema,
                      summary='Загрузить изображения для ПП', description='-')
    @custom_swagger.mark_files_request(is_list=True)
    def post(self, rec_point_id):
        rec_point = RecPoint.objects.filter(id=rec_point_id).first()
        if rec_point is None:
            return {'error': f'RecycleTransaction not found'}, 404
        save_imgs(rec_point, root)
        return {'status': 'ok'}, 201

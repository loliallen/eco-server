from flask_jwt_extended import jwt_required
from flask_restful_swagger_3 import swagger

from src.controllers.utils.BaseController import BaseController
from src.controllers.utils.img_saver import save_imgs
from src.models.recpoint.RecPointComment import RecPointComment
from src.models.user.UserModel import User
from src.models.utils.enums import Status
from src.utils import custom_swagger

root = "rec_points/{id}/comments"


class RecPointCommentImageUploaderController(BaseController):

    @jwt_required()
    @swagger.security(JWT=[])
    @swagger.tags('Filters and Recycle Points')
    @swagger.response(response_code=201, schema=custom_swagger.OkSchema,
                      summary='Загрузить изображения для комментария', description='-')
    @custom_swagger.mark_files_request(is_list=True)
    def post(self, comment_id):
        user = User.get_user_from_request()
        comment = RecPointComment.objects.filter(id=comment_id).first()
        if comment is None:
            return {'error': 'Comment not found'}, 404
        if user != comment.user:
            return {'error': 'Permission denied'}, 403
        if comment.transaction.status != Status.idle.value:
            return {'error': 'Permission denied (comment already approved)'}, 403
        save_imgs(comment, root.format(id=comment.rec_point.id))
        return {'status': 'ok'}, 201

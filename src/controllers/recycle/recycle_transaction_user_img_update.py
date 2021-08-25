from flask_babel import lazy_gettext as _
from flask_jwt_extended import jwt_required
from flask_restful_swagger_3 import swagger

from src.controllers.utils.BaseController import BaseController
from src.controllers.utils.img_saver import save_imgs
from src.models.recycle.RecycleTransaction import RecycleTransaction
from src.models.user.UserModel import User
from src.utils import custom_swagger
from src.utils.roles import role_need, Roles

root = "recycle_transactions"


class RecycleImageUploaderController(BaseController):

    @jwt_required()
    @role_need([Roles.admin_pp])
    @swagger.security(JWT=[])
    @swagger.tags('Recycle')
    @swagger.response(response_code=201, schema=custom_swagger.OkSchema,
                      summary='Загрузить изображения для транзакции зачисления '
                              '(Только для админов пункта  приема)', description='-')
    @custom_swagger.mark_files_request(is_list=True)
    def post(self, recycle_id):
        admin_pp = User.get_user_from_request()
        transaction = RecycleTransaction.objects.filter(id=recycle_id, admin_pp=admin_pp).first()
        if transaction is None:
            return {'error': _('RecycleTransaction not found')}, 404
        save_imgs(transaction, root)
        return {'status': 'ok'}, 201

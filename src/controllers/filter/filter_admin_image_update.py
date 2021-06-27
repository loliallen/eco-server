import os
import pathlib

from flask_restful_swagger_3 import swagger

from src.config import Configuration
from src.controllers.utils.BaseController import BaseController
from src.controllers.utils.img_saver import save_img
from src.models.filter.FilterModel import Filter
from src.utils import custom_swagger

root = "filters"


class FilterImageUploaderController(BaseController):

    @swagger.tags('Filters')
    @swagger.response(response_code=201, schema=custom_swagger.OkSchema,
                      summary='Загрузить изображение фильтра', description='-')
    @custom_swagger.mark_files_request()
    def post(self, filter_id):
        filter = Filter.find_by_id_(filter_id)
        if filter is None:
            return {'error': f'Filter not found'}, 404
        save_img(filter, root, field_name="var_name")
        return {'status': 'ok'}, 201

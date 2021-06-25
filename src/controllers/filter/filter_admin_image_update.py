import os
import pathlib

from flask_restful_swagger_3 import swagger
from werkzeug.utils import secure_filename

from src.config import Configuration
from src.controllers.utils.BaseController import BaseController
from src.models.filter.FilterModel import Filter
from src.utils import custom_swagger
from src.utils.custom_swagger import post_parser_with_file

root = "filters"
files_storage = pathlib.Path(Configuration.STATIC_FOLDER) / root
if not os.path.exists(files_storage):
    os.mkdir(files_storage)


class FilterImageUploaderController(BaseController):

    @swagger.tags('Filters')
    @swagger.response(response_code=201, schema=custom_swagger.OkSchema,
                      summary='Загрузить изображение фильтра', description='-')
    @custom_swagger.mark_files_request()
    def post(self, filter_id):
        args = post_parser_with_file.parse_args()

        filter = Filter.find_by_id_(filter_id)
        if filter is None:
            return {'error': 'Filter not found'}, 404

        file = args.pop('file')[0]
        filename = secure_filename(file.filename)
        FILES_PATH = files_storage / str(filter.id)
        if not os.path.exists(FILES_PATH):
            os.mkdir(FILES_PATH)
        FILES_PATH = FILES_PATH / filename
        file.save(FILES_PATH.resolve())
        filter.image = f'{root}/{filter.id}/{filename}'
        filter.save()
        return {'status': 'ok'}, 201
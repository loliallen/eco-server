import os
import pathlib

from werkzeug.utils import secure_filename

from src.config import Configuration
from src.utils.custom_swagger import post_parser_with_file, post_parser_with_files


# TODO:
#  - вынести дублирующийся код в отдельный метод, возможно объединить в один
#  метод с параметром is_list.
#  - Добавить параметр название поля изображения(ий) в модели


def save_img(obj, root, files_storage: pathlib.Path=None, field_name="id"):
    if files_storage is None:
        files_storage = pathlib.Path(Configuration.STATIC_FOLDER)
    if not os.path.exists(files_storage / root):
        os.mkdir(files_storage / root)

    args = post_parser_with_file.parse_args()

    file = args.pop('file')[0]
    filename = secure_filename(file.filename)
    obj_ident = str(getattr(obj, field_name))
    FILES_PATH = files_storage / root / obj_ident
    if not os.path.exists(FILES_PATH):
        os.mkdir(FILES_PATH)

    if obj.image is not None:
        os.remove((files_storage / obj.image).resolve())
    FILES_PATH = FILES_PATH / filename
    file.save(FILES_PATH.resolve())
    obj.update(set__image=f'{root}/{obj_ident}/{filename}')


def save_imgs(obj, root, files_storage: pathlib.Path=None, field_name="id"):
    if files_storage is None:
        files_storage = pathlib.Path(Configuration.STATIC_FOLDER)
    if not os.path.exists(files_storage / root):
        os.mkdir(files_storage / root)

    args = post_parser_with_files.parse_args()

    files = args.pop('files')

    if obj.images is not None:
        for image in obj.images:
            path = (files_storage / image).resolve()
            if os.path.exists(path):
                os.remove((files_storage / image).resolve())

    images = []
    for file in files:
        filename = secure_filename(file.filename)
        obj_ident = str(getattr(obj, field_name))
        FILES_PATH = files_storage / root / obj_ident
        if not os.path.exists(FILES_PATH):
            os.mkdir(FILES_PATH)
        FILES_PATH = FILES_PATH / filename
        file.save(FILES_PATH.resolve())
        images.append(f'{root}/{obj_ident}/{filename}')
    obj.update(set__images=images)


import os
from pathlib import Path

from mongoengine import Document, StringField, ListField, FloatField

from models.utils.BaseCrud import BaseCrud

REL_PATH = "/statics/filters"
files_storage = Path('./src'+REL_PATH)


class Filter(Document, BaseCrud):
    name = StringField(required=True, comment='Имя')
    var_name = StringField(required=True, comment='Код фильтра')
    image = StringField(comment='Картинка ресурса')
    key_words = ListField(StringField(), comment='Список слов-ассоциаций для поиска')
    bad_words = ListField(StringField(), comment='Стоп список слов для поиска')
    coins_per_unit = FloatField(default=1, comment='Кол-во эко-коинов за единицу сданного ресурса')
    meta = {
        "db_alias": "core",
        "collection": "filters",
        "comment": "Таблица для хранения типа отхода (батарейка, макулатура)"
    }

    def save_img(self, image):
        mime_type = image.split('.').pop()
        filename = str(self.id) + "." + mime_type
        img_path = REL_PATH + "/" + filename
        old_path = files_storage / image
        new_path = files_storage / filename
        os.rename(old_path.resolve(), new_path.resolve())
        self.image = img_path

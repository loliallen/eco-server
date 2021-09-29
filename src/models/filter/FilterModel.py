import os
from pathlib import Path

from mongoengine import Document, StringField, ListField, FloatField, BooleanField

from src.models.utils.BaseCrud import BaseCrud


class Filter(Document, BaseCrud):
    name = StringField(required=True, unique=True, comment='Имя')
    var_name = StringField(required=True, unique=True, comment='Код фильтра')
    image = StringField(comment='Картинка ресурса')
    key_words = ListField(StringField(), comment='Список слов-ассоциаций для поиска')
    bad_words = ListField(StringField(), comment='Стоп список слов для поиска')
    coins_per_unit = FloatField(default=1, comment='Кол-во эко-коинов за единицу сданного ресурса')
    visible = BooleanField(default=True)
    meta = {
        "db_alias": "core",
        "collection": "filters",
        "comment": "Таблица для хранения типа отхода (батарейка, макулатура)"
    }

    def __repr__(self):
        return f'<Filter: ({self.id}) {self.name}>'

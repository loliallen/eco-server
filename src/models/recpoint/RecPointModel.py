from pathlib import Path
from typing import List

from mongoengine import Document, StringField, ListField, ReferenceField, DictField, BooleanField, PointField, QuerySet

from models.partner.PartnerModel import Partner
from models.utils.BaseCrud import BaseCrud
from src.models.filter.FilterModel import Filter

REL_PATH = "/statics/recpoints"
files_storage = Path('./src'+REL_PATH)


class RecPoint(Document, BaseCrud):
    """Точка переработки"""

    name = StringField(required=True, default='Пункт приема')
    description = StringField()
    images = ListField(StringField())
    getBonus = BooleanField()
    address = StringField(requrend=True)
    partner = ReferenceField(Partner, required=False)
    reception_type = StringField()
    payback_type = StringField()
    contacts = ListField()
    coords = PointField(auto_index=False, reqired=True)
    accept_types = ListField(ReferenceField(Filter), required=False)
    work_time = DictField(required=True)
    meta = {
        "db_alias": "core",
        "collection": "rec_points",
        "indexes": [[("coords", "2dsphere")]]
    }

    @classmethod
    def read_(cls, coords: list = None, filters: list = None, rec_type: str = None, payback_type: str = None) -> QuerySet:
        """
        Custom read for RecPoints with filters

        Args:
            coords: list of points [[0, 0], [12, 23], ...] is polygon
            filters: list of filters ids
            rec_type: rec_type name
            payback_type: payback_type name

        Returns: list of RecPoints in json
        """
        print(filters, coords)
        rec_points = RecPoint.objects
        if filters:
            rec_points = rec_points.filter(accept_types=filters)
        if rec_type:
            rec_points = rec_points.filter(reception_type=rec_type)
        if payback_type:
            rec_points = rec_points.filter(payback_type=payback_type)
        if coords:
            coords.append(coords[0])  # замыкаем полигон
            rec_points = rec_points.filter(coords__geo_within=[coords])
        return rec_points

    @classmethod
    def select_rec_points_near(cls, lon: float, lat: float, radius: int = 10) -> QuerySet:
        """
        Все точки переработки в определенном радиусе
        Args:
            lon:
            lat:
            radius: radius at kilometres
        """
        return RecPoint.objects.filter(coords__near=[lon, lat], coords__max_distance=radius)

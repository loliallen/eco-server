import json
from pathlib import Path
from typing import List

from mongoengine import Document, StringField, ListField, ReferenceField, DictField, BooleanField

from models.partner.PartnerModel import Partner
from models.utils.BaseCrud import BaseCrud
from src.models.filter.FilterModel import Filter
from src.utils.coords import coords as check_coords
from src.utils.haversine import haversine

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
    coords = DictField(required=False)  # { lat: int, lng: int }
    accept_types = ListField(ReferenceField(Filter), required=False)
    work_time = DictField(required=True)
    meta = {
        "db_alias": "core",
        "collection": "rec_points"
    }

    @classmethod
    def read_(cls, coords=None, filters=None, rec_type=None, payback_type=None):
        """This is functon thats return all Recycly points"""
        print(filters, coords)
        rec_points = RecPoint.objects
        if filters:
            rec_points = rec_points.filter(accept_types=filters)
        if rec_type:
            rec_points = rec_points.filter(reception_type=rec_type)
        if payback_type:
            rec_points = rec_points.filter(payback_type=payback_type)
        return rec_points.to_json()
        # TODO add coords filter
        # https://docs.mongodb.com/manual/reference/operator/query/geoWithin/
        # frp = []
        # for point in rec_points:
        #     if coords:
        #         if "lat" in point.coords and "lng" in point.coords:
        #             dot = [point.coords["lat"], point.coords["lng"]]
        #             if not check_coords(dot, coords):
        #                 continue
        #     frp.append(point.to_json())
        # return json.dumps(frp)

    @classmethod
    def select_rec_points_near(cls, lon: float, lat: float, radius: int = 10) -> List:
        """
        Все точки в определенном радиусе
        Args:
            lon:
            lat:
            radius: radius at kilometres
        """
        rec_points = cls.read_()
        rec_points_res = []
        for rec_point in rec_points:
            coords = rec_point['coords']
            if haversine(lon, lat, float(coords['lon']), float(coords['lat'])) < radius:
                rec_points_res.append(rec_point)
        return rec_points_res

    @classmethod
    def filter_by_accept_type(cls, filter_: Filter, _rec_points: list = None) -> List:
        if not _rec_points:
            _rec_points = cls.read_()
        result_list = []
        for rec_point in _rec_points:
            for fl in rec_point.accept_types:
                if fl.id == filter_.id:
                    result_list.append(rec_point)

        return result_list

    @classmethod
    def does_point_contains_filters(cls, point, filters_isd: List[Filter]) -> bool:
        var_names = list(map(lambda x: x["var_name"], point.accept_types))
        for filter_id in filters_isd:
            eke = [str(i.id) for i in point.accept_types]
            if filter_id in eke:
                return True
        return False

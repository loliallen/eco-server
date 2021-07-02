from mongoengine import Document, StringField, ListField, ReferenceField, DictField, BooleanField, PointField, QuerySet

from src.models.filter.FilterModel import Filter
from src.models.utils.BaseCrud import BaseCrud
from src.models.utils.enums import STATUS_CHOICES, Status


RECEPTION_TYPE_CHOICES = ('recycle', 'utilisation', 'charity')
PAYBACK_TYPE_CHOICES = ('free', 'paid', 'partner')


class RecPoint(Document, BaseCrud):
    """Точка переработки"""

    name = StringField(required=True, default='Пункт приема')
    description = StringField()
    images = ListField(StringField())
    external_images = ListField(StringField())
    getBonus = BooleanField()
    address = StringField(requrend=True)
    partner = ReferenceField('Partner', required=False)
    reception_type = StringField(choices=RECEPTION_TYPE_CHOICES)
    payback_type = StringField(choices=PAYBACK_TYPE_CHOICES)
    contacts = ListField()
    coords = PointField(auto_index=False, reqired=True)
    accept_types = ListField(ReferenceField(Filter), required=False)
    work_time = DictField(required=True)
    approve_status = StringField(choices=STATUS_CHOICES, default=Status.idle.value)
    author = ReferenceField('User')
    # если это изменение - то здесь будет ссылка на изменяемый объект
    change_by = ReferenceField('RecPoint')

    meta = {
        "db_alias": "core",
        "collection": "rec_points",
        "indexes": [[("coords", "2dsphere")]],
        "strict": False,
    }

    @classmethod
    def read(cls, position: list, radius: int, filters: list = None, reception_type: str = None,
             payback_type: str = None, status: str = True) -> QuerySet:
        """
        Custom read for RecPoints with filters
        """
        rec_points = RecPoint.objects
        if filters:
            rec_points = rec_points.filter(accept_types=filters)
        if reception_type:
            rec_points = rec_points.filter(reception_type=reception_type)
        if payback_type:
            rec_points = rec_points.filter(payback_type=payback_type)

        radian = (radius * 10) / 6378.1
        rec_points = rec_points.filter(coords__geo_within_center=[position, radian])
        if status:
            rec_points = rec_points.filter(approve_status=status)

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

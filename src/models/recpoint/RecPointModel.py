from mongoengine import Document, StringField, ListField, ReferenceField, DictField, BooleanField, PointField, QuerySet

from src.models.filter.FilterModel import Filter
from src.models.utils.BaseCrud import BaseCrud
from src.models.utils.enums import STATUS_CHOICES, Status


RECEPTION_TYPE_CHOICES = ('recycle', 'utilisation', 'charity')
PAYBACK_TYPE_CHOICES = ('free', 'paid', 'partner')
DISTRICTS = (
    'Приволжский',
    'Советский',
    'Вахитовский',
    'Ново-Савинский',
    'Московский',
    'Кировский',
    'Авиастроительный'
)


class RecPoint(Document, BaseCrud):
    """Точка переработки"""

    name = StringField(required=True, default='Пункт приема')
    description = StringField()
    images = ListField(StringField())
    external_images = ListField(StringField())
    getBonus = BooleanField()
    address = StringField(requrend=True)
    district = StringField()
    partner = ReferenceField('Partner')
    reception_type = StringField(choices=RECEPTION_TYPE_CHOICES)
    payback_type = StringField(choices=PAYBACK_TYPE_CHOICES)
    contacts = ListField(StringField())
    coords = PointField(auto_index=False)
    accept_types = ListField(ReferenceField(Filter))
    work_time = DictField()
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
    def read(cls,
             position: list,
             radius: int,
             filters: list = None,
             reception_type: str = None,
             payback_type: str = None,
             approve_status: str = None,
             id__in: list = None,
             **kwargs
             ) -> QuerySet:
        """
        Custom read for RecPoints with filters
        """
        rec_points = RecPoint.objects
        if filters:
            for filter in filters:
                rec_points = rec_points.filter(accept_types__contains=filter)
        if reception_type:
            rec_points = rec_points.filter(reception_type=reception_type)
        if payback_type:
            rec_points = rec_points.filter(payback_type=payback_type)
        if id__in:
            rec_points = rec_points.filter(id__in=id__in)

        if position and radius:
            radian = (radius * 10) / 6378.1
            rec_points = rec_points.filter(coords__geo_within_center=[position, radian])
        if approve_status is not None:
            rec_points = rec_points.filter(approve_status=approve_status)

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

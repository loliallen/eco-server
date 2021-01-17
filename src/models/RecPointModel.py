from mongoengine import Document, StringField, ListField, ReferenceField, DictField, BooleanField
from mongoengine.fields import LazyReferenceField
from mongoengine.queryset.queryset import QuerySet
import json

from src.models.FilterModel import Filter
from src.models.ReceptionTargetModel import ReceptionTarget
from src.models.ReceptionTypeModel import ReceptionType
from src.utils.JsonEncoder import JSONEncoder
from src.utils.haversine import haversine

class RecPoint(Document):
    ''' Recycle model to store Recycle points

    Args:
        Document ([type]): [description]
    '''
    name = StringField(required=True, default='Пункт приема')
    description = StringField()
    getBonus = BooleanField()
    address = StringField(requrend=True)
    partner = ReferenceField('Partner', required=False)
    photo_path = StringField()
    reception_target = ReferenceField(ReceptionTarget)
    reception_type = ReferenceField(ReceptionType)
    contacts = StringField()
    coords = DictField(required=False) # { lat: int, lng: int }
    accept_types = ListField(ReferenceField(Filter), required=False)
    work_time = DictField(required=True)
    meta = {
        "db_alias": "core",
        "collection": "rec_points"
    }
    def to_jsony(self):
        self.select_related(max_depth=2)
        data = self.to_mongo()
        if 'partner' in data: #reference field
            data['partner'] = self.partner.to_mongo() #reference field
        if 'reception_target' in data:
            data['reception_target'] = self.reception_target.to_mongo()
        if 'reception_type' in data:
            data['reception_type'] = self.reception_type.to_mongo()
        
        for i, r_point in enumerate(self.accept_types):  #ListFiled(ReferenceField)
            data['accept_types'][i] = r_point.to_mongo()
        print(json.loads(json.dumps(data, cls=JSONEncoder)))
        return json.loads(json.dumps(data, cls=JSONEncoder))


def read() -> QuerySet:
    """This is functon thats return all Recycly points

    Returns:
        QuerySet: Set of RecPoint Documents
    """
    rec_points = RecPoint.objects.all()

    return rec_points

def create(obj: object) -> RecPoint:

    rec_point = RecPoint(**obj)
    
    rec_point.save()
    return rec_point




def update(_id: str, updates: object) -> RecPoint:
    rec_point = RecPoint.objects(id=_id).first()
    if not rec_point:
        return None
    rec_point.update(**updates)
    return rec_point


def delete(_id: str) -> RecPoint:
    """This is functon thats deletes Recycle points
    Args:
        _id (str): RecPoints id

    Returns:
        RecPoint: Deleted RecPoint
    """
    rec_point = RecPoint.objects(id=_id).first()
    if not rec_point:
        return None
    rec_point.delete()
    return rec_point

def find_by_id(_id: str) -> RecPoint:
    rec_point = RecPoint.objects(id=_id).first()
    if not rec_point:
        return None
    return rec_point


def select_rec_points_near(lon: float, lat: float) -> list:
    rec_points = read()
    # radius at kilometres
    radius = 10
    rec_points_res = []
    for rec_point in rec_points:
        coords = rec_point['coords']
        if haversine(lon, lat, float(coords['lon']), float(coords['lat'])) < radius:
            rec_points_res.append(rec_point)
    return rec_points_res


def filter_by_reception_target(rec_target: ReceptionTarget, _rec_points: list = []) -> list:
    if not _rec_points:
        _rec_points = read()
    result_list = []
    for rec_point in _rec_points:
        if rec_point.reception_target.id == rec_target.id:
            result_list.append(rec_point)
    return result_list


def filter_by_reception_type(rec_type: ReceptionType , _rec_points: list = []) -> list:
    if not _rec_points:
        _rec_points = read()
    result_list = []
    for rec_point in _rec_points:
        if rec_point.reception_type.id == rec_type.id:
            result_list.append(rec_point)
    return result_list

def filter_by_accept_type(filter: Filter , _rec_points: list = []) -> list:
    if not _rec_points:
        _rec_points = read()
    result_list = []
    for rec_point in _rec_points:
        for fl in rec_point.accept_types:
            if fl.id == filter.id:
                result_list.append(rec_point)

    return result_list
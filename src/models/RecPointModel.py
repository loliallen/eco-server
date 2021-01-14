from bson import json_util
from mongoengine import Document, StringField, ListField, ReferenceField, EmbeddedDocumentField, DictField, BooleanField, EmbeddedDocument, DecimalField
from mongoengine.fields import LazyReferenceField
from mongoengine.queryset.queryset import QuerySet
from models.CustomQueySet import CustomQuerySet

from models.FilterModel import Filter

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
    contacts = StringField()
    coords = DictField(required=False)
    accept_types = ListField(LazyReferenceField(Filter), required=False)
    work_time = DictField(required=True)
    meta = {
        "db_alias": "core",
        "collection": "rec_points"
    }

'''
   Этот метод решает проблему, но появляются проблемы с кодировкой (в JSON почему-то слеши)
    def to_json(self):
        self.select_related(max_depth=2)
        data = self.to_mongo()
        data['id'] = json_util.dumps(self.id)
        data['partner'] = self.partner.to_mongo()
        for i, r_point in enumerate(self.accept_types):
            data['accept_types'][i] = r_point.to_mongo()
        print(json.dumps(data, default=json_util.default))
        return json.dumps(data, default=json_util.default)
    '''

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


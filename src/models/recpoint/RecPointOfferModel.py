from mongoengine import Document, BooleanField, ListField, StringField, DictField, ReferenceField

from models.utils.BaseCrud import BaseCrud


class RecPointOffer(Document, BaseCrud):
    coords = DictField()
    description = StringField()
    contact = ListField()
    recpoint = ReferenceField('RecPoint')
    images = ListField(StringField())
    getBonus = BooleanField()
    address = StringField(requrend=True)
    reception_type = StringField()
    payback_type = StringField()
    accept_types = ListField(ReferenceField('Filter'), required=False)
    work_time = DictField(required=True)
    
    meta = {
        "db_alias": "core",
        "collection": "rec_points_offer"
    }

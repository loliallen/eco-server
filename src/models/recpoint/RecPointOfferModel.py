from mongoengine import Document, BooleanField, ListField, StringField, DictField, ReferenceField

class RecPointOffer(Document):
    coords = DictField()
    description = StringField()
    contact = ListField()
    recpoint = ReferenceField('RecPoint')
    description = StringField()
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

def create(obj):
    rec_off = RecPointOffer(**obj)
    rec_off.save()

    return rec_off
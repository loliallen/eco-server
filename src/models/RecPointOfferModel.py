from mongoengine import Document, StringField, DictField

class RecPointOffer(Document):
    coords = DictField()
    description = StringField()
    contact = DictField()
    
    meta = {
        "db_alias": "core",
        "collection": "rec_points_offer"
    }

def create(obj):
    rec_off = RecPointOffer(**obj)
    rec_off.save()

    return rec_off
from datetime import datetime

from mongoengine import Document, DateTimeField, StringField, ReferenceField, DictField

from src.models.partner.PartnerModel import Partner
from src.models.recpoint.RecPointModel import RecPoint
from src.models.user.UserModel import User


class RequestsStatistic(Document):
    request_uri = StringField()
    date = DateTimeField(default=datetime.utcnow)
    params = DictField()
    user = ReferenceField(User, required=False)
    user_agent = StringField()
    
    meta = {
        "db_alias": "core",
        "collection": "requests_statistics"
    }



# эти методы не используются, оставил их как пример для группировки
def aggr(date=True, request=False):
    pipeline = [
        {
            "$group": {
                "_id": {
                    "year" : { "$year" : "$date" },        
                    "month" : { "$month" : "$date" },        
                    "day" : { "$dayOfMonth" : "$date" },
                },
                "requests": {
                    "$push": "$request_uri"
                }
            }
        }
    ]
    data = list(Statistic.objects.aggregate(*pipeline))
    print(data)
    return data

def users():
    users = len(User.objects.all())
    partners = len(Partner.objects.all())
    rec_points = len(RecPoint.objects.all())

    return {'Пользователи': users, 'Партнеры': partners, 'Пункты приема': rec_points}
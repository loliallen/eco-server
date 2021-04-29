from mongoengine import Document, DateTimeField, StringField, ReferenceField
from src.models.user.UserModel import User
#from src.models.partner.PartnerModel import Partner
#from src.models.recpoint.RecPointModel import RecPoint
from datetime import datetime
from src.utils.JsonEncoder import JSONEncoder
from bson import json_util
import json

class Statistic(Document):

    request_uri = StringField()
    date = DateTimeField(default=datetime.now)
    user = ReferenceField(User, required=False)
    
    meta = {
        "db_alias": "core",
        "collection": "statistics"
    }

    def to_jsony(self):
        self.select_related(max_depth=2)
        data = self.to_mongo()
        if 'user' in data: #reference field
            data['user'] = self.user.to_mongo() #reference field
        # if 'reception_target' in data:
        #     data['reception_target'] = self.reception_target.to_mongo()
        # if 'reception_type' in data:
        #     data['reception_type'] = self.reception_type.to_mongo()
        # for i, r_point in enumerate(self.points):  #ListFiled(ReferenceField)
        #     data['points'][i] = r_point.to_mongo()
        data['date'] = str(self.date)
        return json.loads(json.dumps(data, cls=JSONEncoder))

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
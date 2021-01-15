from flask import Flask
from flask_restful import Api

from controllers.FilterController import FilterController
from controllers.PartnerController import PartnerController
from controllers.RecPointController import RecPointController
from controllers.ReceptionTargetController import RecepTargetController
from controllers.ReceptionTypeController import RecepTypeController
from controllers.RecPointSortingController import RecPointsSorting
import services.Database as Database

app = Flask(__name__)
api = Api(app)


api.add_resource(FilterController, '/filters')
api.add_resource(RecPointController, '/rec_points')
api.add_resource(PartnerController, '/partners')
api.add_resource(RecPointsSorting, '/recpoints_sort')
api.add_resource(RecepTargetController, '/reception_targets')
api.add_resource(RecepTypeController, '/reception_types')

if __name__ == "__main__":
    Database.global_connect()
    app.run(debug=True)

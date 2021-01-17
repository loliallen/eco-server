from flask import Flask
from flask_restful import Api

from src.controllers.FilterController import FilterController
from src.controllers.PartnerController import PartnerController
from src.controllers.RecPointController import RecPointController
from src.controllers.ReceptionTargetController import RecepTargetController
from src.controllers.ReceptionTypeController import RecepTypeController
from src.controllers.RecPointSortingController import RecPointsSorting
import src.services.Database as Database

Database.global_connect()


app = Flask(__name__)
api = Api(app)

api.add_resource(FilterController, '/filters')
api.add_resource(RecPointController, '/rec_points')
api.add_resource(PartnerController, '/partners')
api.add_resource(RecPointsSorting, '/recpoints_sort')
api.add_resource(RecepTargetController, '/reception_targets')
api.add_resource(RecepTypeController, '/reception_types')

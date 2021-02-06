from flask import Flask
from flask_restful import Api

from src.controllers.FilterController import FilterController
from src.controllers.RecPointController import RecPointController
from src.controllers.MarkerController import MarkerController, MarkerControllerList, MarkerControllerListAll
import src.services.Database as Database

Database.global_connect()


app = Flask(__name__)
api = Api(app)

api.add_resource(FilterController, '/api/filters')
api.add_resource(RecPointController, '/api/rec_points')
api.add_resource(MarkerController, '/api/markers')
api.add_resource(MarkerControllerList, '/api/markers/list')
api.add_resource(MarkerControllerListAll, '/api/markers/list/all')



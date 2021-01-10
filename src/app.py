from flask import Flask
from flask_restful import Api

from controllers.FilterController import FilterController
from controllers.PartnerController import PartnerController
from controllers.RecPointController import RecPointController
import services.Database as Database

app = Flask(__name__)
api = Api(app)


api.add_resource(FilterController, '/')
api.add_resource(RecPointController, '/rec_points')
api.add_resource(PartnerController, '/partners')

if __name__ == "__main__":
    Database.global_connect()
    app.run(debug=True)

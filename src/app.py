from flask import Flask
from flask_restful import Api

from controllers.FilterController import FilterController
import services.Database as Database

app = Flask(__name__)
api = Api(app)


api.add_resource(FilterController, '/')

if __name__ == "__main__":
    Database.global_connect()
    app.run(debug=True)

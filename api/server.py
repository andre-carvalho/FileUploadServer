import os, base64
from flask import Flask, request, send_file
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from storage_module.locations_dao import LocationsDao
from base64_module.base64_utils import B64Utils
from logs_module.log_writer import logWriter

SERVER_IP='0.0.0.0'
SERVER_DOMAIN=os.getenv('SERVER_DOMAIN', '127.0.0.1:5000')
DATA_PATH='/uploadImages'

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

class Locations(Resource):
    def post(self):
        # set default
        json_data=None

        # Trying parse the input JSON
        try:
            json_data = request.get_json(force=True)
        except Exception as error:
            error_msg = 'error in Locations class when trying parse input JSON data. Return HTTP:500'
            logWriter(os.path.abspath(os.curdir) + DATA_PATH).write(error_msg)
            return {'status': 'parse error'}, 500
        
        # trying store data into database
        try:
            db = LocationsDao()
            id_photo = db.storeLocation(json_data)
            url_picture = "http://{0}/locations/{1}".format(SERVER_DOMAIN, id_photo)
            db.updateLocation(id_photo, url_picture)
        except Exception as error:
            error_msg = 'error in Locations class when trying store posted data. Return HTTP:500'
            logWriter(os.path.abspath(os.curdir) + DATA_PATH).write(error_msg)
            return {'status': 'database error'}, 500

        # trying write picture to disk
        try:
            curpath = os.path.abspath(os.curdir) + DATA_PATH
            b64 = B64Utils(curpath, json_data['photo'])
            b64.writeToBinary(id_photo)
        except Exception as error:
            error_msg = 'error in Locations class when trying write picture to disk. Return HTTP:500'
            logWriter(os.path.abspath(os.curdir) + DATA_PATH).write(error_msg)
            return {'status': 'IO error'}, 500
        
        return {'status':'completed'}, 201

class LocationsList(Resource):
     def get(self, location_id):
        
        curpath = os.path.abspath(os.curdir) + DATA_PATH
        b64 = B64Utils(curpath)

        # trying read picture from disk
        try:
            imageio,attach,mime = b64.readFromBinary(location_id)
        except Exception as error:
            error_msg = 'error in LocationsList class when trying load picture({0}) from disk. Return HTTP:404'.format(location_id)
            logWriter(os.path.abspath(os.curdir) + DATA_PATH).write(error_msg)
            return 404
        return send_file(imageio, attachment_filename=attach, mimetype=mime)


api.add_resource(Locations, '/locations') # Route_1
api.add_resource(LocationsList, '/locations/<location_id>')


if __name__ == '__main__':
     app.run(host=SERVER_IP, port=5000)
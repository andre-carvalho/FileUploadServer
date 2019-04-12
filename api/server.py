import os
import json
from flask import Flask, request, send_from_directory
from flask_restful import abort, Api, Resource
from werkzeug.utils import secure_filename
from flask_cors import CORS
#from storage_module.midias_dao import MidiasDao
from logs_module.log_writer import logWriter

UPLOAD_FOLDER = '/tmp/uploadImages'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

SERVER_IP='0.0.0.0'
SERVER_DOMAIN=os.getenv('SERVER_DOMAIN', '127.0.0.1:5000')
LOG_PATH='/logs'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

class PhotoUpload(Resource):
    
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def post(self):
        # check if the post request has the file part
        if 'data' not in request.files or 'form_id' not in request.form:
            # No file part
            error_msg = 'Error in PhotoUpload class when trying test the file part from request. Return HTTP:500'
            logWriter(os.path.abspath(os.curdir) + LOG_PATH).write(error_msg)
            return {'status': 'parse error'}, 500
        file = request.files['data']
        form_id = request.form['form_id']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '' or form_id == '':
            error_msg = 'Error in PhotoUpload class when trying read the filename. Return HTTP:500'
            logWriter(os.path.abspath(os.curdir) + LOG_PATH).write(error_msg)
            return {'status': 'parse error'}, 500
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.isdir(app.config['UPLOAD_FOLDER'] + '/' +form_id):
                os.mkdir(app.config['UPLOAD_FOLDER'] + '/' +form_id)
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+ '/' +form_id, filename))
            return {'status':'completed'}, 201

class PhotoDownload(Resource):
    def get(self, form_id, photo_id):
        dir=os.path.join(app.config['UPLOAD_FOLDER'],form_id)
        filename=photo_id+'.jpg'
        # trying read picture from disk and send to client
        try:
            if os.path.isfile(dir+'/'+filename):
                return send_from_directory(dir, filename, as_attachment=False)
        except Exception as error:
            error_msg = 'Error in PhotoDownload class when trying load picture({0}) from disk. Return HTTP:404'.format(photo_id)
            logWriter(os.path.abspath(os.curdir) + LOG_PATH).write(error_msg)
            error_msg = str(error)
            logWriter(os.path.abspath(os.curdir) + LOG_PATH).write(error_msg)
            return 404

class PhotoInput(Resource):
    
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def post(self):
        # check if the post request has the file part
        if 'data' not in request.files or 'json_data' not in request.form:
            # No file part
            error_msg = 'Error in PhotoUpload class when trying test the file part from request. Return HTTP:500'
            logWriter(os.path.abspath(os.curdir) + LOG_PATH).write(error_msg)
            return {'status': 'parse error'}, 500
        file = request.files['data']
        json_data = request.form['json_data']
        # parse JSON:
        aJson = json.loads(json_data)
        user_id = aJson["user_id"]
        print(aJson)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '' or user_id == '':
            error_msg = 'Error in PhotoUpload class when trying read the filename. Return HTTP:500'
            logWriter(os.path.abspath(os.curdir) + LOG_PATH).write(error_msg)
            return {'status': 'parse error'}, 500
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.isdir(app.config['UPLOAD_FOLDER'] + '/' +user_id):
                os.mkdir(app.config['UPLOAD_FOLDER'] + '/' +user_id)
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+ '/' +user_id, filename))
            return {'status':'completed'}, 201

class PhotoOutput(Resource):
    def get(self, user_id, photo_id):
        dir=os.path.join(app.config['UPLOAD_FOLDER'],user_id)
        filename=photo_id+'.jpg'
        # trying read picture from disk and send to client
        try:
            if os.path.isfile(dir+'/'+filename):
                return send_from_directory(dir, filename, as_attachment=False)
            else:
                abort(404)
        except Exception as error:
            error_msg = 'Error in PhotoUpload class when trying read the filename. Return HTTP:500'
            error_msg = error_msg+'\n'+str(error)
            logWriter(os.path.abspath(os.curdir) + LOG_PATH).write(error_msg)
            return {'status': 'file not found'}, 404

api.add_resource(PhotoUpload, '/photo')
api.add_resource(PhotoDownload, '/photo/<form_id>/<photo_id>')
# receive the JSON data together pictures
api.add_resource(PhotoInput, '/send')
api.add_resource(PhotoOutput, '/collect/<user_id>/<photo_id>')


if __name__ == '__main__':
     app.run(host=SERVER_IP, port=5000)
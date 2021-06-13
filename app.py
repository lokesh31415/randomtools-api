from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from marshmallow import ValidationError
from ma import ma
from libs.flask_uploads_copy import configure_uploads, patch_request_class
from libs.file_handler import UPLOAD_SET
from models.message import MessageResponse, ProcessStatus
from resources import compress, file_upload, file_download_delete


# intialize Flask
app = Flask(__name__)
# load .env file
load_dotenv(".env", verbose=True)
# load constants from the config file
app.config.from_object('default_config')
app.config.from_envvar('APPLICATION_SETTINGS')
# limit max file size (10MB)
patch_request_class(app=app, size=10 * 1024 * 1024)
# configure uploadset
configure_uploads(app=app, upload_sets=UPLOAD_SET)
# initialize flask_restful instance
api = Api(app=app)

# handles propagated marshmallow ValidationError exceptions 
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return MessageResponse(message=err.messages, status=ProcessStatus.ERROR).get_json()


# Resources
api.add_resource(compress.CompressResource, "/compress")
api.add_resource(file_upload.FileUploadResource, "/upload")
api.add_resource(file_download_delete.FileDownDelResource, "/downdel/<string:filename>")


if __name__ == '__main__':
    ma.init_app(app=app)
    app.run(port=5000)
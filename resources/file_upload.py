import traceback
from libs.flask_uploads_copy import UploadNotAllowed
from flask import request
from flask_restful import Resource
from werkzeug.datastructures import FileStorage
from schemas.file_upload import FileUploadSchema
from libs import file_handler
from libs.strings import gettext
from libs import logger
from models.message import MessageResponse, ProcessStatus
from models.file_upload import FileUploadResponse

file_upload_schema = FileUploadSchema()

class FileUploadResource(Resource):

    def post(self):
        data = file_upload_schema.load(data=request.files) # {"file": FileStorage}
        file:FileStorage = data["file"]
        file_ext = file_handler.get_extension(file, False)
        folder = file_ext
        try:
            saved_path = file_handler.save_file(file=file, folder=folder)
            basename = file_handler.get_basename(saved_path)
            message = gettext('file_uploaded').format(basename)
            message_json = MessageResponse(message, status=ProcessStatus.SUCCESS).get_json()
            upload_json = FileUploadResponse(basename).get_json()
            response = {**upload_json, **message_json}
            return response, 201
        except UploadNotAllowed:
            message = gettext("invalid_extension").format(file_ext)
            return MessageResponse(message=message, status=ProcessStatus.INVALID).get_json(), 400
        except:
            traceback.print_exc()
            logger.exception(traceback.format_exc())
            msg = gettext('internal_server_error').format(file.filename)
            return MessageResponse(message=msg, status=ProcessStatus.INVALID), 500            



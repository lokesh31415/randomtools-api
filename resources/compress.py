import os
import traceback
from flask_restful import Resource
from flask import request
from models.message import MessageResponse, ProcessStatus
from models.compress import CompressModel, CompressResponse
from schemas.compress import CompressSchema
from libs.strings import gettext
from libs import file_handler
from libs import logger
from libs.compress import CompressionException, compress_pdf

compress_schema = CompressSchema()

COMPRESS_ALLOWD_EXTS = ['pdf']

class CompressResource(Resource):
    """
    Inherits flask_restful Resource object.
    It has one post endpoint handler to perform document compress.
    Payload should follow CompressSchema.
    On successful compression it'll return the compressed file. 
    """    
    def post(self):
        data = compress_schema.load(request.get_json())
        # load the response into compress model
        compress_model = CompressModel(data=data)
        file_name = compress_model.fileName
        basename = file_handler.get_basename(file_name)
        # perform some validations
        file_ext = folder =  file_handler.get_extension(file_name, False)
        # check if this extension allowed for compression
        if file_ext not in COMPRESS_ALLOWD_EXTS:
            message = gettext("compress_invalid_extension").format(file_ext)
            return MessageResponse(message=message, status=ProcessStatus.INVALID).get_json(), 400

        # proceed with compression
        try:
            ip_path = file_handler.get_path(filename=basename, folder=folder)
            out_path = file_handler.get_out_path(ip_path)
            bin_path = os.environ['GHOSTSCRIPT_PATH']
            # compress the saved file
            final_size_mb, ratio = compress_pdf(in_path=ip_path, out_path=out_path,\
                 power=compress_model.power, bin_path=bin_path)
            # send the response
            compress_json = CompressResponse(ratio=ratio, final_size=final_size_mb).get_json()
            message = gettext('compress_success').format(basename)
            msg_json = MessageResponse(message, status=ProcessStatus.SUCCESS).get_json()
            response =  {**compress_json, **msg_json} 
            return response
        except CompressionException as e:
            logger.exception(f"compression - {e.message}")
            message = gettext("compress_failed")
            return MessageResponse(message=message, status=ProcessStatus.FAILED, errmsg=e.message).get_json(), 400
        except:
            traceback.print_exc()
            logger.exception(traceback.format_exc())
            message = gettext("internal_server_error")
            return MessageResponse(message=message, status=ProcessStatus.FAILED).get_json(), 400
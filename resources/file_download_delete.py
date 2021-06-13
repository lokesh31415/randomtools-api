import os
import traceback
from flask import send_file
from flask_restful import Resource
from libs import file_handler
from models.message import MessageResponse, ProcessStatus
from libs.strings import gettext
from libs import logger 


class FileDownDelResource(Resource):
    
    def get(self, filename):
        """
        Returns the requested file if exist.
        If not then responds with error message.
        """
        # retrive folder and out_path 
        folder = file_handler.get_extension(filename, False)
        _, out_path = file_handler.get_inout_paths(filename=filename, folder=folder) 
        
        # check if filename is safe
        if not file_handler.is_filename_safe(file=filename):
            msg = gettext('illegal_filename').format(filename)
            return MessageResponse(message=msg, status=ProcessStatus.INVALID).get_json(), 400
        
        # if file exist then send the file
        try:
            return send_file(out_path)

        except FileNotFoundError:
            msg = gettext('file_not_found').format(filename)
            return MessageResponse(message=msg, status=ProcessStatus.INVALID).get_json(), 400
        
        except:
            traceback.print_exc()
            logger.exception(traceback.format_exc())
            msg = gettext('internal_server_error').format(filename)
            return MessageResponse(message=msg, status=ProcessStatus.INVALID).get_json(), 500


    def delete(self, filename):
        """
        Deletes the provided file from input path as well as in the output path if exist.
        """
        # retrive folder and outpath 
        folder = file_handler.get_extension(filename, False)
        in_path, out_path = file_handler.get_inout_paths(filename=filename, folder=folder) 
        
        # check if filename is safe
        if not file_handler.is_filename_safe(file=filename):
            msg = gettext('illegal_filename').format(filename)
            return MessageResponse(message=msg, status=ProcessStatus.INVALID).get_json(), 400
        try:
            os.remove(in_path)
            os.remove(out_path)
            msg = gettext('file_deleted').format(filename)
            return MessageResponse(message=msg, status=ProcessStatus.SUCCESS).get_json(), 200
        except FileNotFoundError:
            # if out_path exist then remove it
            if os.path.isfile(out_path): os.remove(out_path) 
            msg = gettext('file_not_found').format(filename)
            return MessageResponse(message=msg, status=ProcessStatus.INVALID).get_json(), 400
        
        except:
            traceback.print_exc()
            logger.exception(traceback.format_exc())
            msg = gettext('internal_server_error').format(filename)
            return MessageResponse(message=msg, status=ProcessStatus.INVALID).get_json(), 500




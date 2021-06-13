import os
import re
from typing import Union
from libs.flask_uploads_copy import AUDIO, IMAGES, AUDIO, UploadSet
from werkzeug.datastructures import FileStorage

DOCS = tuple('pdf docx'.split())
ALLOWED_EXTENSIONS = set(IMAGES + AUDIO + DOCS)

UPLOAD_SET = UploadSet(name='files', extensions=tuple(ALLOWED_EXTENSIONS))

def save_file(file: FileStorage, folder: str, filename: str=None) -> str:
    """ 
    Takes FileStorage and saves into a folder (make sure folder will have the file extension as name). 
    If filename (with extension) not mentioned, name from the FileStorage object will be used.
    The file will be saved and its name (including the folder) will be returned
    """
    return UPLOAD_SET.save(storage=file, folder=folder, name=filename)


def get_path(filename: str, folder: str) -> str:
    """ Takes filename (with extension) and folder and returns fullpath  (make sure folder will have the file extension as name). """
    return UPLOAD_SET.path(filename=filename, folder=folder)

def get_out_path(ip_path: str):
    """ 
    Mainly to use as output path in ghostscript.
    Takes input file path with filepath/filename.extension.
    Returns output folder path - filepath/out/filename.extension.
    /out/ folder will be created if does not exist.
    """
    ip_dir, filename = os.path.split(ip_path)
    out_dir = os.path.join(ip_dir, 'out')
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    return os.path.join(out_dir, filename)

def get_inout_paths(filename: str, folder: str) -> str:
    """
    Returns paths of the input file and output file.
    """
    in_path = get_path(filename=filename, folder=folder)    
    out_path = get_out_path(in_path) 
    return in_path, out_path


def find_file_any_format(filename: str, folder: str) -> Union[str, None]:
    """ Takes filename (just name not extension) and folder, reurns path of the first occured extension. """
    for _format in ALLOWED_EXTENSIONS:
        file = f"{filename}.{_format}"
        file_path = UPLOAD_SET.path(filename=file, folder=folder)
        if os.path.isfile(file_path):
            return file_path
        return None


def _retrive_filename(file: Union[str, FileStorage]):
    """ 
    Takes FileStorage and returns the filename. 
    Allows other functions to call with both filename and Filestorage and always returns the file name
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    """ Check if the filename and extension is supported """
    filename = _retrive_filename(file)
    allowd_formats = '|'.join(ALLOWED_EXTENSIONS)
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowd_formats})$"
    return re.match(regex, filename)

def  get_basename(file: Union[str, FileStorage]) -> str:
    """ 
    Returns base name of the file provided.
    static/files/document.pdf -> document.pdf
    """
    filename = _retrive_filename(file)
    return os.path.split(filename)[1]

def get_extension(file: Union[str, FileStorage], include_dot=True) -> str:
    """ 
    Returns extension of the file provided.
    static/files/document.pdf -> .pdf
    """
    filename = _retrive_filename(file)
    ext_with_dot = os.path.splitext(filename)[1]
    return ext_with_dot if include_dot else ext_with_dot.split(".")[1] 




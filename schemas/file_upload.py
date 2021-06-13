from typing import Any, Optional, Mapping
from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


class FileStorageField(fields.Field):
    """ 
    Custom marshmallo field to validate 'file' property from the response.
    which holds actual serilized file data.
    """
    default_error_messages = {
        'invalid': 'Not a valid file.'
    }

    def _deserialize(self, value: Any, attr: Optional[str], data: Optional[Mapping[str, Any]], **kwargs):
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail("invalid") # raises ValidationError

        return value

        
class FileUploadSchema(Schema):
    """
    Custom marshmallo Schema to validate 'file' property from the response.
    which holds actual serilized file data.
    """
    file = FileStorageField(required=True)
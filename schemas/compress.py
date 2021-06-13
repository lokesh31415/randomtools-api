from marshmallow import fields, Schema

class CompressSchema(Schema):
    """
    marshmallow Schema to handle Compression payload.
    """
    power = fields.Int()
    fileName = fields.Str(required=True)

from marshmallow import Schema, fields

class OrganisationSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=False)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    user_id = fields.Int(required=True)
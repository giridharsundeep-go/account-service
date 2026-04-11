from marshmallow import Schema, fields
from validators.validators import UserFlowValidator


class SignupSchema(Schema):
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    gender = fields.Str(required=True)
    password = fields.Str(
        required=True,
        validate=UserFlowValidator.validate_password
    )


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
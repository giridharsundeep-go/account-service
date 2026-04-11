from marshmallow import Schema, fields, ValidationError
import re

class UserFlowValidator:
    def validate_user_flow(self, user_flow):
        if user_flow is None:
            return

    # ===== VALIDATORS =====
    @staticmethod
    def validate_username(value):
        email_regex = r'^[^@]+@[^@]+\.[^@]+$'
        phone_regex = r'^[0-9]{10}$'
        if not (re.match(email_regex, value) or re.match(phone_regex, value)):
            raise ValidationError("Must be valid email or phone")

    @staticmethod
    def validate_password(value):
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{6,}$', value):
            raise ValidationError(
                "Password must contain uppercase, lowercase, number and 6+ chars"
            )


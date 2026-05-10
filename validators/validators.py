from flask_jwt_extended import get_jwt_identity
from marshmallow import Schema, fields, ValidationError
import re

from api_messages.common_messages import message
from database_connectivity import DatabaseConnectivity
from repositories.org_repository import OrganisationRepository
from repositories.user_account_repository import UserAccountRepository

db = DatabaseConnectivity()
org_repo = OrganisationRepository(db)
user_repo = UserAccountRepository(db)

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

    @staticmethod
    def validate_email(value):
        user_email = value
        user_id = user_email  # 🔁 replace with actual lookup if needed
        user = user_repo.get_user_by_email(user_id)
        if not user.get('email') == user_id:
            return message.error({'email': user_id}, 400)
        else:
            return user

from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from database_connectivity import DatabaseConnectivity
from repositories.products_repository import ProductsRepository
from api_messages.common_messages import message
from repositories.user_account_repository import UserAccountRepository
from validators import validators

db = DatabaseConnectivity()
products_repo = ProductsRepository(db)
user_repo = UserAccountRepository(db)


# ✅ CREATE PRODUCT
@app.route('/api/products/create', methods=['POST'])
@jwt_required()
def create_product():
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)
        data = request.get_json()

        name = data.get('name')
        description = data.get('description')

        if not name:
            return message.error({'error': 'Name is required'}, 400)

        product_id = products_repo.create_product(user['id'], name, description)

        return message.success({
            'id': product_id,
            'name': name,
            'description': description
        }, 201)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ GET ALL PRODUCTS BY USER
@app.route('/api/products', methods=['GET'])
@jwt_required()
def get_products():
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        products = products_repo.get_products_by_user(user['id'])
        return message.success(products, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ UPDATE PRODUCT
@app.route('/api/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        data = request.get_json()

        name = data.get('name')
        description = data.get('description')

        if not name:
            return message.error({'error': 'Name is required'}, 400)

        updated = products_repo.update_product(product_id, name, description)

        if updated == 0:
            return message.error({'error': 'Product not found'}, 404)

        return message.success({
            'id': product_id,
            'name': name,
            'description': description
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)


# ✅ DELETE PRODUCT
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    try:
        user_email = get_jwt_identity()
        user = validators.UserFlowValidator.validate_email(user_email)

        deleted = products_repo.delete_product(product_id)

        if deleted == 0:
            return message.error({'error': 'Product not found'}, 404)

        return message.success({
            'message': 'Product deleted successfully',
            'id': product_id
        }, 200)

    except Exception as e:
        return message.error({'error': str(e)}, 500)
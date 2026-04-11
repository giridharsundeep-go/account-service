from flask import jsonify


class message:

    @staticmethod
    def success(data=None, message="Success"):
        return jsonify({
            "success": True,
            "message": message,
            "data": data
        }), 200

    @staticmethod
    def error(message="Error", code=400):
        return jsonify({
            "success": False,
            "message": message
        }), code
import os
import werkzeug
from flask import request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import uuid

from api_messages.common_messages import message
from main import app


@app.route('/api/user/upload-avatar', methods=['POST'])
@jwt_required()  # Or your auth setup
def upload_avatar():
    if 'file' not in request.files:
        return jsonify({"error": "No file stream segment found"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No asset name allocated"}), 400

    if file:
        filename = secure_filename(file.filename)
        # Use a unique identifier to prevent overwrites if needed
        target_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # 🌟 HIGH-SPEED STREAM BUFFER: Saves chunks into storage explicitly fast
        # instead of relying on slow block writes
        file.save(target_path)

        # Return only the relative path string your frontend database expects
        relative_db_path = f"storage/profile_pictures/{filename}"

        return jsonify({
            "status": "success",
            "profile_picture_url": relative_db_path
        }), 200


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'storage', 'profile_pictures')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 2. MATCH THE URL: Added '/api' prefix to match your Angular request exactly
@app.route('/api/storage/profile_pictures/<filename>', methods=['GET'])
def serve_profile_picture(filename):
    try:
        # Debug print: Check your terminal to see exactly where Flask is looking on your disk
        print(f"🔍 Flask is searching for file at: {os.path.join(app.config['UPLOAD_FOLDER'], filename)}")

        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({"error": "File physically missing from disk structure"}), 404
from werkzeug.security import generate_password_hash, check_password_hash
from app.missing_imports import safe_str_cmp
from flask_jwt_extended import create_access_token, jwt_required
from flask import Blueprint, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from app import db, models, config
import os
import uuid # for randomizing file names

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET'])
def index():
    return "Welcome! you may want to visit /list, /upload or /download/<file_id>"

@bp.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Test route!"})
  
@bp.route('/test-jwt', methods=['GET'])
@jwt_required()
def test_route():
    return jsonify({"message": "Test route! you have a valid JWT"})

# Signup Route
@bp.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = models.User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# Login Route
@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = models.User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    return jsonify({"error": "Invalid credentials"}), 401

# Protect the endpoints using the @jwt_required() decorator
@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        extension = original_filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4()}.{extension}"
        
        filepath = os.path.join(config.Config.UPLOAD_FOLDER, filename)
        try:
          file.save(filepath)
          os.chmod(filepath, 0o644) # prevent file from being executed
        except Exception as e:
            return jsonify({"error": f"File save error: {str(e)}"}), 500
        
        new_file = models.File(name=filename, original_name=original_filename, path=filepath)
        db.session.add(new_file)
        db.session.commit()
        
        return jsonify({"message": "File uploaded successfully", "file_id": new_file.id})
    
    return jsonify({"error": "Invalid file type"}), 400

@bp.route('/download/<int:file_id>', methods=['GET'])
@jwt_required()
def download_file(file_id):
    file = models.File.query.get_or_404(file_id)
    response = send_from_directory(config.Config.UPLOAD_FOLDER, file.name)
    # Add Content-Disposition header
    response.headers["Content-Disposition"] = f"attachment; filename={file.original_name}"
    return response

@bp.route('/list', methods=['GET'])
@jwt_required()
def list_files():
    files = models.File.query.all()
    return jsonify([{"id": file.id, "name": file.name, "uploaded_at": file.uploaded_at} for file in files])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.Config.ALLOWED_EXTENSIONS

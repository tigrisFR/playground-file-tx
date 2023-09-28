from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Initializing extensions
    db.init_app(app)
    jwt.init_app(app)

    allowed_origins = [
        "https://tigrisfr.github.io",     # GitHub Page
    # Add any other IPs or domains as needed
    ] 

    CORS(app, resources={r"/*": {"origins": allowed_origins
    }}) # Allowing all origins for simplicity.

    # Register your blueprints 
    from . import routes
    app.register_blueprint(routes.bp)
    

    return app

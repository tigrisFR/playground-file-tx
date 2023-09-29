from p3app import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('p3app.config.Config')

    allowed_origins = [
        "https://tigrisfr.github.io",     # GitHub Page
        #"https://curious-manatee-guiding.ngrok-free.app", # ngrok tunnel to expose HTTPS 
    # Add any other IPs or domains as needed
    ] 
    CORS(app, resources={r"/*": {"origins": allowed_origins}})
    #CORS(app) # allow all origins
    
    # Initializing extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register your blueprints 
    from . import routes
    app.register_blueprint(routes.bp)
    

    return app

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from . import config

migrate = Migrate()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)

    # Sesseion 초기화
    app.config["SESSION_TYPE"] = "filesystem"
    
    migrate.init_app(app, db, render_as_batch=True)
    
    from . import models
    
    from mining.views import main_views
    
    app.register_blueprint(main_views.bp)
    
    return app
    
    
    
    
    
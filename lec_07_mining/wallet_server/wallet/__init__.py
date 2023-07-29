import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from wallet import config

mingrate = Migrate()
csrf = CSRFProtect()
db = SQLAlchemy()

# Initialize Login Manager
login_manager = LoginManager()

def create_app():
    template_folder = os.path.join(config.BASE_DIR, 'templates')
    app = Flask(__name__, template_folder=template_folder)
    app.config.from_object(config)
    login_manager.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    
    mingrate.init_app(app, db, render_as_batch=True)
    
    from . import models
    
    from wallet.views import(
        main_views,
        auth_views,
        wallet_views,
        transfer_views,
    )
    
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(wallet_views.bp)
    app.register_blueprint(transfer_views.bp)
    
    return app
    
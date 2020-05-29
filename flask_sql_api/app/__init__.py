from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()
login_manager=LoginManager()

def create_app():
    app=Flask(__name__)
    app.config.from_object('config.Config')     # Configuring app from config.py

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import routes
        from . import models
        db.create_all()

    return app

# In create_app initialize everything, register all routes, models and create them.

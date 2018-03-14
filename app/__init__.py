from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail

from config import Config

toolbar = DebugToolbarExtension()
db = MongoEngine()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    app.debug = True

    db.init_app(app)
    toolbar.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

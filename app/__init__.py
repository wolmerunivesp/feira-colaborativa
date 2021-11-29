import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv, dotenv_values

load_dotenv()

#Iniciando o SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'sqlite:///db.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'feiracolaborativa')
    
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # esse import precisa estar aqui na linha 34 antes do @login_manager.user_loader e após o  login_manager.init_app(app)
    from app.models.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #Projetando as rotas de autenticação
    from app.controllers.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #Partes sem autenticação
    from app.controllers.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

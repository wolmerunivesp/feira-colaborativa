import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

#Iniciando o SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'feira#br7-natu@za')
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'sqlite:///db.sqlite')

    # Configuração para PRODUÇÃO no Heroku
    db_driver = 'pymysql'
    db_dialect = 'mysql'
    db_user = 'b61ca611e9cd86'
    db_pass ='b9274dfc'
    db_host = 'us-cdbr-east-04.cleardb.com'
    db_name = 'heroku_46cc2957a8f111a'

    # Conexão com o BD
    app.config['SQLALCHEMY_DATABASE_URI'] = "{db_dialect}+{db_driver}://{db_user}:{db_pass}@{db_host}/{db_name}".format(db_dialect=db_dialect, db_driver=db_driver, db_user = db_user, db_pass = db_pass, db_host = db_host, db_name = db_name)
    
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

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

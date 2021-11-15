from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#Iniciando o SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    
    app.config['SECRET_KEY'] = 'feira#br7-natu@za'

    # dialect + driver: //username:password@host:port/database
    #heruko
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b61ca611e9cd86:b9274dfc@us-cdbr-east-04.cleardb.com/heroku_46cc2957a8f111a'
    #phpmyadmin
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bd_flask'
    

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
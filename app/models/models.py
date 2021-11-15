from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    telefone = db.Column(db.String(25))

class Grupo(db.Model):
    __tablename__ = 'grupo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    admin = db.Column(db.Integer, db.ForeignKey('user.id'))
    verdura = db.Column(db.Boolean, default=0)
    legume = db.Column(db.Boolean, default=0)
    fruta = db.Column(db.Boolean, default=0)
    tempero = db.Column(db.Boolean, default=0)
    semanalmente = db.Column(db.Boolean, default=0)
    quinzenalmente = db.Column(db.Boolean, default=0)
    cep = db.Column(db.String(8))
    latitude = db.Column(db.String(15))
    longitude = db.Column(db.String(15))
    whatsapp = db.Column(db.String(60))

user_grupo = db.Table(
    "user_grupo",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("grupo_id", db.Integer, db.ForeignKey("grupo.id")),
)
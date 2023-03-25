from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin



class MaterialUsado(db.Model):
    __tablename__ = 'material_usado'
    materialUsadoID = db.Column(db.Integer, primary_key=True, nullable=False)
    telaUsada = db.Column(db.String(50), nullable=False)
    cantidadTela = db.Column(db.Integer, nullable=False)
    hiloUsado = db.Column(db.Integer, nullable=False)
    cierreUsado = db.Column(db.Integer, nullable=False)


class TipoProducto(db.Model):
    __tablename__ = 'tipo_producto'
    tipoProductoID = db.Column(db.Integer, primary_key=True, nullable=False)
    nombreProducto = db.Column(db.String(50), nullable=False)
    materialUsadoID = db.Column(db.Integer, db.ForeignKey('material_usado.materialUsadoID'), nullable=False)
    material_usado = db.relationship('MaterialUsado', backref=db.backref('tipo_productos', lazy=True))
    productos = db.relationship('Productos', backref='tipo_producto', lazy=True)


class Productos(db.Model):
    __tablename__ = 'productos'
    idProducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.String(255))
    tipoProductoID = db.Column(db.Integer, db.ForeignKey('tipo_producto.tipoProductoID'), nullable=False)
    image_name = db.Column(db.String(255))
    estatus = db.Column(db.Integer, default=1)




class TipoProducto(db.Model):
    __tablename__ = 'v_tipo_producto'
    tipoProductoID = db.Column(db.Integer, primary_key=True)
    nombreProducto = db.Column(db.String(255), nullable=False)

roles_users = db.Table('roles_users',
        db.Column('userId', db.Integer(), db.ForeignKey('user.id')),
        db.Column('roleId', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime



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



class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    idrole = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime(), default=datetime.utcnow)
    idrole = db.Column(db.Integer, db.ForeignKey('role.idrole'), nullable=False)
    role = db.relationship('Role')




class MateriaPrima(db.Model):
    __tablename__ = 'materiaPrima'
    materiaPrimaId = db.Column(db.Integer(), primary_key=True)
    image_name = db.Column(db.String(255))
    nombreMateriaPrima = db.Column(db.String(255), unique=True)
    metrosMateriaPrima = db.Column(db.Integer(), unique=False)

class Compra(db.Model):
    __tablename__ = 'compras'
    idCompra = db.Column(db.Integer(), primary_key=True)
    fechaCompra = db.Column(db.DateTime(), nullable=False)
    id = db.Column(db.Integer(), nullable=False)
    subtotal = db.Column(db.Integer())
    estatus = db.Column(db.Integer(), default=1)
    detalle_compra = db.relationship('DetalleCompra', backref='compra')

class DetalleCompra(db.Model):
    __tablename__ = 'detalleCompra'
    idDetalleCompra = db.Column(db.Integer(), primary_key=True)
    idCompra = db.Column(db.Integer(), db.ForeignKey('compras.idCompra'), nullable=False)
    idProducto = db.Column(db.Integer(), db.ForeignKey('productos.idProducto'), nullable=False)
    cantidad = db.Column(db.Integer(), nullable=False)
    costo = db.Column(db.Float(), nullable=False)

class Pedidos(db.Model):
    __tablename__ = 'v_detalle_compras'
    CompraId = db.Column(db.Integer(), primary_key=True)
    fechaCompra = db.Column(db.DateTime(), nullable=False)
    UsuarioID = db.Column(db.Integer(), nullable=False)
    UsuarioNombre = db.Column(db.String(255), nullable=False)
    ProductoNombre = db.Column(db.String(255), nullable=False)
    cantidad = db.Column(db.Integer(), nullable=False)
    costo = db.Column(db.Float(), nullable=False)
    subtotal = db.Column(db.Float(), nullable=False)

class v_compras_estatus (db.Model):
    __tablename__ = 'v_compras_estatus'
    idCompra = db.Column(db.Integer, primary_key=True)
    fechaCompra = db.Column(db.DateTime, nullable=False)
    id = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    descripcionEstatus = db.Column(db.String(255), nullable=False)


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
    domicilioId = db.Column(db.Integer, db.ForeignKey('domicilio.domicilioId'), nullable=False)

class Domicilio(db.Model):
    tablename = 'domicilio'
    domicilioId = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(255), nullable=False)
    municipio = db.Column(db.String(255), nullable=False)
    codigoPostal = db.Column(db.Integer, nullable=False)
    colonia = db.Column(db.String(255), nullable=False)
    calle = db.Column(db.String(255), nullable=False)
    numeroInt = db.Column(db.Integer, nullable=True)
    numeroExt = db.Column(db.Integer, nullable=False)
    referencia = db.Column(db.String(255), nullable=False)




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
    estado = db.Column(db.String(255), nullable=False)
    municipio = db.Column(db.String(255), nullable=False)
    codigoPostal = db.Column(db.Integer, nullable=False)
    colonia = db.Column(db.String(255), nullable=False)
    calle = db.Column(db.String(255), nullable=False)
    numeroInt = db.Column(db.Integer, nullable=True)
    numeroExt = db.Column(db.Integer, nullable=False)
    referencia = db.Column(db.String(255), nullable=False)
    subtotal = db.Column(db.Integer())
    totalBotiquines = db.Column(db.Integer())
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
    idDetalleCompra = db.Column(db.Integer, primary_key=True)
    CompraId = db.Column(db.Integer)
    fechaCompra = db.Column(db.DateTime)
    UsuarioID = db.Column(db.Integer)
    UsuarioNombre = db.Column(db.String(255))
    ProductoNombre = db.Column(db.String(255))
    cantidad = db.Column(db.Integer)
    costo = db.Column(db.Float)
    subtotal = db.Column(db.Float)
    Estatus = db.Column(db.String(255))


class v_compras_estatus (db.Model):
    tablename = 'v_compras_estatus'
    idCompra = db.Column(db.Integer, primary_key=True)
    fechaCompra = db.Column(db.DateTime, nullable=False)
    id = db.Column(db.Integer, nullable=False)
    userName = db.Column(db.String(50), nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    descripcionEstatus = db.Column(db.String(255), nullable=False)
    domicilio = db.Column(db.String(255), nullable=False)

class descontarMaterial(db.Model):
    __tablename__ = 'v_detalle_compras_con_material'
    idDetalleCompra = db.Column(db.Integer, primary_key=True)
    CompraId = db.Column(db.Integer)
    fechaCompra = db.Column(db.DateTime)
    UsuarioID = db.Column(db.Integer)
    UsuarioNombre = db.Column(db.String(255))
    ProductoNombre = db.Column(db.String(255))
    tipoProductoID = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    costo = db.Column(db.Float)
    subtotal = db.Column(db.Float)
    Estatus = db.Column(db.String(255))
    materialUsadoID = db.Column(db.Integer)
    telaUsada = db.Column(db.String(255))
    cantidadTela = db.Column(db.Integer)
    hiloUsado = db.Column(db.Integer)
    cierreUsado = db.Column(db.Integer)
    carroUsado = db.Column(db.Integer)
    reflejanteUsado = db.Column(db.Integer)
    argollaUsada = db.Column(db.Integer)
    bandolaUsada = db.Column(db.Integer)
    hombreraUsada = db.Column(db.Integer)


class Proveedor(db.Model):
    __tablename__ = 'proovedores'
    proovedoresId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(250), nullable=False)
    materiaPrima = db.Column(db.String(250), nullable=False)
    costoxmetro = db.Column(db.String(250), nullable=False)
    estatus = db.Column(db.Integer(), default=1)

class CompraMateriaPrima(db.Model):
    __tablename__ = 'compraMateriaPrima'
    compraMateriaPrimaID = db.Column(db.Integer, primary_key=True)
    proovedoresId = db.Column(db.Integer, db.ForeignKey('proovedores.proovedoresId'), nullable=False)
    cantidadEnMetros = db.Column(db.Integer, nullable=False)
    pagoTotal = db.Column(db.Integer, nullable=False)
    confirmed_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())


class v_user_con_domicilio(db.Model):
    __tablename__ = 'v_user_con_domicilio'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(255), nullable=False)
    municipio = db.Column(db.String(255), nullable=False)
    codigoPostal = db.Column(db.Integer, nullable=False)
    colonia = db.Column(db.String(255), nullable=False)
    calle = db.Column(db.String(255), nullable=False)
    numeroExt = db.Column(db.Integer, nullable=False)
    numeroInt = db.Column(db.Integer)
    referencia = db.Column(db.String(255), nullable=False)

class v_user_con_domicilio_role(db.Model):
    __tablename__ = 'v_usuario_con_domicilio'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True)
    role_name = db.Column(db.String(255), nullable=False)
    domicilio = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    








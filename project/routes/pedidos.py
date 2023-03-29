import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify,Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user, roles_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from ..models import Productos, TipoProducto, Compra, Pedidos,DetalleCompra, v_compras_estatus
from .. import db
import os
from os.path import abspath, dirname, join
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime
from collections import defaultdict

pedidos = Blueprint('pedidos', __name__, url_prefix='/pedidos')

@pedidos.route('/verPedidos')
@login_required
@roles_required('Admin')
def verPedidos():
    detalles = v_compras_estatus.query.all()
    return render_template('/pedidos/verPedidos.html', detalles=detalles)

# @pedidos.route('/verPedidos')
# @login_required
# @roles_required('Admin', 'Empleado','Cliente')
# def verPedidos():
#     if current_user.has_role('Admin', 'Empleado'):
#         # Obtener todos los pedidos
#         pedidos = Pedidos.query.all()
#     if current_user.has_role('Cliente'):
#         # Obtener solo los pedidos del usuario actual
#         pedidos = Pedidos.query.filter_by(usuario_id=current_user.id).all()

#     return render_template('/pedidos/verPedidos.html', pedidos=pedidos)

@pedidos.route('/crear_pedido', methods=['GET', 'POST'])
@login_required
def crear_pedido():
    data = request.get_json()
    if data:
        productos = data.get("productos")
        subtotal = data.get("subtotal")
        if productos and subtotal:
            compra = Compra(fechaCompra=datetime.now(), id=current_user.id, subtotal=subtotal)
            db.session.add(compra)
            for producto in productos:
                producto_id = int(producto["id"])
                cantidad = int(producto["cantidad"])
                producto = Productos.query.get(producto_id)
                detalle = DetalleCompra(
                    idCompra=compra.idCompra,
                    idProducto=producto_id,
                    cantidad=cantidad,
                    costo=producto.precio
                )
                db.session.add(detalle)
            db.session.commit()
            return jsonify({'Estatus': 'ok', 'mensaje': 'Pedido agregado con éxito'})
    return jsonify({'Estatus': 'no', 'mensaje': 'Error al crear el pedido'})





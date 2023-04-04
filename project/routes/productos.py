import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user, roles_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from ..models import Productos, TipoProducto
from .. import db
import os
from os.path import abspath, dirname, join
from werkzeug.utils import secure_filename
from pathlib import Path

productos = Blueprint('productos', __name__, url_prefix='/productos')

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler = logging.FileHandler('app.log')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

@productos.route('/galeria')
@login_required
def galeria():
    productos = Productos.query.filter_by(estatus=1).all()
    # logger.info('Galeria de productos vista por el usuario: %s', current_user.name)
    return render_template('/productos/galeria.html', productos=productos)

@productos.route('/listaProductos')
@login_required
def listaProductos():
    if (current_user.idrole == 1 or current_user.idrole == 2):
        productos = Productos.query.filter_by(estatus=1).all()
        productos2 = Productos.query.filter_by(estatus=2).all()
        return render_template('/productos/listaProductos.html', productos1=productos, productos2=productos2)
    else:
        flash('No tiene permisos para acceder a esta vista.')
        return redirect(url_for('main.profile'))

@productos.route('/addProducto')
@login_required
def addProducto():
    if (current_user.idrole == 1 or current_user.idrole == 2):
        tipos = TipoProducto.query.all()
        return render_template('/productos/addProductos.html', tipos=tipos)
    else:
        flash('No tiene permisos para acceder a esta vista.')
        return redirect(url_for('main.profile'))



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@productos.route('/addProducto', methods=['POST'])
@login_required
def addProducto_post():
    if (current_user.idrole == 1 or current_user.idrole == 2):
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        tipo_producto_id = request.form.get('tipo_producto')
        file = request.files['file']
        upload_path = os.path.join(current_app.static_folder, 'img', 'productos')
        if 'file' not in request.files:
            # logger.warning('No se ha seleccionado ningún archivo al agregar un producto')
            flash('No se ha seleccionado ningún archivo.')
            return redirect(request.url)
        if file.filename == '':
            # logger.warning('No se ha seleccionado un archivo al agregar un producto')
            flash('No se ha seleccionado ningún archivo.')
            return redirect(request.url)
        if not allowed_file(file.filename):
            # logger.warning('El formato del archivo no es válido al agregar un producto')
            flash('Este archivo no es válido. Los formatos permitidos son: {}'.format(', '.join(ALLOWED_EXTENSIONS)))
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            file.save(os.path.join(upload_path, file_name))
            producto = Productos(nombre=nombre, precio=precio, image_name=file_name, tipoProductoID=tipo_producto_id)
            db.session.add(producto)
            db.session.commit()
            # logger.info('El producto %s ha sido agregado exitosamente', nombre)
            flash('Producto agregado exitosamente.')
        return redirect(url_for('productos.listaProductos'))
    else:
            flash('No tiene permisos para acceder a esta vista.')
            return redirect(url_for('main.profile'))



@productos.route('/updateProducto/<id>', methods=['POST','GET'])
@login_required
def updateProducto(id):
    if (current_user.idrole == 1 or current_user.idrole == 2):
        tipos = TipoProducto.query.all()
        producto = Productos.query.get(id)
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            precio = request.form.get('precio')
            tipo_producto_id = request.form.get('tipo_producto')
            upload_path = os.path.join(current_app.static_folder, 'img', 'productos')
            if 'file' not in request.files:
                # logger.warning('No se ha seleccionado ningún archivo al agregar un producto')
                flash('No se ha seleccionado ningún archivo.')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                # logger.warning('No se ha seleccionado un archivo al agregar un producto')
                flash('No se ha seleccionado un archivo.')
                return redirect(request.url)
            if not allowed_file(file.filename):
                # logger.warning('El formato del archivo no es válido al agregar un producto')
                flash('Este archivo no es válido. Los formatos permitidos son: {}'.format(', '.join(ALLOWED_EXTENSIONS)))
                return redirect(request.url)
            if file and allowed_file(file.filename):
                file_name = secure_filename(file.filename)
                file.save(os.path.join(upload_path, file_name))
                producto.nombre = nombre
                producto.precio = precio
                producto.image_name = file_name
                producto.tipoProductoID = tipo_producto_id
                db.session.commit()
                # logger.info('El producto %s ha sido agregado exitosamente', nombre)
                flash('Producto Editado exitosamente.')
                return redirect(url_for('productos.listaProductos'))
        
        return render_template('/productos/updateProductos.html', producto=producto,tipos=tipos)
    else:
        flash('No tiene permisos para acceder a esta vista.')
        return redirect(url_for('main.profile'))

@productos.route('/deleteProducto/<id>')
@login_required
def deleteProducto(id):
    if (current_user.idrole == 1 or current_user.idrole == 2):
        producto = Productos.query.get(id)
        producto.estatus = 2
        db.session.commit()
        # logger.info('El producto se ha desactivado exitosamente.')
        flash('Producto desactivado exitosamente.')
        return redirect(url_for('productos.listaProductos'))
    else:
        flash('No tiene permisos para acceder a esta vista.')
        return redirect(url_for('main.profile'))

@productos.route('/activeProducto/<id>')
@login_required
def activeProducto(id):
    if (current_user.idrole == 1 or current_user.idrole == 2):
        producto = Productos.query.get(id)
        producto.estatus = 1
        db.session.commit()
        # logger.info('El producto se ha desactivado exitosamente.')
        flash('Producto activado exitosamente.')
        return redirect(url_for('productos.listaProductos'))
    else:
        flash('No tiene permisos para acceder a esta vista.')
        return redirect(url_for('main.profile'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
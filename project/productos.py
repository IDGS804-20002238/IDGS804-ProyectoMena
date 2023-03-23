from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user, roles_required
from flask import current_app
from flask import jsonify
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from . models import Productos
from . import db
import os
from os.path import abspath, dirname, join
from werkzeug.utils import secure_filename
from pathlib import Path

productos = Blueprint('productos', __name__, url_prefix='/productos')

@productos.route('/galeria')
@login_required
def galeria():
    productos = Productos.query.all()
    return render_template('/productos/galeria.html', productos=productos)

@productos.route('/listaProductos')
@login_required
@roles_required('Admin')
def listaProductos():
    productos = Productos.query.filter_by(estatus=1).all()
    productos2 = Productos.query.filter_by(estatus=2).all() # filtrar productos con estatus=1
    return render_template('/productos/listaProductos.html', productos1=productos, productos2=productos2)

@productos.route('/addProducto')
@login_required
@roles_required('Admin')
def addProducto():
    return render_template('/productos/addProductos.html')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# ruta para agregar productos
@productos.route('/addProducto', methods=['POST'])
@login_required
@roles_required('Admin')
def addProducto_post():
    nombre = request.form.get('nombre')
    precio = request.form.get('precio')
    file = request.files['file']
    base_path = os.path.abspath(os.path.dirname(__file__))
    upload_path = os.path.join(base_path, 'static/img/productos/')
    if 'file' not in request.files:
        flash('No se ha seleccionado ningún archivo.')
        return redirect(request.url)
    if file.filename == '':
        flash('No se ha seleccionado un archivo.')
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash('Este archivo no es válido. Los formatos permitidos son: {}'.format(', '.join(ALLOWED_EXTENSIONS)))
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        file.save(os.path.join(upload_path, file_name))
        producto = Productos(nombre=nombre, precio=precio, image_name=file_name)
        db.session.add(producto)
        db.session.commit()
        flash('Producto agregado exitosamente.')
    return redirect(url_for('productos.listaProductos'))






@productos.route('/updateProducto/<id>', methods=['POST','GET'])
@login_required
@roles_required('Admin')
def updateProducto(id):
    producto = Productos.query.get(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        base_path = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(base_path, 'static/img/productos/')
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            file.save(os.path.join(upload_path, file_name))
            producto.nombre = nombre
            producto.precio = precio
            producto.image_name = file_name
            db.session.commit()
            flash('Producto Editado exitosamente.')
            return redirect(url_for('productos.listaProductos'))
    
    return render_template('/productos/updateProductos.html', producto=producto)

@productos.route('/deleteProducto/<id>')
@login_required
@roles_required('Admin')
def deleteProducto(id):
    producto = Productos.query.get(id)
    producto.estatus = 2
    db.session.commit()
    flash('Producto desactivado exitosamente.')
    return redirect(url_for('productos.listaProductos'))

@productos.route('/activeProducto/<id>')
@login_required
@roles_required('Admin')
def activeProducto(id):
    producto = Productos.query.get(id)
    producto.estatus = 1
    db.session.commit()
    flash('Producto activado exitosamente.')
    return redirect(url_for('productos.listaProductos'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
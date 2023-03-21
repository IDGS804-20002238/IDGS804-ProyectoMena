from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user, roles_required
from flask import current_app
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
    productos = Productos.query.all()
    return render_template('/productos/listaProductos.html', productos=productos)

@productos.route('/addProducto')
@login_required
@roles_required('Admin')
def addProducto():
    return render_template('/productos/addProductos.html')


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@productos.route('/addProducto', methods=['POST'])
@login_required
@roles_required('Admin')
def addProducto_post():
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
        producto = Productos(nombre=nombre, precio=precio, image_name=file_name)
        db.session.add(producto)
        db.session.commit()
        return redirect(url_for('productos.listaProductos'))
    
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
            return redirect(url_for('productos.listaProductos'))
    
    return render_template('/productos/updateProductos.html', producto=producto)

@productos.route('/deleteProducto/<id>')
@login_required
@roles_required('Admin')
def deleteProducto(id):
    producto = Productos.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('productos.listaProductos'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
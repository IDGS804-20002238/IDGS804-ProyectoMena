import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user, roles_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from ..models import Productos, TipoProducto,MateriaPrima
from .. import db
import os
from os.path import abspath, dirname, join
from werkzeug.utils import secure_filename
from pathlib import Path

materiaPrima = Blueprint('materiaPrima', __name__, url_prefix='/materiaPrima')

@materiaPrima.route('/galeriaMateriaPrima')
@login_required
def galeriaMateriaPrima():
    materiaPrima = MateriaPrima.query.all()
    # logger.info('Galeria de productos vista por el usuario: %s', current_user.name)
    return render_template('/Materia_Prima/materia_prima.html', materiaPrima=materiaPrima)
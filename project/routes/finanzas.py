import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify,Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user, roles_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from ..models import v_gastos,Compra,v_finanzas
from .. import db
import os
from os.path import abspath, dirname, join
from werkzeug.utils import secure_filename
from pathlib import Path
from werkzeug.security import check_password_hash


finanzas = Blueprint('finanzas', __name__, url_prefix='/finanzas')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

@finanzas.route('/getFinanzas')
@login_required
def getFinanzas():
    if (current_user.idrole == 1):
        logger.info('finanzas vista por el usuario: %s', current_user.name)
        ingresos =     Compra.query.filter_by(estatus=4).all()
        gastos = v_gastos.query.all()
        ganancias = v_finanzas.query.all()
        return render_template('/Finanzas/finanzas.html', ingresos=ingresos, gastos=gastos, ganancias=ganancias)
    else:
        flash('No tiene permisos para acceder a esta vista.')
        logger.info('error de permisos, no puede ingresar debido a su rol, nombre del usuario que intentó ingresar: %s', current_user.name)
        return redirect(url_for('main.profile'))
import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify,Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user, roles_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from ..models import MateriaPrima,Proveedor, CompraMateriaPrima
from .. import db
import os
from os.path import abspath, dirname, join
from werkzeug.utils import secure_filename
from pathlib import Path

materiaPrima = Blueprint('materiaPrima', __name__, url_prefix='/materiaPrima')

@materiaPrima.route('/galeriaMateriaPrima')
@login_required
def galeriaMateriaPrima():
    if (current_user.idrole == 1 or current_user.idrole == 2):
        materiaPrima = MateriaPrima.query.all()
        # logger.info('Galeria de productos vista por el usuario: %s', current_user.name)
        return render_template('/Materia_Prima/materia_prima.html', materiaPrima=materiaPrima)
    else:
            flash('No tiene permisos para acceder a esta vista.')
            return redirect(url_for('main.profile'))

@materiaPrima.route('/Proovedores')
@login_required
def proovedores():
    if (current_user.idrole == 1):
        proovedores = Proveedor.query.filter(Proveedor.estatus == 1)
        return render_template('/Materia_Prima/proovedores.html', proovedores=proovedores)
    else:
        flash('No tiene permisos para acceder a esta vista.')
        return redirect(url_for('main.profile'))


@materiaPrima.route('/guardar_proovedor', methods=['GET', 'POST'])
@login_required
def guardar_proovedor():
    if (current_user.idrole == 1):
         nombre = request.get_json()['nombre']
         costoxmetro = request.get_json()['costoxmetro']
         materiaPrima = request.get_json()['materiaPrima']
         proveedor = Proveedor(nombre=nombre, costoxmetro=costoxmetro, materiaPrima=materiaPrima)
    
         db.session.add(proveedor)
         db.session.commit()
         return jsonify({'status': 'succes', 'message': 'Exito'})   
    else:
        flash('No tiene permisos para acceder a esta vista.')
        return redirect(url_for('main.profile'))     

@materiaPrima.route('/actualizar_proveedor', methods=['GET', 'POST'])
@login_required
def actualzar_proovedor():
    if (current_user.idrole == 1):
        proovedoresId = request.get_json()['proovedoresId']
        proveedor = Proveedor.query.filter_by(proovedoresId=proovedoresId).first()
        
        if proveedor is None:
            return jsonify({"error": "Proveedor no encontrado"})
        
        datos_proveedor = {
            "proveedor_id": proveedor.proovedoresId,
            "nombre": proveedor.nombre,
            "materiaPrima": proveedor.materiaPrima,
            "costoxmetro":proveedor.costoxmetro
        }
        
        return jsonify(datos_proveedor)
    else:
        flash('No tiene permisos para acceder a esta vista.')
        return redirect(url_for('main.profile'))    


     
@materiaPrima.route('/editar_proovedor', methods=['GET', 'POST'])
@login_required
def editar_proovedor():
    if (current_user.idrole == 1):
         nombre = request.get_json()['nombre']
         costoxmetro = request.get_json()['costoxmetro']
         materiaPrima = request.get_json()['materiaPrima']
         proovedoresId = request.get_json()['proovedoresId']
         proveedor = Proveedor.query.filter_by(proovedoresId=proovedoresId).first()

    if proveedor is not None:
        proveedor.nombre = nombre
        proveedor.costoxmetro = costoxmetro
        proveedor.materiaPrima = materiaPrima
        db.session.commit()
        return jsonify({'status': 'succes', 'message': 'Exito'}) 
    else:
            flash('No tiene permisos para acceder a esta vista.')
            return redirect(url_for('main.profile'))    
    
@materiaPrima.route('/comprar_materiaPrima', methods=['GET', 'POST'])
@login_required
def comprar_materiaPrima():
    if (current_user.idrole == 1):
        proovedoresId = request.get_json()['proovedoresId']
        cantidadEnMetros = request.get_json()['cantidadEnMetros']
        pagoTotal = request.get_json()['pagoTotal']
        nombreMateriaPrima = request.get_json()['nombreMateriaPrima']

        # Actualiza la tabla CompraMateriaPrima
        compra = CompraMateriaPrima(proovedoresId=proovedoresId, cantidadEnMetros=cantidadEnMetros, pagoTotal=pagoTotal)
        db.session.add(compra)
        
        # Actualiza la tabla MateriaPrima
        materia_prima = MateriaPrima.query.filter_by(nombreMateriaPrima=nombreMateriaPrima).first()
        materia_prima.metrosMateriaPrima += int(cantidadEnMetros)


        # Confirma la transacción
        db.session.commit()
        return jsonify({'status': 'succes', 'message': 'Exito'})
    else:
            flash('No tiene permisos para acceder a esta vista.')
            return redirect(url_for('main.profile'))  

@materiaPrima.route('/eliminar_proovedor', methods=['GET', 'POST'])
@login_required
def eliminar_proovedor():
    if (current_user.idrole == 1):
        proovedoresId = request.get_json()['proovedoresId']
        proovedor = Proveedor.query.get(proovedoresId)

        proovedor.estatus = 2 # Cambiar estatus a "eliminado"
        db.session.commit()
        return jsonify({'status': 'succes', 'message': 'Exito'})
    else:
        flash('No tiene permisos para acceder a esta vista.')
        return redirect(url_for('main.profile'))



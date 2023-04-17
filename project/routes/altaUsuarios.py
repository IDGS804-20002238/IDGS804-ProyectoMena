import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify,Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user, roles_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from ..models import User, Domicilio,v_user_con_domicilio_role,v_user_con_domicilio
from .. import db
import os
from os.path import abspath, dirname, join
from werkzeug.utils import secure_filename
from pathlib import Path
from werkzeug.security import check_password_hash


altaUsuarios = Blueprint('altaUsuarios', __name__, url_prefix='/altaUsuarios')

@altaUsuarios.route('/createUsers')
@login_required
def createUsers():
    if (current_user.idrole == 1):
        # logger.info('Galeria de productos vista por el usuario: %s', current_user.name)
        usuario =     v_user_con_domicilio_role.query.filter_by(active=1).filter(v_user_con_domicilio_role.role_name.in_(['Empleado', 'Repartidor', 'Cliente'])).all()
        usuario2 = v_user_con_domicilio_role.query.filter_by(active=0).all()
        return render_template('/Usuarios/altaUsuarios.html', usuario=usuario, usuario2=usuario2)
    else:
            flash('No tiene permisos para acceder a esta vista.')
            return redirect(url_for('main.profile'))
    
@altaUsuarios.route('/eliminar_user', methods=['GET', 'POST'])
@login_required
def eliminar_user():
    if (current_user.idrole == 1):
        id = request.get_json()['id']
        user = User.query.filter_by(id=id).first()
        user.active = False
        db.session.commit()
        return jsonify({'success': 'Usuario actualizado correctamente'})
    else:
            flash('No tiene permisos para acceder a esta vista.')
            return redirect(url_for('main.profile'))
    
@altaUsuarios.route('/activar_user', methods=['GET', 'POST'])
@login_required
def activar_user():
    if (current_user.idrole == 1):
        id = request.get_json()['id']
        user = User.query.filter_by(id=id).first()
        user.active = 1
        db.session.commit()
        return jsonify({'success': 'Usuario actualizado correctamente'})
    else:
            flash('No tiene permisos para acceder a esta vista.')
            return redirect(url_for('main.profile'))



@altaUsuarios.route('/registerUsuario', methods=['GET', 'POST'])
def register_post():
    email = request.get_json()['email']
    name = request.get_json()['name']
    password = request.get_json()['password']
    estatus = request.get_json()['estatus']

    user = User.query.filter_by(email=email).first()

    if user:
        response = {'status': 'error', 'message': 'el correo ya existe'}
        return jsonify(response)
    
    # obtiene los datos del form para llenar la tabla domicilio
    estado = request.get_json()['estado']
    municipio = request.get_json()['municipio']
    codigoPostal = request.get_json()['codigoPostal']
    colonia = request.get_json()['colonia']
    calle = request.get_json()['calle']
    numeroInt = request.get_json()['numeroInt']
    numeroExt = request.get_json()['numeroExt']
    referencia = request.get_json()['referencia']

    #inserta el domicilio
    domicilio = Domicilio(estado=estado, municipio=municipio, codigoPostal=codigoPostal, colonia=colonia, calle=calle, numeroInt=numeroInt, numeroExt=numeroExt, referencia=referencia)
    db.session.add(domicilio)
    db.session.commit()

    # obtiene el id del domicilio recién insertado
    domicilio_id = domicilio.domicilioId

    # crea un nuevo objeto User y agrega el id del domicilio a la columna domicilioId
    new_user = User(name=name, email=email, password=generate_password_hash(password, method='sha256'), idrole=estatus, domicilioId=domicilio_id)
    db.session.add(new_user)
    db.session.commit()

    response = {'status': 'success', 'message': 'La compra se ha actualizado correctamente'}
    return jsonify(response)

@altaUsuarios.route('/update_usuario', methods=['GET', 'POST'])
def update_usuario():
    id = request.get_json()['id']
    email = request.get_json()['email']
    name = request.get_json()['name']
    password = request.get_json()['password']
    estatus = request.get_json()['estatus']

    user = User.query.filter_by(id=id).first()

    if not user:
        response = {'status': 'error', 'message': 'Usuario no encontrado'}
        return jsonify(response)

    if user.email != email:
        # Verifica si el correo ya existe en la base de datos
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            response = {'status': 'error', 'message': 'el correo ya existe'}
            return jsonify(response)

        # obtiene los datos del form para actualizar la tabla domicilio
        estado = request.get_json()['estado']
        municipio = request.get_json()['municipio']
        codigoPostal = request.get_json()['codigoPostal']
        colonia = request.get_json()['colonia']
        calle = request.get_json()['calle']
        numeroInt = request.get_json()['numeroInt']
        numeroExt = request.get_json()['numeroExt']
        referencia = request.get_json()['referencia']

        domicilio = Domicilio.query.filter_by(domicilioId=user.id).first()
        domicilio.estado = estado
        domicilio.municipio = municipio
        domicilio.codigoPostal = codigoPostal
        domicilio.colonia = colonia
        domicilio.calle = calle
        domicilio.numeroInt = numeroInt
        domicilio.numeroExt = numeroExt
        domicilio.referencia = referencia

        # actualiza el objeto User
        user.name = name
        user.email = email
        user.password = generate_password_hash(password, method='sha256')
        user.idrole = estatus

        # confirma los cambios en la base de datos
        db.session.commit()

        response = {'status': 'success', 'message': 'El usuario se ha actualizado correctamente'}
        return jsonify(response)
    
    # Si el correo no ha cambiado, se actualiza solo la información del usuario
    user.name = name
    user.password = generate_password_hash(password, method='sha256')
    user.idrole = estatus

    # confirma los cambios en la base de datos
    db.session.commit()

    response = {'status': 'success', 'message': 'El usuario se ha actualizado correctamente'}
    return jsonify(response)




@altaUsuarios.route('/actualizar_user', methods=['GET', 'POST'])
@login_required
def actualizar_user():
    if (current_user.idrole == 1):
        id = request.get_json()['id']
        user = v_user_con_domicilio.query.filter_by(id=id).first()

        user_dict ={
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'estado': user.estado,
            'municipio': user.municipio,
            'codigoPostal': user.codigoPostal,
            'colonia': user.colonia,
            'calle': user.calle,
            'numeroExt': user.numeroExt,
            'numeroInt': user.numeroInt,
            'referencia': user.referencia,
        }
        

        return jsonify(user_dict)
    else:
        flash('No tiene permisos para acceder a esta vista.')
        return redirect(url_for('main.profile'))




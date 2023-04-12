import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify,Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user, roles_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from ..models import Productos, v_user_con_domicilio, Compra, Pedidos,DetalleCompra, v_compras_estatus,descontarMaterial,MateriaPrima
from ..import db
from os.path import abspath, dirname, join
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime
from sqlalchemy import text, func



pedidos = Blueprint('pedidos', __name__, url_prefix='/pedidos')

@pedidos.route('/verPedidos')
@login_required
def verPedidos():
    if (current_user.idrole == 1 or current_user.idrole == 2):
        detalles = v_compras_estatus.query.all()
        return render_template('/pedidos/verPedidos.html', detalles=detalles)
    if (current_user.idrole == 3):
        detalles = v_compras_estatus.query.filter(v_compras_estatus.descripcionEstatus == 'PEDIDO ENVIADO').all()
        return render_template('/pedidos/verPedidos.html', detalles=detalles)
    if current_user.idrole == 4:
        detalles = v_compras_estatus.query.filter_by(id=current_user.id).all()
        return render_template('/pedidos/verPedidos.html', detalles=detalles)
    else:
        flash('No tiene permisos para acceder a esta vista.')
        return redirect(url_for('main.profile'))
    
@pedidos.route('/crear_pedido', methods=['GET', 'POST'])
@login_required
def crear_pedido():
    if (current_user.idrole == 1 or current_user.idrole == 2 or current_user.idrole == 4):
        data = request.get_json()
        if data:
            productos = data.get("productos")
            subtotal = data.get("subtotal")
            estado = data.get("estado")
            municipio = data.get("municipio")
            codigoPostal = data.get("codigoPostal")
            colonia = data.get("colonia")
            calle = data.get("calle")
            numeroExt = data.get("numeroExt")
            numeroInt = data.get("numeroInt")
            referencia = data.get("referencia")
            totalBotiquines = data.get("totalBotiquines")
            if productos and subtotal:
                compra = Compra(fechaCompra=datetime.now(), id=current_user.id, subtotal=subtotal,estado=estado,municipio=municipio,codigoPostal=codigoPostal,colonia=colonia,calle=calle,numeroExt=numeroExt,numeroInt=numeroInt,referencia=referencia,totalBotiquines=totalBotiquines)
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
    else:
        flash('No tiene permisos para acceder a esta vista.')
        return redirect(url_for('main.profile'))

@pedidos.route('/cancelar_pedido', methods=['GET', 'POST'])
@login_required
def cancelar_pedido():
    if (current_user.idrole == 1 or current_user.idrole == 2 or current_user.idrole == 4):
            idCompra = request.get_json()['idCompra']
            compra = Compra.query.filter_by(idCompra=idCompra).first()
            if compra is None:
                return jsonify({'status': 'error', 'message': 'La compra no existe.'})
            else:
                db.session.execute(text('UPDATE compras SET estatus = :estatus WHERE idCompra = :id'), {'estatus': '5', 'id': idCompra})
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'El pedido ha sido cancelado.'})
    else:
        flash('No tiene permisos para acceder a esta vista.')
        return redirect(url_for('main.profile'))


    
@pedidos.route('/ver_detalle/<int:idPedido>')
@login_required
def ver_detalle(idPedido):
    if (current_user.idrole == 1 or current_user.idrole == 2 or current_user.idrole == 4):
        detalle = Pedidos.query.filter(Pedidos.CompraId == idPedido).all()
        return render_template('/pedidos/detallePedido.html', pedido=detalle)
    else:
        flash('No tiene permisos para acceder a esta vista.')
        return redirect(url_for('main.profile'))





@pedidos.route('/actualizar_compra', methods=['GET', 'POST'])
@login_required
def actualizar_compra():
    idCompra = request.get_json()['idCompra']
    compras = descontarMaterial.query.filter_by(CompraId=idCompra).all()

    for compra in compras:
        materialUsadoID = compra.materialUsadoID
        telaUsada = compra.telaUsada
        cantidadTela = compra.cantidadTela
        hiloUsado = compra.hiloUsado
        cierreUsado = compra.cierreUsado
        carroUsado = compra.carroUsado
        reflejanteUsado = compra.reflejanteUsado
        argollaUsada = compra.argollaUsada
        bandolaUsada = compra.bandolaUsada
        hombreraUsada = compra.hombreraUsada
        # Descontar la tela utilizada
        materiales = MateriaPrima.query.filter_by(nombreMateriaPrima=telaUsada).all()
        for material in materiales:
            if material.metrosMateriaPrima >= cantidadTela:
                material.metrosMateriaPrima -= cantidadTela
                db.session.commit()
            else:
                # Si no hay suficiente materia prima, enviar un error
                return jsonify({'status': 'error', 'message': 'No hay suficiente tela para completar la compra'})

        # Descontar el hilo utilizado
        hilo = MateriaPrima.query.filter_by(nombreMateriaPrima='Hilo').first()
        if hilo.metrosMateriaPrima >= hiloUsado:
            hilo.metrosMateriaPrima -= hiloUsado
            db.session.commit()
        else:
            # Si no hay suficiente materia prima, enviar un error
            return jsonify({'status': 'error', 'message': 'No hay suficiente hilo para completar la compra'})

        # Descontar el cierre utilizado
        cierre = MateriaPrima.query.filter_by(nombreMateriaPrima='Cierre').first()
        if cierre.metrosMateriaPrima >= cierreUsado:
            cierre.metrosMateriaPrima -= cierreUsado
            db.session.commit()
        else:
            # Si no hay suficiente materia prima, enviar un error
            return jsonify({'status': 'error', 'message': 'No hay suficiente cierre para completar la compra'})
        ##-----
        # Descontar el Carros utilizados
        Carros = MateriaPrima.query.filter_by(nombreMateriaPrima='Carros').first()
        if Carros.metrosMateriaPrima >= carroUsado:
            Carros.metrosMateriaPrima -= carroUsado
            db.session.commit()
        else:
            # Si no hay suficiente materia prima, enviar un error
            return jsonify({'status': 'error', 'message': 'No hay suficientes Carros para completar la compra'})
        
        # Descontar el Argollas utilizados
        Argollas = MateriaPrima.query.filter_by(nombreMateriaPrima='Argollas').first()
        if Argollas.metrosMateriaPrima >= argollaUsada:
            Argollas.metrosMateriaPrima -= argollaUsada
            db.session.commit()
        else:
            # Si no hay suficiente materia prima, enviar un error
            return jsonify({'status': 'error', 'message': 'No hay suficientes Argollas para completar la compra'})
        
        # Descontar el Reflejante utilizado
        Reflejante = MateriaPrima.query.filter_by(nombreMateriaPrima='Reflejante').first()
        if Reflejante.metrosMateriaPrima >= reflejanteUsado:
            Reflejante.metrosMateriaPrima -= reflejanteUsado
            db.session.commit()
        else:
            # Si no hay suficiente materia prima, enviar un error
            return jsonify({'status': 'error', 'message': 'No hay suficiente Reflejante para completar la compra'})
        
        # Descontar la Bandola utilizado
        Bandola = MateriaPrima.query.filter_by(nombreMateriaPrima='Bandola').first()
        if Bandola.metrosMateriaPrima >= bandolaUsada:
            Bandola.metrosMateriaPrima -= bandolaUsada
            db.session.commit()
        else:
            # Si no hay suficiente materia prima, enviar un error
            return jsonify({'status': 'error', 'message': 'No hay suficiente Bandola para completar la compra'})
        
        # Descontar la Bandola utilizado
        Hombrera = MateriaPrima.query.filter_by(nombreMateriaPrima='Hombrera').first()
        if Hombrera.metrosMateriaPrima >= hombreraUsada:
            Hombrera.metrosMateriaPrima -= hombreraUsada
            db.session.commit()
        else:
            # Si no hay suficiente materia prima, enviar un error
            return jsonify({'status': 'error', 'message': 'No hay suficientes Hombreras para completar la compra'})
   
    # Actualizar la compra con el nuevo estatus
    compra = Compra.query.get(idCompra)
    compra.estatus = 2
    db.session.commit()
    return jsonify({'status': 'succes', 'message': 'La compra se ha actualizado correctamente'})   

@pedidos.route('/enviarPedido', methods=['GET', 'POST'])
@login_required
def enviarPedido():
    idCompra = request.get_json()['idCompra']
    # Actualizar la compra con el nuevo estatus
    compra = Compra.query.get(idCompra)
    compra.estatus = 3
    db.session.commit()
    return jsonify({'status': 'succes', 'message': 'La compra se ha actualizado correctamente'})

@pedidos.route('/entregarPedido', methods=['GET', 'POST'])
@login_required
def entregarPedido():
    idCompra = request.get_json()['idCompra']
    # Actualizar la compra con el nuevo estatus
    compra = Compra.query.get(idCompra)
    compra.estatus = 4
    db.session.commit()
    return jsonify({'status': 'succes', 'message': 'La compra se ha actualizado correctamente'})

@pedidos.route('/obtener_domicilio', methods=['GET', 'POST'])
@login_required
def obtener_domicilio():
    user_id = current_user.get_id()
    user_details = v_user_con_domicilio.query.filter_by(id=user_id).first()
    
    # Obtener la suma de totalBotiquines donde estatus=1
    total_botiquines = db.session.query(func.sum(Compra.totalBotiquines)).filter_by(estatus=1).scalar()
    
    domicilio_dict ={
        'estado': user_details.estado,
        'municipio': user_details.municipio,
        'codigoPostal': user_details.codigoPostal,
        'colonia': user_details.colonia,
        'calle': user_details.calle,
        'numeroExt': user_details.numeroExt,
        'numeroInt': user_details.numeroInt,
        'referencia': user_details.referencia,
        'totalBotiquines': total_botiquines
    }
    return jsonify(domicilio_dict)










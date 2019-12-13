#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 20:11:09 2019

Clase que representa el microservicio REST por el que acceder a los datos de las
mascotas de la clase "Mascotas".

@author: Lidia Sánchez Mérida
"""
from flask import Flask, Response
from celery import Celery
import json
from mascotas_celery import descargar_mascotas
import mascotas

"""Configuramos Flask para que pueda conectarse con el microservicio de celery"""
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
"""Iniciamos el servidor de Celery acorde a la configuración anterior de Flask."""
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

"""Objeto que nos conecta con la clase Mascotas."""
m = mascotas.Mascotas()

@app.route("/")
def index():
    return Response("Microservicio REST para recopilar datos de mascotas.", status=200)

@app.route("/obtener_mascotas", methods=['GET'])
def obtener_mascotas():
    """Servicio REST para obtener los datos de todas las mascotas descargados
        por el microservicio de Celery.
        Si hay datos de mascotas los devuelve en formato diccionario.
        Si no devuelve el código 404 NOT FOUND.
    """
    mascotas = descargar_mascotas.apply()
    #mascotas = resultado.wait()
    if (type(mascotas.result) == dict and mascotas.status == 'SUCCESS'): 
        return Response(json.dumps(mascotas.result), status=200, mimetype="application/json")
    else: return Response("Aún no existen datos de mascotas.", status=404)

@app.route("/obtener_una_mascota/<int:id_mascota>", methods=['GET'])
def obtener_una_mascota(id_mascota):
    """Servicio REST que obtiene los datos de una mascota determinada. Para ello
        será necesario aportar un identificador válido.
        Si el ID de la mascota es correcto devolverá un diccionario con los datos
        de la mascota en cuestión.
        Si no devuelve el código 404 NOT FOUND.
    """
    mascotas = descargar_mascotas.apply()
    resultado = m.obtener_una_mascota(id_mascota, mascotas.result)
    if (type(resultado) == dict): 
        return Response(json.dumps(resultado), status=200, mimetype="application/json")
    else:
        return Response("No existe ninguna mascota con el identificador especificado.", status=404)
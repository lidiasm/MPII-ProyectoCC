#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase que representa el microservicio REST por el que acceder a los datos de las
mascotas de la clase "Mascotas".

@author: Lidia Sánchez Mérida
"""
from flask import Flask, Response
from flask_caching import Cache
import json
import mascotas
import sys
sys.path.append("src")
from excepciones import EmptyCollection, WrongPetIndex
import os
import mongodb

"""Configuramos Flask para que pueda conectarse con el microservicio de celery"""
app = Flask(__name__)
"""Añadimos caché para comprobar si mejoran las prestaciones."""
app.config["CACHE_DEFAULT_TIMEOUT"] = 36000
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

"""Creamos un objeto de la base de datos y lo configuramos."""
bd = mongodb.MongoDB(os.environ.get("MONGODB_URI"), 'PetfinderBD', 'mascotas')
"""Objeto que nos conecta con la clase Mascotas."""
m = mascotas.Mascotas(bd)

@app.route("/")
def index():
    return Response("Microservicio REST para recopilar datos de mascotas.", status=200)

@app.route("/obtener_mascotas", methods=['GET'])
@cache.cached()
def obtener_mascotas():
    """Servicio REST que obtiene los datos de todas las mascotas que préviamente
        han sido descargados por el microservicio periódico de Celery. Para ello
        accede a la base de datos mongodb, que es donde se almacenan dichos datos
        como caché y los devuelve, si estos existen, en formato JSON.
        Si no devuelve el código 404 NOT FOUND.
    """
    try:
        mascotas = m.obtener_mascotas()
        return Response(json.dumps(mascotas), status=200, mimetype="application/json")
    except EmptyCollection:
        return Response("REST: No existen datos de mascotas aún.", status=400)
#    try:
#        tarea = descargar_mascotas.apply_async()
#        mascotas = tarea.get()
#        if (mascotas == None):
#            return Response("No existen datos de mascotas aún. Espere....", status=200)
#        else:
#            return Response(json.dumps(mascotas), status=200, mimetype="application/json")
#    except MaxPetfinderRequestsExceeded: 
#        return Response("Gunicorn: Número de peticiones máximo excedido.", status=400)

@app.route("/obtener_una_mascota/<string:id_mascota>", methods=['GET'])
@cache.cached()
def obtener_una_mascota(id_mascota):
    """Servicio REST que obtiene los datos de una mascota determinada. Para ello
        será necesario aportar un identificador válido.
        Si el ID de la mascota es correcto devolverá un diccionario con los datos
        de la mascota en cuestión obtenido desde la base de datos que funciona como caché.
        Si no devuelve el código 404 NOT FOUND.
    """
    try:
        mascota = m.obtener_una_mascota(id_mascota)
        return Response(json.dumps(mascota), status=200, mimetype="application/json")
    except EmptyCollection:
        return Response("REST: No se han recopilado datos de mascotas aún.", status=400)
    except WrongPetIndex:
        return Response("REST: No existe una mascota con el índice especificado.", status=404)
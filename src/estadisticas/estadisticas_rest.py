#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servicios RESTs con los que visualizar los tres tipos de informes estadísticos
generados por el microservicio en Celery.

@author: Lidia Sánchez Mérida
"""
from flask import Flask, Response
from flask_caching import Cache
import json
import estadisticas
import sys
sys.path.append("src")
from excepciones import ItemNotFound

import os
import mongodb

app = Flask(__name__)
app.config["CACHE_DEFAULT_TIMEOUT"] = 36000
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

"""Creamos un objeto de la base de datos y lo configuramos."""
bd = mongodb.MongoDB(os.environ.get("MONGODB_URI"), 'PetfinderBD', 'estadisticas')
"""Objeto que nos conecta con la clase Estadisticas."""
estd = estadisticas.Estadisticas(bd)

@app.route("/")
def index():
    return Response("Microservicio REST para visualizar estadísticas de mascotas.", status=200)

@app.route("/ver_estadistica_ninios", methods=['GET'])
@cache.cached()
def ver_estadistica_ninios():
    """Servicio REST que obtiene y muestra el informe estadístico acerca de la
        relación entre las mascotas descargadas y los niños.
        Si aún no se ha generado devuelve el código 404 NOT FOUND.
    """
    try:
        estd_ninios = estd.obtener_estadistica_ninios()
        return Response(json.dumps(estd_ninios), status=200, mimetype="application/json")
    except ItemNotFound:
        return Response("REST estadísticas: Aún no se ha generado dicho informe.", status=400)

@app.route("/ver_estadistica_tipos_mascotas", methods=['GET'])
@cache.cached()
def ver_estadistica_tipos_mascotas():
    """Servicio REST que obtiene y muestra el informe estadístico acerca del número
        de ejemplares de cada mascota adoptable.
        Si aún no se ha generado devuelve el código 404 NOT FOUND.
    """
    try:
        estd_tipos_mascotas = estd.obtener_estadistica_tipos_mascotas()
        return Response(json.dumps(estd_tipos_mascotas), status=200, mimetype="application/json")
    except ItemNotFound:
        return Response("REST estadísticas: Aún no se ha generado dicho informe.", status=400)

@app.route("/ver_estadistica_razas_perro", methods=['GET'])
@cache.cached()
def ver_estadistica_razas_perro():
    """Servicio REST que obtiene y muestra el informe estadístico acerca de la
        sociabilidad de cada una de las razas de perro registradas.
        Si aún no se ha generado devuelve el código 404 NOT FOUND.
    """
    try:
        estd_razas_perro = estd.obtener_estadistica_razas_perro()
        return Response(json.dumps(estd_razas_perro), status=200, mimetype="application/json")
    except ItemNotFound:
        return Response("REST estadísticas: Aún no se ha generado dicho informe.", status=400)

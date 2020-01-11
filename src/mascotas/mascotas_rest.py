#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase que representa el microservicio REST por el que acceder a los datos de las
mascotas de la clase "Mascotas".

@author: Lidia Sánchez Mérida
"""
from flask import Flask, Response, request
from flask_caching import Cache
import json
import mascotas
import sys
sys.path.append("src")
from excepciones import EmptyCollection, WrongPetIndex, WrongNumberSearchParameters, WrongSearchParametersValues, PetsNotFound, MaxPetfinderRequestsExceeded

import os
import mongodb

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
    
@app.route("/buscar_mascotas", methods=['GET'])
def buscar_mascotas():
    """Servicio REST con el que buscar mascotas en función de una serie de parámetros
    configurables por el usuario."""
    try:
        terminos_busqueda = request.args
        tipo_animal = edad = genero = tamanio = ninios = gatos = perros = ''
        """Comprobamos los parámetros que se han pasado en la URL"""
        if ('tipo_animal' in terminos_busqueda): tipo_animal = terminos_busqueda['tipo_animal']
        if ('edad' in terminos_busqueda): edad = terminos_busqueda['edad']
        if ('genero' in terminos_busqueda): genero = terminos_busqueda['genero']
        if ('tamanio' in terminos_busqueda): tamanio = terminos_busqueda['tamanio']
        if ('ninios' in terminos_busqueda): ninios = terminos_busqueda['ninios']
        if ('gatos' in terminos_busqueda): gatos = terminos_busqueda['gatos']
        if ('perros' in terminos_busqueda): perros = terminos_busqueda['perros']

        """Preparamos el diccionario con la búsqueda."""
        parametros = {'tipo_animal':tipo_animal, 'edad':edad, 'genero':genero,
              'tamanio':tamanio, 'ninios':ninios, 'gatos':gatos, 'perros':perros}
        mascotas_coincidentes = m.buscar(parametros)
        return Response(json.dumps(mascotas_coincidentes), status=200, mimetype="application/json")
    
    except WrongNumberSearchParameters:
        return Response("Número de parámetros de búsqueda incorrecto.", status=400)
    except WrongSearchParametersValues:
        return Response("Al menos un parámetro de búsqueda debe tener un valor.", status=400)
    except PetsNotFound:
        return Response("No existen mascotas sobre las que realizar la búsqueda.", status=428)
    except TypeError:
        return Response("Los valores de los parámetros no son válidos.", status=400)
    except MaxPetfinderRequestsExceeded: 
        return Response("Número de peticiones máximo excedido.", status=412)

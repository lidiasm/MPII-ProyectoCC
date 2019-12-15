#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase que representa el microservicio asociado a la clase Búsqueda. A través
de él podremos realizar una búsqueda de mascotas basada en preferencias.

@author: Lidia Sánchez Mérida
"""

from flask import Flask, Response, request
from celery import Celery
import json
import sys
sys.path.append("../")
from excepciones import WrongNumberSearchParameters, WrongSearchParametersValues, PetsNotFound, MaxPetfinderRequestsExceeded
sys.path.append("../mascotas")
sys.path.append("src/mascotas")
from mascotas_celery import descargar_mascotas
sys.path.append("src/busqueda")
import busqueda

"""Configuramos Flask para que pueda conectarse con el microservicio de Celery
que obtiene los datos de la API Petfinder."""
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
"""Iniciamos el servidor de Celery acorde a la configuración anterior de Flask."""
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

"""Objeto que nos conecta con la clase Busqueda."""
b = busqueda.Busqueda()

@app.route("/")
def index():
    return Response("Microservicio REST para buscar mascotas en base a preferencias.", status=200)

@app.route("/buscar_mascotas", methods=['GET'])
def buscar_mascotas():
    """Servicio REST con el que buscar mascotas en función de una serie de parámetros
    configurables por el usuario."""
    try:
        mascotas = descargar_mascotas.apply()
        if (type(mascotas.result) == dict):
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
    
            """Ajustamos los valores de todos los parámetros de la búsqueda."""
            parametros = {'tipo_animal':tipo_animal, 'edad':edad, 'genero':genero,
                  'tamanio':tamanio, 'ninios':ninios, 'gatos':gatos, 'perros':perros}
            mascotas_coincidentes = b.buscar(mascotas.result, parametros)
            return Response(json.dumps(mascotas_coincidentes), status=200, mimetype="application/json")
        else: 
            return Response("Número de peticiones máximo excedido.", status=412)
    except WrongNumberSearchParameters:
        return Response("Número de parámetros de búsqueda incorrecto.", status=400)
    except WrongSearchParametersValues:
        return Response("Al menos un parámetro de búsqueda debe tener un valor.", status=400)
    except PetsNotFound:
        return Response("No existen mascotas sobre las que realizar la búsqueda.", status=412)
    except TypeError:
        return Response("Los valores de los parámetros no son válidos.", status=400)
    except MaxPetfinderRequestsExceeded: 
        return Response("Número de peticiones máximo excedido.", status=412)

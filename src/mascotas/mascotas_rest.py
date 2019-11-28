#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 20:11:09 2019

Clase que representa el microservicio REST por el que acceder a los datos de las
mascotas de la clase "Mascotas".

@author: Lidia Sánchez Mérida
"""
from flask import Flask, Response
import mascotas
import json

app = Flask(__name__)
m = mascotas.Mascotas()

@app.route("/")
def index():
    return Response("Microservicio para recopilar datos de mascotas.", status=200)

@app.route("/obtener_mascotas", methods=['GET'])
def obtener_mascotas():
    """Servicio REST para obtener los datos de todas las mascotas.
        Si hay datos de mascotas los devuelve en formato diccionario.
        Si no devuelve el código 404 NOT FOUND.
    """
    resultado = m.obtener_datos()
    if (type(resultado) == dict): return Response(json.dumps(resultado),
        status=200, mimetype="application/json")
    else: return Response("Aún no existen datos de mascotas.", status=404)

@app.route("/obtener_una_mascota/<int:id_mascota>", methods=['GET'])
def obtener_mascota(id_mascota):
    """ Servicio REST para obtener los datos de una mascota determinada en función
    de su ID.
        Si el ID de la mascota es correcto devolverá un diccionario con los datos
        de la mascota en cuestión.
        Si no devuelve el código 404 NOT FOUND.
    """
    resultado = m.obtener_datos_mascota(id_mascota)
    if (type(resultado) == str): return Response("No existe una mascota con el ID especificado.", status=404)
    elif (type(resultado) == dict): return Response(json.dumps(resultado),
          status=200, mimetype="application/json")

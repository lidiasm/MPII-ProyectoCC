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

@app.route("/obtener_mascotas", methods=['GET'])
def obtener_mascotas():
    """Servicio REST para obtener los datos de todas las mascotas.
        Si hay datos de mascotas los devuelve en formato diccionario.
        Si no devuelve el código 400 BAD REQUEST.
    """
    n_mascotas = m.get_n_mascotas()
    if (n_mascotas > 0):
        return Response(json.dumps(m.obtener_datos()), status=200, mimetype="application/json")
    else:
        return Response(status=400)

@app.route("/obtener_una_mascota/<int:id_mascota>", methods=['GET'])
def obtener_mascota(id_mascota):
    """ Servicio REST para obtener los datos de una mascota determinada en función
    de su ID.
        Si el ID de la mascota es correcto devolverá un diccionario con los datos
        de la mascota en cuestión.
        Si no devuelve el código 404 NOT FOUND.
    """
    if (id_mascota == None or type(id_mascota) != int or (id_mascota in m.mascotas) == False):
        return Response(status=404)
    else:
        return Response(json.dumps(m.obtener_datos_mascota(id_mascota)), status=200, mimetype="application/json")

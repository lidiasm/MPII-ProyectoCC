#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 11:47:11 2019

Clase que contiene los datos de todas las mascotas disponibles en la API Petfinder.

@author: Lidia Sánchez Mérida
"""

from celery import Celery
app = Celery('mascotas', broker='pyamqp://guest@localhost//')
#from .celery import app

class Mascotas:
    
    # Prueba para Celery
    @app.task
    def add(x, y):
        return x + y
    
    # Constructor
    def __init__(self):
        self.mascotas = []
    
    def comprobar_variable(self, variable, tipo):
        if (variable == None or isinstance(variable, tipo) == False): return True
        return False
    
    # Analiza y añade los datos de una nueva mascota al vector de mascotas.
    # Los datos que no sean válidos se sustituirán por 'DNV' (Dato No Válido).
    def aniadir_nueva_mascota(self, nueva_mascota):
        datos_no_validos = 0
        check_nombre = self.comprobar_variable(nueva_mascota.nombre, str)
        if (check_nombre) :
            nueva_mascota.nombre = "DNV"
            datos_no_validos += 1
        check_tipo_animal = self.comprobar_variable(nueva_mascota.tipo_animal, str)
        if (check_tipo_animal) :
            nueva_mascota.tipo_animal = "DNV"
            datos_no_validos += 1
        check_raza = self.comprobar_variable(nueva_mascota.raza, str)
        if (check_raza) :
            nueva_mascota.raza = "DNV"
            datos_no_validos += 1
        check_tamanio = self.comprobar_variable(nueva_mascota.tamanio, str)
        if (check_tamanio) :
            nueva_mascota.tamanio = "DNV"
            datos_no_validos += 1
        check_genero = self.comprobar_variable(nueva_mascota.genero, str)
        if (check_genero) :
            nueva_mascota.genero = "DNV"
            datos_no_validos += 1
        check_edad = self.comprobar_variable(nueva_mascota.edad, str)
        if (check_edad) :
            nueva_mascota.edad = "DNV"
            datos_no_validos += 1
        check_raza = self.comprobar_variable(nueva_mascota.raza, str)
        if (check_raza) :
            nueva_mascota.raza = "DNV"
            datos_no_validos += 1
        check_tipo_pelaje = self.comprobar_variable(nueva_mascota.tipo_pelaje, str)
        if (check_tipo_pelaje) :
            nueva_mascota.tipo_pelaje = "DNV"
            datos_no_validos += 1
        check_estado = self.comprobar_variable(nueva_mascota.estado, str)
        if (check_estado) :
            nueva_mascota.estado = "DNV"
            datos_no_validos += 1
        check_bueno_con_ninios = self.comprobar_variable(nueva_mascota.bueno_con_ninios, bool)
        if (check_bueno_con_ninios) :
            nueva_mascota.bueno_con_ninios = "DNV"
            datos_no_validos += 1
        check_bueno_con_gatos = self.comprobar_variable(nueva_mascota.bueno_con_gatos, bool)
        if (check_bueno_con_gatos) :
            nueva_mascota.bueno_con_gatos = "DNV"
            datos_no_validos += 1
        check_bueno_con_perros = self.comprobar_variable(nueva_mascota.bueno_con_perros, bool)
        if (check_bueno_con_perros) :
            nueva_mascota.bueno_con_perros = "DNV"
            datos_no_validos += 1
        check_ciudad = self.comprobar_variable(nueva_mascota.ciudad, str)
        if (check_ciudad) :
            nueva_mascota.ciudad = "DNV"
            datos_no_validos += 1
        check_pais = self.comprobar_variable(nueva_mascota.pais, str)
        if (check_pais) :
            nueva_mascota.pais = "DNV"
            datos_no_validos += 1
        # Añadimos la nueva mascota con sus datos originales o modificados
        self.mascotas.append(nueva_mascota)
        if (datos_no_validos > 0): return "Algunos datos de la mascota no son válidos."
        return "Nueva mascota añadida correctamente."
    
    # Conecta con la API Petfinder proporcionándole las credenciales.
    def conectar_APIPetfinder(self, api_key, api_secret):
        if (api_key == None or isinstance(api_key, str) == False or
            api_secret == None or isinstance(api_secret, str) == False):
            return "Credenciales no válidas."
        
        self.api_key = api_key
        self.api_secret = api_secret
        # Conectamos con la API
        return "Credenciales correctas."
        
    # Devuelve el objeto de la mascota que esté referenciada por el índice
    # suministrado, si este fuese válido.
    def obtener_datos_mascota(self, n_mascota):
        if n_mascota == None or isinstance(n_mascota, int) == False or n_mascota >= len(self.mascotas):
            return "Número de mascota inválido."
        # Devolvemos los datos de la mascota requerida
        return self.mascotas[n_mascota]
        
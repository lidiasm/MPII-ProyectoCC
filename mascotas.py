#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 11:47:11 2019

Clase que contiene los datos de todas las mascotas disponibles en la API Petfinder.

@author: Lidia Sánchez Mérida
"""

class Mascotas:
    
    # Constructor
    def __init__(self):
        self.mascotas = []
    
    # Analiza y añade los datos de una nueva mascota al vector de mascotas.
    # Los datos que no sean válidos se sustituirán por 'DNV' (Dato No Válido).
    def aniadir_nueva_mascota(self, nueva_mascota):
        datos_no_validos = 0
        if (nueva_mascota.nombre == None or isinstance(nueva_mascota.nombre, str) == False): 
            datos_no_validos += 1
            nueva_mascota.nombre = "DNV" 
        if (nueva_mascota.tipo_animal == None or isinstance(nueva_mascota.tipo_animal, str) == False):
            datos_no_validos += 1
            nueva_mascota.tipo_animal = "DNV" 
        if (nueva_mascota.raza == None or isinstance(nueva_mascota.raza, str) == False):
            datos_no_validos+=1
            nueva_mascota.raza = "DNV"
        if (nueva_mascota.tamanio == None or isinstance(nueva_mascota.tamanio, str) == False): 
            datos_no_validos+=1
            nueva_mascota.tamanio = "DNV" 
        if (nueva_mascota.genero == None or isinstance(nueva_mascota.genero, str) == False): 
            datos_no_validos+=1
            nueva_mascota.genero = "DNV" 
        if (nueva_mascota.edad == None or isinstance(nueva_mascota.edad, str) == False):
            datos_no_validos+=1
            nueva_mascota.edad = "DNV"
        if (nueva_mascota.tipo_pelaje == None or isinstance(nueva_mascota.tipo_pelaje, str) == False): 
            datos_no_validos+=1
            nueva_mascota.tipo_pelaje = "DNV" 
        if (nueva_mascota.estado == None or isinstance(nueva_mascota.estado, str) == False):
            datos_no_validos+=1
            nueva_mascota.estado = "DNV"
        if (nueva_mascota.bueno_con_ninios == None or isinstance(nueva_mascota.bueno_con_ninios, bool) == False):
            datos_no_validos+=1
            nueva_mascota.bueno_con_ninios = "DNV"
        if (nueva_mascota.bueno_con_gatos == None or isinstance(nueva_mascota.bueno_con_gatos, bool) == False):
            datos_no_validos+=1
            nueva_mascota.bueno_con_gatos = "DNV"
        if (nueva_mascota.bueno_con_perros == None or isinstance(nueva_mascota.bueno_con_perros, bool) == False):
            datos_no_validos+=1
            nueva_mascota.bueno_con_perros = "DNV"
        if (nueva_mascota.ciudad == None or isinstance(nueva_mascota.ciudad, str) == False): 
            datos_no_validos += 1
            nueva_mascota.ciudad = "DNV" 
        if (nueva_mascota.pais == None or isinstance(nueva_mascota.pais, str) == False): 
            datos_no_validos += 1
            nueva_mascota.pais = "DNV" 
        
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
        
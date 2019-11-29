#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 11:47:11 2019

Clase que contiene los datos de todas las mascotas disponibles en la API Petfinder.

@author: Lidia Sánchez Mérida
"""
import petpy
import ficha_mascota

class Mascotas:
    
    ID = 0
    """ Los datos de las mascotas son comunes a todos los objetos de la clase."""
    mascotas = {}  
    """ Conexión con la API Petfinder"""
    api_petifinder = None
    
    def comprobar_variable(self, variable, tipo):
        """Comprueba el tipo y el valor de una variable."""
        if (variable == None or isinstance(variable, tipo) == False): return True
        return False
    
    def aniadir_nueva_mascota(self, nueva_mascota):
        """Analiza y añade los datos de una nueva mascota al vector de mascotas.
            Los datos que no sean válidos se sustituirán por 'DNV' (Dato No Válido)."""
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
        
        (Mascotas.mascotas)[Mascotas.ID] = {
                'nombre':nueva_mascota.nombre,
                'tipo_animal':nueva_mascota.tipo_animal,
                'raza':nueva_mascota.raza,
                'tamanio':nueva_mascota.tamanio,
                'genero':nueva_mascota.genero,
                'edad':nueva_mascota.edad,
                'tipo_pelaje':nueva_mascota.tipo_pelaje,
                'estado':nueva_mascota.estado,
                'ninios':nueva_mascota.bueno_con_ninios,
                'perros':nueva_mascota.bueno_con_perros,
                'gatos':nueva_mascota.bueno_con_gatos,
                'ciudad':nueva_mascota.ciudad,
                'pais':nueva_mascota.pais
        }
        Mascotas.ID += 1
        if (datos_no_validos > 0): return "Algunos datos de la mascota no son válidos."
        return "Nueva mascota añadida correctamente."
    
    def conectar_APIPetfinder(self, api_key, api_secret):
        """Conecta con la API Petfinder"""
        if (api_key == None or isinstance(api_key, str) == False or
            api_secret == None or isinstance(api_secret, str) == False):
            return "Credenciales no válidas."
        
        self.api_key = api_key
        self.api_secret = api_secret
        """Conectamos con la API Petfinder"""
        try:
            Mascotas.api_petifinder = petpy.Petfinder(self.api_key, self.api_secret)
            return "Conexión realizada correctamente."
        except petpy.exceptions.PetfinderInvalidCredentials:
            return "Credenciales no válidas."
    
    def descargar_datos_mascotas(self):
        """Obtenemos los 20 primeros animales."""
        if (Mascotas.api_petifinder == None):
            return "Error. Primero debe conectarse a la API Petfinder."
        else:
            animales = Mascotas.api_petifinder.animals()
            for animal in animales['animals']:
                nueva_mascota = ficha_mascota.FichaMascota(animal['name'], animal['type'], 
                   animal['breeds']['primary'], animal['size'], animal['gender'], animal['age'],
                   animal['coat'], animal['status'], animal['environment']['children'], 
                   animal['environment']['cats'], animal['environment']['dogs'], 
                   animal['contact']['address']['city'], animal['contact']['address']['country'])
                self.aniadir_nueva_mascota(nueva_mascota)
                
            return animales
        
    def obtener_datos_mascota(self, n_mascota):
        """Devuelve los datos de una mascota en particular si el id es válido.
            Si no devuelve un mensaje informando de que el identificador no es válido."""
        if n_mascota == None or type(n_mascota) != int or (n_mascota in Mascotas.mascotas) == False:
            return "Identificador de mascota inválido."

        return Mascotas.mascotas[n_mascota]
    
    def obtener_mascotas(self):
        """Obtiene el diccionario con los datos de todas las mascotas, si existen datos.
            Si no devuelve un mensaje informativo."""
        if (self.get_n_mascotas() > 0): return Mascotas.mascotas
        else: return "No existen datos de mascotas."
    
    def get_n_mascotas(self):
        """Obtiene el número de mascotas del diccionario."""
        return len(Mascotas.mascotas)
    
    def borrar_datos(self):
        """Borra todos los datos de las mascotas."""
        Mascotas.mascotas = {}
        Mascotas.ID = 0

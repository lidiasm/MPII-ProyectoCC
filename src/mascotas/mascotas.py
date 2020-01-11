#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase que contiene los datos de todas las mascotas disponibles en la API Petfinder.

@author: Lidia Sánchez Mérida
"""
import sys
sys.path.append("src")
from conexion_api_petfinder import ConexionAPIPetfinder
from excepciones import MaxPetfinderRequestsExceeded, WrongPetIndex, EmptyCollection, WrongNumberSearchParameters, WrongSearchParametersValues, PetsNotFound

class Mascotas:
    
    def __init__(self, mongodb):
        """Constructor. En él se genera una variable de instancia en la que 
            se almacena la conexión con la API Petfinder.
            Añadimos inyección de dependencias para trabajar con la base de datos."""
        self.api_petfinder = ConexionAPIPetfinder.conectarConPetfinder()
        self.mongodb = mongodb
    
    def variable_correcta(self, variable, tipo):
        """Comprueba el tipo y el valor de una variable."""
        return (variable != None and isinstance(variable, tipo) == True)
    
    def aniadir_nueva_mascota(self, nueva_mascota):
        """Analiza los datos recibidos de una mascota en particular para comprobar
            si existen datos no válidos. En tal caso se sustituirán por el valor 'DNV'.
            Posteriormente se creará un diccionario con solo los datos 
            interesantes para el proyecto y se devolverá como resultado."""
        datos_no_validos = 0
        check_nombre = self.variable_correcta(nueva_mascota['nombre'], str)
        if not (check_nombre) :
            nueva_mascota['nombre'] = "DNV"
            datos_no_validos += 1
        check_tipo_animal = self.variable_correcta(nueva_mascota['tipo_animal'], str)
        if not (check_tipo_animal) :
            nueva_mascota['tipo_animal'] = "DNV"
            datos_no_validos += 1
        check_raza = self.variable_correcta(nueva_mascota['raza'], str)
        if not (check_raza) :
            nueva_mascota['raza'] = "DNV"
            datos_no_validos += 1
        check_tamanio = self.variable_correcta(nueva_mascota['tamanio'], str)
        if not (check_tamanio) :
            nueva_mascota['tamanio'] = "DNV"
            datos_no_validos += 1
        check_genero = self.variable_correcta(nueva_mascota['genero'], str)
        if not (check_genero) :
            nueva_mascota['genero'] = "DNV"
            datos_no_validos += 1
        check_edad = self.variable_correcta(nueva_mascota['edad'], str)
        if not (check_edad) :
            nueva_mascota['edad'] = "DNV"
            datos_no_validos += 1
        check_tipo_pelaje = self.variable_correcta(nueva_mascota['tipo_pelaje'], str)
        if not (check_tipo_pelaje) :
            nueva_mascota['tipo_pelaje'] = "DNV"
            datos_no_validos += 1
        check_estado = self.variable_correcta(nueva_mascota['estado'], str)
        if not (check_estado) :
            nueva_mascota['estado'] = "DNV"
            datos_no_validos += 1
        check_bueno_con_ninios = self.variable_correcta(nueva_mascota['ninios'], bool)
        if not (check_bueno_con_ninios) :
            nueva_mascota['ninios'] = "DNV"
            datos_no_validos += 1
        else:
            """Normalizamos todos los valores a cadena."""
            nueva_mascota['ninios'] = 'No'
            if (nueva_mascota['ninios']): nueva_mascota['ninios'] = 'Yes'
        check_bueno_con_gatos = self.variable_correcta(nueva_mascota['gatos'], bool)
        if not (check_bueno_con_gatos) :
            nueva_mascota['gatos'] = "DNV"
            datos_no_validos += 1
        else:
            """Normalizamos todos los valores a cadena."""
            nueva_mascota['gatos'] = 'No'
            if (nueva_mascota['gatos']): nueva_mascota['gatos'] = 'Yes'
        check_bueno_con_perros = self.variable_correcta(nueva_mascota['perros'], bool)
        if not (check_bueno_con_perros) :
            nueva_mascota['perros'] = "DNV"
            datos_no_validos += 1
        else:
            """Normalizamos todos los valores a cadena."""
            nueva_mascota['perros'] = 'No'
            if (nueva_mascota['perros']): nueva_mascota['perros'] = 'Yes'
        check_ciudad = self.variable_correcta(nueva_mascota['ciudad'], str)
        if not (check_ciudad) :
            nueva_mascota['ciudad'] = "DNV"
            datos_no_validos += 1
        check_pais = self.variable_correcta(nueva_mascota['pais'], str)
        if not (check_pais) :
            nueva_mascota['pais'] = "DNV"
            datos_no_validos += 1
        
        """Añadimos la nueva mascota a la base de datos si no existía préviamente."""
        self.mongodb.insertar_elemento(nueva_mascota)
        
        return nueva_mascota

    def descargar_datos_mascotas(self):
        """Método que descarga datos de hasta veinte mascotas. Posteriormente
            examina los valores que son relevantes para el proyecto y si contiene
            valores no válidos se sustituye por 'DNV'."""
        if (self.api_petfinder == None): 
            raise MaxPetfinderRequestsExceeded("No hay conexión con la API Petfinder.")
        else:
            id_mascota_validada = 0
            mascotas_validadas = {}
            try:
                mascotas = (self.api_petfinder).animals()
            except RuntimeError:
                raise MaxPetfinderRequestsExceeded("Número de peticiones máximo excedido.")
                
            for mascota in mascotas['animals']:
                nueva_mascota = {
                        'id':str(mascota['id']),
                        'nombre': mascota['name'], 
                        'tipo_animal': mascota['type'], 
                        'raza': mascota['breeds']['primary'], 
                        'tamanio': mascota['size'], 
                        'genero': mascota['gender'], 
                        'edad': mascota['age'],
                        'tipo_pelaje': mascota['coat'], 
                        'estado': mascota['status'], 
                        'ninios': mascota['environment']['children'], 
                        'gatos': mascota['environment']['cats'], 
                        'perros': mascota['environment']['dogs'], 
                        'ciudad': mascota['contact']['address']['city'], 
                        'pais': mascota['contact']['address']['country']
                   }
                mascota_validada = self.aniadir_nueva_mascota(nueva_mascota)
                """Devolvemos las mascotas con los datos validados."""
                mascotas_validadas[id_mascota_validada] = mascota_validada
                id_mascota_validada += 1
                
            return mascotas_validadas
    
    def obtener_una_mascota(self, identificador):
        """Método que devuelve los datos de una mascota concreta especificando,
            para ello, su identificador válido. Si existen mascotas en la base de
            datos y encuentra la mascota en particular, devuelve sus datos."""
        if (self.mongodb.tam_coleccion() == 0): 
            raise EmptyCollection('No existen datos de mascotas.')
            
        if identificador == None:
            raise WrongPetIndex("No existe ninguna mascota con el identificador especificado.")
        
        """Recuperamos los datos de la mascota en cuestión si existe."""
        mascota = self.mongodb.get_elemento('id', identificador)
        if (mascota == None): raise WrongPetIndex("No existe ninguna mascota con el identificador especificado.")
        return mascota
    
    def obtener_mascotas(self):
        """Método que devuelve los datos de todas las mascotas."""
        mascotas = self.mongodb.get_coleccion()
        if (mascotas == None): raise EmptyCollection('No existen datos de mascotas.')
        return mascotas
    
    def comparar_variables_busqueda(self, variable1, variable2):
        """Método para comparar el valor de dos cadenas. Si la segunda cadena está
            vacía se devuelve verdadero para no interferir en la búsqueda."""
        if (variable2 == ""): return True
        elif (type(variable1) != type(variable2)): raise TypeError('Los tipos de las variables '
           'deben ser iguales')
        return variable1 == variable2
    
    def buscar(self, terminos_busqueda):
        """Método para buscar las mascotas que coincidan con los términos de
            búsqueda establecidos pasados como un diccionario."""
            
        """Comprobamos los términos de consulta."""
        if (len(terminos_busqueda) != 7): 
            raise WrongNumberSearchParameters('Deben existir los siete términos de búsqueda.')
        tiene_valor = False
        if (terminos_busqueda['tipo_animal'] != ""): tiene_valor = True
        elif (terminos_busqueda['edad'] != ""): tiene_valor = True
        elif (terminos_busqueda['genero'] != ""): tiene_valor = True
        elif (terminos_busqueda['tamanio'] != ""): tiene_valor = True
        elif (terminos_busqueda['ninios'] != ""): tiene_valor = True
        elif (terminos_busqueda['gatos'] != ""): tiene_valor = True
        elif (terminos_busqueda['perros'] != ""): tiene_valor = True
        if (tiene_valor == False):
            raise WrongSearchParametersValues('Debe existir al menos un término de búsqueda con un valor.') 
        
        """Comprobamos que existen mascotas."""
        mascotas = self.obtener_mascotas()
        if (len(mascotas) == 0 or type(mascotas) != dict): 
            raise PetsNotFound('No hay mascotas sobre las que realizar la búsqueda.')
            
        """Búsqueda de mascotas."""
        resultado = {}
        ID = 0
        for id_mascota in mascotas:
            check_tipo_animal = self.comparar_variables_busqueda(mascotas[id_mascota]['tipo_animal'].lower(), 
               terminos_busqueda['tipo_animal'].lower())
            check_edad = self.comparar_variables_busqueda(mascotas[id_mascota]['edad'].lower(), 
               terminos_busqueda['edad'].lower())
            check_genero = self.comparar_variables_busqueda(mascotas[id_mascota]['genero'].lower(),
                terminos_busqueda['genero'].lower())
            check_tam = self.comparar_variables_busqueda(mascotas[id_mascota]['tamanio'].lower(),
             terminos_busqueda['tamanio'].lower())
            check_ninios = self.comparar_variables_busqueda(mascotas[id_mascota]['ninios'], 
                terminos_busqueda['ninios'])
            check_gatos = self.comparar_variables_busqueda(mascotas[id_mascota]['gatos'],
               terminos_busqueda['gatos'])
            check_perros = self.comparar_variables_busqueda(mascotas[id_mascota]['perros'],
                terminos_busqueda['perros'])

            if (check_tipo_animal and check_edad and check_genero and check_tam
                and check_ninios and check_gatos and check_perros):
                resultado[ID] = mascotas[id_mascota]
                ID = ID +1
        
        return resultado

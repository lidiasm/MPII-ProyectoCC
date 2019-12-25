#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase encargada de realizar las operaciones necesarias con la base de datos
establecida para el proyecto. Esta clase será común a todas las operaciones
de las clases de la lógica de la aplicación.

@author: Lidia Sánchez Mérida.
"""
import pymongo
import sys
sys.path.append('src/excepciones')
from excepciones import CollectionNotFound, NewItemNotFound, ItemNotFound, EmptyCollection

class MongoDB:
    
    def __init__(self, uri, bd, coleccion):
        """Crea un cliente para la base de datos MongoDB con la uri pasada por
            parámetro y crea una instancia de la base de datos especificada también
            como argumento obteniendo además la colección concretada."""
        self.cliente = pymongo.MongoClient(uri)
        self.coleccion = self.cliente[bd][coleccion]
    
    def insertar_elemento(self, elemento):
        """Comprobamos la conexión a la base de datos y el elemento a insertar."""
        if (self.coleccion == None or self.cliente == None):
            raise CollectionNotFound('No se ha realizado la conexión con la base de datos.')
        if (elemento == None or len(elemento) == 0): 
            raise NewItemNotFound('No existe el elemento a insertar.')
        """Inserta un nuevo elemento en la base de datos y colección actual siempre
            y cuando no se encuentre ya insertado."""
        if (self.get_elemento('id', elemento['id']) == None):
            id_nueva_mascota = self.coleccion.insert_one(elemento.copy()).inserted_id
            return str(id_nueva_mascota)
            
    def get_elemento(self, clave, valor):
        """Comprobamos la conexión a la base de datos."""
        if (self.coleccion == None or self.cliente == None):
            raise CollectionNotFound('No se ha realizado la conexión con la base de datos.')
        """Devuelve un elemento basándose en una pareja clave-valor. Por lo general
            la clave se corresponderá con un identificador."""
        elemento = self.coleccion.find_one({clave:valor})
        """Convertimos el id asignado por mongo en una cadena para que el servicio
            REST pueda devolver los datos en formato JSON."""
        if (elemento != None): elemento['_id'] = str(elemento['_id'])
        return elemento
    
    def get_coleccion(self):
        """Comprobamos la conexión a la base de datos."""
        if (self.coleccion == None or self.cliente == None):
            raise CollectionNotFound('No se ha realizado la conexión con la base de datos.')
        """Devuelve un cursor para recorrer los registros devueltos."""
        registros_coleccion = {}
        indice_registro = 0
        elementos = (self.coleccion).find({})
        for elemento in elementos:
            """Convertimos el id asignado por mongo en una cadena para que el servicio
                REST pueda devolver los datos en formato JSON."""
            elemento['_id'] = str(elemento['_id'])
            registros_coleccion[indice_registro] = elemento
            indice_registro += 1

        if (len(registros_coleccion) == 0): raise EmptyCollection('La colección actual está vacía')
        return registros_coleccion
    
    def eliminar_elemento(self, clave, valor):
        """Comprobamos la conexión a la base de datos."""
        if (self.coleccion == None or self.cliente == None):
            raise CollectionNotFound('No se ha realizado la conexión con la base de datos.')
        
        """Eliminamos el elemento."""
        resultado = self.coleccion.delete_one({clave:valor})
        if (resultado.deleted_count == 0): raise ItemNotFound('No existe ningún elemento con la clave-valor especificados')
        return resultado
    
    def vaciar_coleccion(self):
        """Comprobamos la conexión a la base de datos."""
        if (self.coleccion == None or self.cliente == None):
            raise CollectionNotFound('No se ha realizado la conexión con la base de datos.')
        
        """Eliminamos todos los registros de la colección."""
        resultado = self.coleccion.delete_many({})
        if (resultado.deleted_count == 0): raise EmptyCollection('La colección está vacía.')
        return resultado

    def tam_coleccion(self):
        """Devuelve el número de elementos almacenados en la colección."""
        return self.coleccion.count_documents({})
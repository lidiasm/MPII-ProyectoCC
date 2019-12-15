#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase de excepciones específicas para el proyecto en cuestión. Por defecto,
todas las clases heredarán de la clase Exception de Python y se les podrá
agregar un mensaje informativo.

@author: Lidia Sánchez Mérida.
"""

class OneInstanceConexionAPIPetfinder(Exception):
    """Clase específica para indicar que solo se puede instanciar un único objeto
    de la clase ConexionAPIPetfinder que realiza la conexión con la misma."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class ApiPetfinderConnectionError(Exception):
    """Clase específica para indicar que se ha producido un error al conectar
    con la API Petfinder."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class MaxPetfinderRequestsExceeded(Exception):
    """Clase específica para indicar que se han excedido el número máximo de
    peticiones a la API Petfinder."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class WrongPetIndex(Exception):
    """Clase específica para indicar que el identificador de una mascota proporcionado
    no es válido."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class PetsNotFound(Exception):
    """Clase específica para indicar que no existen mascotas registradas."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class WrongNumberSearchParameters(Exception):
    """Clase específica para indicar que el número de parámetros de búsqueda
    es incorrecto."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class WrongSearchParametersValues(Exception):
    """Clase específica para indicar que al menos uno de los parámetros de
    búsqueda debe de tener un valor."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
    
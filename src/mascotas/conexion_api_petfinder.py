#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase singleton para realizar una única conexión con la API Petfinder.

@author: Lidia Sánchez Mérida
"""
import sys
import petpy
import os
sys.path.append("../")
from excepciones import OneInstanceConexionAPIPetfinder, ApiPetfinderConnectionError

class ConexionAPIPetfinder:
    __instance = None
    
    def __init__(self):
      """Crear la única instancia de esta clase."""
      if ConexionAPIPetfinder.__instance != None: 
          raise OneInstanceConexionAPIPetfinder("Ya existe una instancia de esta clase singleton.")
      else: 
          return ConexionAPIPetfinder.__instance
    
    @staticmethod 
    def getInstance():
      """Obtener la única instancia de esta clase."""
      if ConexionAPIPetfinder.__instance == None: ConexionAPIPetfinder()
      return ConexionAPIPetfinder.__instance
  
    @staticmethod
    def conectarConPetfinder():
        """Obtenemos de las variables de entorno las credenciales para la conexión"""
        api_key = os.environ.get("API_KEY")
        api_secret = os.environ.get("API_SECRET")
      
        """Comprobamos las credenciales"""
        if (api_key == None or isinstance(api_key, str) == False or
            api_secret == None or isinstance(api_secret, str) == False):
            raise ApiPetfinderConnectionError("Credenciales no válidas.")
      
        """Conectamos con la API Petfinder."""
        try:
            ConexionAPIPetfinder.__instance = petpy.Petfinder(api_key, api_secret)
            return ConexionAPIPetfinder.__instance
        except petpy.exceptions.PetfinderInvalidCredentials:
            raise ApiPetfinderConnectionError("Credenciales no válidas.")

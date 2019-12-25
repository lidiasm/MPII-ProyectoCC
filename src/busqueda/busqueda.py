#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase que representa el motor de búsqueda por el cual se podrá realizar una consulta
en base a unos parámetros definidos para obtener las fichas de las mascotas que 
cumplan con los términos buscados.

@author: Lidia Sánchez Mérida.
"""
import sys
sys.path.append("src")
from excepciones import WrongNumberSearchParameters, WrongSearchParametersValues, PetsNotFound

class Busqueda:
    
    def comparar_variables_busqueda(self, variable1, variable2):
        """Método para comparar el valor de dos cadenas. Si la segunda cadena está
            vacía se devuelve verdadero para no interferir en la búsqueda."""
        if (variable2 == ""): return True
        elif (type(variable1) != type(variable2)): raise TypeError('Los tipos de las variables '
           'deben ser iguales')
        return variable1 == variable2
    
    def buscar(self, mascotas, terminos_busqueda):
        """Método para buscar las mascotas que coincidan con los términos de
            búsqueda establecidos.
            Se le deberán proporcionar como argumentos un diccionario con los
            datos de cada mascota en un diccionario aparte, y otro diccionario
            con los parámetros de búsqueda completados o vacíos.
        """
        if (len(terminos_busqueda) != 7): raise WrongNumberSearchParameters('Deben existir los '
           'siete términos de búsqueda.')
        """Comprobamos que al menos uno de los términos tenga algún valor."""
        tiene_valor = False
        if (terminos_busqueda['tipo_animal'] != ""): tiene_valor = True
        elif (terminos_busqueda['edad'] != ""): tiene_valor = True
        elif (terminos_busqueda['genero'] != ""): tiene_valor = True
        elif (terminos_busqueda['tamanio'] != ""): tiene_valor = True
        elif (terminos_busqueda['ninios'] != ""): tiene_valor = True
        elif (terminos_busqueda['gatos'] != ""): tiene_valor = True
        elif (terminos_busqueda['perros'] != ""): tiene_valor = True
        if (tiene_valor == False): raise WrongSearchParametersValues('Debe existir al menos un término '
           'de búsqueda con un valor.') 
        
        """Comprobamos si existen mascotas."""
        if (len(mascotas) == 0 or type(mascotas) != dict): raise PetsNotFound('No hay mascotas sobre las que realizar la búsqueda.')
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

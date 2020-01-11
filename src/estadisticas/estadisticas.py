#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase que contiene la lógica de la parte de la api encargada de generar las 
estadísticas predefinidas con los datos de las mascotas descargados.
Tipos de estadísticas:
    1) Mascotas en adopción que sepan relacionarse con niños.
    2) Razas de perros que mejor se relacionen tanto con niños como con otros animales.
    3) Tipos de animales que se pueden adoptar así como el número de ejemplares disponibles.
    
@author: Lidia Sánchez Mérida
"""
import sys
sys.path.append("src")
from excepciones import PetsNotFound
import operator

class Estadisticas:
    
    def generar_estadistica_tipos_mascotas(self, mascotas):
        """Método que genera un informe estadísico en formato JSON con los tipos
            de mascotas que se pueden adoptar así como su número de ejemplares respectivo."""
        if (type(mascotas) != dict or len(mascotas) == 0):
            raise PetsNotFound('No hay mascotas sobre las que generar el informe estadístico.')
        
        estadistica = {}
        for m in mascotas:
            if mascotas[m]['tipo_animal'].lower() not in estadistica:
                animal = mascotas[m]['tipo_animal']
                estadistica[animal] = sum(1 for m2 in mascotas if mascotas[m2]['tipo_animal'].lower() == animal)            
        
        """Ordenamos los datos de forma descendente para colocar el tipo de animal
            más amistoso con los niños en primer lugar."""
        estadistica_ordenada = dict( sorted(estadistica.items(), key=operator.itemgetter(1),reverse=True))
        
        return estadistica_ordenada
        
    
    def generar_estadistica_ninios(self, mascotas):
        """Método que genera un informe estadísico en formato JSON con el porcentaje
            asociado a las mascotas de cada tipo que pueden relacionarse con niños."""
        if (type(mascotas) != dict or len(mascotas) == 0):
            raise PetsNotFound('No hay mascotas sobre las que generar el informe estadístico.')

        estadistica = {}
        total_mascotas = {}
        for mascota in mascotas:
            """Mascotas que se relacionan bien con niños."""
            if mascotas[mascota]['ninios'].lower() == 'yes':
                if mascotas[mascota]['tipo_animal'] not in estadistica:
                    estadistica[mascotas[mascota]['tipo_animal']] = 1
                else:
                    estadistica[mascotas[mascota]['tipo_animal']] += 1
            """Total de cada tipo de mascota."""
            if mascotas[mascota]['tipo_animal'] not in total_mascotas:
                total_mascotas[mascotas[mascota]['tipo_animal']] = 1
            else:
                total_mascotas[mascotas[mascota]['tipo_animal']] += 1
        
        """Ordenamos los datos de forma descendente para colocar el tipo de animal
            más amistoso con los niños en primer lugar."""
        estadistica_ordenada = dict( sorted(estadistica.items(), key=operator.itemgetter(1),reverse=True))
        """Calculamos el porcentaje para cada tipo de mascota."""
        for mascota in total_mascotas:
            estadistica_ordenada[mascota] = str((estadistica_ordenada[mascota] / total_mascotas[mascota])*100) + "%"
        
        return estadistica_ordenada
    
    def generar_estadistica_razas_perro(self, mascotas):
        """Método que genera un informe estadísico en formato JSON con el porcentaje
            asociado a las razas de perro más sociables."""
        if (type(mascotas) != dict or len(mascotas) == 0):
            raise PetsNotFound('No hay mascotas sobre las que generar el informe estadístico.')
            
        estadistica = {}
        total_razas = {}
        """Contamos los ejemplares de las distintas razas de perro."""
        for m in mascotas:
            if (mascotas[m]['tipo_animal'].lower() == 'dog'):
                if (mascotas[m]['raza'].lower() not in total_razas and mascotas[m]['raza'].lower() != "dnv"):
                    raza_perro = mascotas[m]['raza'].lower() 
                    total_razas[raza_perro] = sum(1 for m2 in mascotas if mascotas[m2]['raza'].lower() == raza_perro)
        
        """Calculamos la sociabilidad con cada animal y niño"""
        n_ninios = n_gatos = n_perros = 0
        for raza in total_razas:
            if (raza not in estadistica):
                n_ninios = sum(1 for m3 in mascotas if mascotas[m3]['raza'].lower() == raza 
                    and mascotas[m3]['ninios'].lower() == 'yes')
                n_perros = sum(1 for m3 in mascotas if mascotas[m3]['raza'].lower() == raza 
                    and mascotas[m3]['perros'].lower() == 'yes')
                n_gatos = sum(1 for m3 in mascotas if mascotas[m3]['raza'].lower() == raza
                    and mascotas[m3]['gatos'].lower() == 'yes')
                
                estadistica[raza] = {'ninios': str((n_ninios/total_razas[raza])*100) + "%",
                                     'gatos': str((n_gatos/total_razas[raza])*100) + "%",
                                     'perros': str((n_perros/total_razas[raza])*100) + "%"}
                
        return estadistica
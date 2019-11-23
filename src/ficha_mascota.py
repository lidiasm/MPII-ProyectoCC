#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 11:43:13 2019

Clase que representa la estructura de datos con los campos que se completarán
con la información de cada mascota.

@author: Lidia Sánchez Mérida
"""
class FichaMascota:
    
    def __init__(self, nombre, tipo_animal, raza, tamanio, genero, edad,
                 tipo_pelaje, estado, ninios, gatos, perros, ciudad, pais):
        self.nombre = nombre
        self.tipo_animal = tipo_animal
        self.raza = raza
        self.tamanio = tamanio
        self.genero = genero
        self.edad = edad
        self.tipo_pelaje = tipo_pelaje
        self.estado = estado
        self.bueno_con_ninios = ninios
        self.bueno_con_gatos = gatos
        self.bueno_con_perros = perros
        self.ciudad = ciudad
        self.pais = pais

    def to_s(self):
        return "".join(["Nombre: ", self.nombre, "\nTipo de mascota: ", self.tipo_animal,
        "\nRaza: ", self.raza, "\nTamaño: ", self.tamanio, "\nEdad: ", self.edad,
        "\nTipo de pelaje: ", self.tipo_pelaje, "\nEstado: ", self.estado,
        "\nBueno con niños: ", str(self.bueno_con_ninios),
        "\nBueno con gatos: ", str(self.bueno_con_gatos),
        "\nBueno con perros: ", str(self.bueno_con_perros), "\nCiudad: ", self.ciudad,
        "\nPais: ", self.pais])

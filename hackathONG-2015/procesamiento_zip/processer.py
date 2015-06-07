#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

def process(filename):
    """
    Procesa los nombres de Nombres de los archivos zip
    devolviendo una lista que contiene, Departamento,
    Localidad, tipo de Dato, y año.
    """
    result = []
    dpto = ''
    data_list = filename.split(' - ')
    aux_dto_list = data_list[0].split(' ')
    if len(aux_dto_list) < 3:
        print "No compatible: %s" % data_list
        return False

    aux_dto_list.pop(0) #eliminamos 'Capa'
    aux_dto_list.pop(0) #eliminamos 'Localidad'
    #Si la tercera palabra es un 'de', lo eliminamos
    if aux_dto_list[0] == "de":
        aux_dto_list.pop(0)
    #Concatenamos el nombre del departamente
    for word in aux_dto_list:
        dpto += word
    #Formamos la lista
    result.append(dpto.decode('iso-8859-1').encode('utf8'))
    result.append(re.sub(" ", "", data_list[1]))
    result.append(re.sub(" ", "", data_list[2]))
    result.append(re.sub(" ", "", data_list[3]))

    return result

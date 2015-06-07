# -*- coding: utf-8 -*-
""" comparar los textos de los archivos con los nombres oficiales de municipedia
para poder vincular los IDs """
import json

class getMunis:
    
    def __init__(self, json_file='municipios_municipedia.json'):        
        self.munis = json.load(open(json_file))


# -----------------------------
# TEST
import sys, os
import Levenshtein as levi
import processer

path = sys.argv[1]
archives = os.listdir(path)

munis = getMunis()

c=0
for file in archives:
    name_attr = processer.process(file)
    print name_attr
    if not name_attr:
        continue

    

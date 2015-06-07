# -*- coding: utf-8 -*-
""" 
Comparar los textos de los archivos con los nombres oficiales de municipedia
para poder vincular los IDs 
"""
import sys, os
import Levenshtein as levi
import processer
from munis import getMunis

path = sys.argv[1]
archives = os.listdir(path)

munis = getMunis()

c=0
for filename in archives:
    name_attr = processer.process(filename)
    print name_attr
    if not name_attr:
        continue

    

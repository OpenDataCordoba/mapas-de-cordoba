# -*- coding: utf-8 -*-
""" read projections and detect cities at Paso-2--metadatos-by-tabulapdf.csv file """

import csv
import json

class Projections:
    def __init__(self, path='Paso-2--metadatos-by-tabulapdf.csv'):
        f = open(path, 'r')
        reader = csv.reader(f)

        self.projections_type = {}
        self.projections = {}
        self.cities = []
        for p in reader:
            depto, city, projection = p
            # print "depto: {}, ciudad:{}, proyeccion:{}".format(depto, city, projection)
            self.cities.append(city)
            self.projections[city] = projection
            if not self.projections_type.get(projection, None):
                self.projections_type[projection] = 1
            else:
                self.projections_type[projection] = self.projections_type[projection] + 1
                
    def projections_types(self):
        return json.dumps(self.projections_type, sort_keys=True, indent=2, separators=(',', ': '))
    

if __name__ == "__main__":
    """ mostrar la cantidad de proyecciones detectadas y cuanto se usan"""
    p = Projections()
    print "======================="
    print "Proyecciones detectadas"
    print "======================="
    print p.projections_types()
    print "======================="
    print "Ciudades encontradas: %d" % len(p.cities)
    
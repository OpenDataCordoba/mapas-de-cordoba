# -*- coding: utf-8 -*-
import Levenshtein as levi


class LeviMuni():
    """ encontrar el municipio de la base oficial basados en un nombre diferente """
    
    def __init__(self, munis):
        self.munis = munis # municipios de municipedia
        
    def find(self, municipio):
        """ analizar un nombre de municipio y encontrar su mejor match """
        max_levi = 0.0
        final = None
        for m in self.munis: # munis es mi base oficial de Municipedia
            muni = m['municipio'] if type(m['municipio']) == unicode else unicode(m['municipio'].decode('utf8'))
            
            lev_res = levi.ratio(municipio, muni)
            if lev_res > max_levi:
                max_levi = lev_res
                final = m
                
        return final


if __name__ == "__main__":
    """ probar contra el CSV de proyecciones """
    from munis import getMunis
    munis = getMunis().munis # obtener los municipios de municipedia
    lm = LeviMuni(munis=munis)

    import csv
    reader = csv.reader('metadatos-2010/Paso-2--metadatos-by-tabulapdf.csv')

    for p in reader:
        depto, city, projection = p
        muni = lm.find(city)
        if not muni:
            print "NO %s " % city
        else:
            print "SI %s == %s" % (city, muni['municipio'])
        
    
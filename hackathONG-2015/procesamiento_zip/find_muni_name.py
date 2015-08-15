# -*- coding: utf-8 -*-
import Levenshtein as levi


class LeviMuni():
    """ encontrar el municipio de la base oficial basados en un nombre diferente """
    
    def __init__(self, munis):
        self.munis = munis # municipios de municipedia
        self.final_munis = {} # resultados finales despues del procesamiento
        self.final_municipedia = {} # uso de los IDs de municipedia
        self.final_loc = {} # relacion final localidad -> municipio

        self.errores = []
    
    def find(self, municipio):
        """ analizar un nombre de municipio y encontrar su mejor match """
        loc = municipio
        
        max_levi = 0.0
        final = None
        for m in self.munis: # munis es mi base oficial de Municipedia
            muni = m['municipio'] if type(m['municipio']) == unicode else unicode(m['municipio'].decode('utf8'))
            
            lev_res = levi.ratio(loc, muni)
            if lev_res > max_levi:
                max_levi = lev_res
                final = m
                
        return final
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
            municipio = municipio if type(municipio) == unicode else unicode(municipio.decode('utf-8'))
            
            lev_res = levi.ratio(municipio, muni)
            if lev_res > max_levi:
                max_levi = lev_res
                final = {'m': m, 'levi': lev_res}
                
        return final


if __name__ == "__main__":
    """ probar contra el CSV de proyecciones """
    from munis import getMunis
    munis = getMunis().munis # obtener los municipios de municipedia
    lm = LeviMuni(munis=munis)

    import csv
    path = 'metadatos-2010/Paso-2--metadatos-by-tabulapdf.csv'
    f = open(path, 'r')
    reader = csv.reader(f)

    for p in reader:
        try:
            depto, city, projection = p
        except Exception, e:
            print "Error line %s => %s" % (str(p), str(e))
            exit(1)
            
        m = lm.find(city)
            
        if not m:
            print "NO %s " % city
        else:
            lev = m['levi'] 
            muni = m['m']['municipio'] if type(m['m']['municipio']) == unicode else unicode(m['m']['municipio'].decode('utf8'))
            city = city if type(city) == unicode else unicode(city.decode('utf8'))
            print "SI %s %s == %s" % (str(lev), city, muni)
        
    
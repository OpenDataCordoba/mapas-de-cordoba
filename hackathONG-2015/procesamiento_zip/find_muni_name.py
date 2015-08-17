# -*- coding: utf-8 -*-
import Levenshtein as levi
import codecs
from parses import *
import csv


class LeviMuni():
    """ encontrar el municipio de la base oficial basados en un nombre diferente """
    
    def __init__(self, munis):
        self.munis = munis # municipios de municipedia
        self.results = []
        self.projections = {} # cada ID de municipedia y su proyeccion

        # shit
        self.fix_type = None # fot fix nice_tipo

    def load(self, path = 'metadatos-2010/Paso-2--metadatos-by-tabulapdf.csv'):
        """ load from file all projections """        
        f = open(path, 'r')
        reader = csv.reader(f)
    
        for p in reader:
            try:
                depto, city, projection = p
            except Exception, e:
                print "Error line %s => %s" % (str(p), str(e))
                return None
                
            if projection in ['', 'PDF']:
                # print "IGNORE %s for PDF" % city
                continue
                
            res = self.find(city)
                
            if not res:
                print "NO %s (%s)" % (city, projection)
            else:
                projection = projection if type(projection) == unicode else unicode(projection.decode('utf-8'))
                self.projections[res['m']['id']] = projection
                
            
    def find(self, municipio, para='Proyeccion'):
        """ analizar un nombre de municipio y encontrar su mejor match 
            Para medir repeticiones de uso de municipio (deberia usarse 
            uno solo para cada utilidad) se usa el <para>
            para = Proyeccion | Mapa Se usa para leer los archivos con mapas o las proyecciones """
            
        self.fix_type = None # shit
        max_levi = 0.0
        final = None
        final_muni = None # objeto de la iteracion en municipedia finalmente usado

        municipio = municipio.upper().strip()

        if para=='Proyeccion' and municipio in IGNORES_PROY:
            return None
        if para=='Mapa' and municipio in IGNORES_PROY:
            return None
            
        municipio = municipio if type(municipio) == unicode else unicode(municipio.decode('utf-8'))
        # fix some none breaking space (used in latin 1)
        municipio = municipio.replace(u'\xa0', u' ')

        if para=='Mapa' and municipio in IGNORES:
            print "Ignoring %s (MARK) " % municipio
            return None
                
        if para=='Mapa' and REPLACES.get(municipio, False): 
            municipio = REPLACES[municipio]
            
        if para=='Proyeccion' and REPLACES_PROY.get(municipio, False): 
            municipio = REPLACES_PROY[municipio]

        if para=='Mapa' and EXTRA_MAPS.get(municipio, False): 
            # nice_tipo = '%s %s' % (nice_tipo, EXTRA_MAPS[municipio]['tipomapa'])
            municipio = EXTRA_MAPS[municipio]['nombre']
            print "ADDING %s for %s" % (municipio, extra_maps[municipio])
            self.fix_type = '%s %s' % (nice_tipo, extra_maps[municipio]['tipomapa'])
            
        for m in self.munis: # munis es mi base oficial de Municipedia
            muni = m['municipio'] if type(m['municipio']) == unicode else unicode(m['municipio'].decode('utf8'))
            muni = muni.upper().strip()
            
            lev_res = levi.ratio(municipio, muni)
            if lev_res > max_levi:
                max_levi = lev_res
                final_muni = m
                final = {'original': municipio, 
                         'm': m, 
                         'levi': lev_res}
                         
        if para=='Proyeccion' and final: # contabilizar y detallar el uso
            fld = 'usado_%s' % para
            # marcar como usado al municipio
            if final_muni.get(fld, None):
                print "DUPLICADO PROY %s" % str(final_muni[fld])
                final_muni[fld].append(municipio)
                return None 
            else:
                final_muni[fld] = [municipio]
                
        else:
            print "NOT FOUND ERROR %s" % municipio

        self.results.append(final)
        return final

    def write_results(self, dest_file='results.csv'):
        """ write final results at csv"""
        f = codecs.open(dest_file, 'w', encoding='utf8')
        f.write('municipedia_id,municipedia_nombre,usado_proyeccion, usado_mapa\n')

        for r in self.munis:
            municipedia_id = r['id']
            municipedia_nombre = r['municipio']
            usado_mapa = r.get('usado_Mapa', [])
            usado_mapa_str = ' | '.join(usado_mapa)
            usado_proyeccion = r.get('usado_Proyeccion', [])
            usado_proyeccion_str = ' | '.join(usado_proyeccion)

            f.write('%s,%s,%s: %s,%s: %s\n' % (municipedia_id, municipedia_nombre, 
                                                len(usado_proyeccion), usado_proyeccion_str, 
                                                len(usado_mapa), usado_mapa_str))

        f.close()

if __name__ == "__main__":
    """ probar contra el CSV de proyecciones """
    from munis import getMunis
    munis = getMunis().munis # obtener los municipios de municipedia
    
    lm = LeviMuni(munis=munis)
    lm.load()
    
    lm.write_results()
    
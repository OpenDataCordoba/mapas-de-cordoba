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
        # algunos que no estan (?)
        # CBA capital
        self.projections[271] = u"Gauss Kruger Zona 4 (WGS84), -63º (POSGAR98)"
        # Supongo que parque norte es igual a VILLAS LOS LLANOS - JUAREZ CELMAN
        self.projections[2231] = u"Gauss Kruger Zona 4 (WGS84), -63º (POSGAR98)"
        # loteo san javier es un barrio de San Ignacio, copia proyeccion
        self.projections[500] = u"Gauss Kruger Zona 4 (WGS84), -63º (POSGAR98)"
        
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

            """
            if projection in ['', 'PDF']:
                # print "IGNORE %s for PDF" % city
                continue
            """
            
            res = self.find(city)
                
            if not res:
                # print "NO %s (%s)" % (city, projection)
                pass
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
        
        final_muni = None # objeto de la iteracion en municipedia finalmente usado
        muni_orig = municipio # para replaces viejos
        
        municipio = municipio.upper().strip()

        if para=='Proyeccion' and municipio in IGNORES_PROY:
            return None
        if para=='Mapa' and municipio in IGNORES:
            return None
            
        municipio = municipio if type(municipio) == unicode else unicode(municipio.decode('utf-8'))
        # fix some none breaking space (used in latin 1)
        municipio = municipio.replace(u'\xa0', u' ')

        if para=='Mapa' and municipio in IGNORES:
            print "Ignoring %s (MARK) " % municipio
            return None
                
        if para=='Mapa' and REPLACES.get(municipio, False): 
            print "Replacing %s for %s" % (municipio, REPLACES[municipio])
            municipio = REPLACES[municipio]
            
        if para=='Mapa' and REPLACES.get(muni_orig, False): 
            print "Replacing %s for %s" % (muni_orig, REPLACES[muni_orig])
            municipio = REPLACES[muni_orig]
        else:
            print "NOT replaces for %s" % municipio

        if para=='Proyeccion' and REPLACES_PROY.get(municipio, False): 
            municipio = REPLACES_PROY[municipio]

        if para=='Mapa' and EXTRA_MAPS.get(municipio, False): 
            municipio = EXTRA_MAPS[municipio]['nombre']
            print "ADDING %s for %s" % (municipio, EXTRA_MAPS[municipio])
            self.fix_type = EXTRA_MAPS[municipio]['tipomapa']

        if para=='Mapa' and EXTRA_MAPS.get(muni_orig, False): 
            municipio = EXTRA_MAPS[muni_orig]['nombre']
            print "ADDING %s for %s" % (municipio, EXTRA_MAPS[muni_orig])
            self.fix_type = EXTRA_MAPS[muni_orig]['tipomapa']

        final = None
        municipio = municipio.upper().strip()
        for m in self.munis: # munis es mi base oficial de Municipedia
            muni = m['municipio'] if type(m['municipio']) == unicode else unicode(m['municipio'].decode('utf8'))
            muni = muni.upper().strip()

            lev_res = levi.ratio(municipio, muni)
                
            if lev_res > max_levi:
                # print "CHECK %.2f %s -- %s" % (lev_res, municipio, muni)
                max_levi = lev_res
                final = {'original': municipio, 'm': m, 'levi': lev_res}
                         
        if final: # contabilizar y detallar el uso en el caso de las proyecciones
            final_muni = final['m']
            if para=='Proyeccion':
                # print "SELECTED %.2f %s -- %s" % (max_levi, municipio, final_muni['municipio'])
                fld = 'usado_%s' % para
                # marcar como usado al municipio
                
                if final_muni.get(fld, None):
                    print "DUPLICADO %s => PROYs %s" % (municipio, str(final_muni[fld]))
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
    
# -*- coding: utf-8 -*-
""" process geo data by OGR command """
import subprocess

class MyOGR:
    
    def __init__(self):
        self.lastError = None
        self.errores = []
        
    def load(self, localidad, anio, tipo):
        self.localidad=localidad
        self.anio=anio
        self.tipo=tipo
        
    def doit(self, shp_orig, dest_file, projection_origin="EPSG:22194", projection_dest="EPSG:4326", format_dest='GeoJSON'):
        """ pasar de shp a otro formto. Los valores predeterminados son los de este """
        command_parts = ["ogr2ogr", "-f", format_dest, "-t_srs", projection_dest, "-s_srs", projection_origin, "-skipfailures", dest_file, shp_orig]
        
        proc = subprocess.Popen(command_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        if proc.returncode != 0:
            error = {'muni': self.localidad,
                               'command': ' '.join(command_parts), 
                               'ret_code': proc.returncode,
                               'stdout': stdout.replace('\n', ''),
                               'stderr': stderr.replace('\n', '')}
            self.errores.append(error)
            self.lastError = error
            error = "Error geoJson %s [%s]-> %s" % (self.localidad, self.anio, self.tipo)
            return False, error
            
        else:
            self.lastError = None
            return True, ''
            
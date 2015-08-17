# -*- coding: utf-8 -*-
"""
Leer un directorio y procesa todos sus archivos SHP-ZIP
"""

import os, subprocess, sys, processer, json, glob
from parses import *
from slugify import slugify

path = 'GeoPortal-Cordoba/localidades' # my default value
total = 0 # do a full process. Use --total=3 for test 3 files
full_log = []
unknown_projection = [] # proyecciones que no conozcoy tomo cualquiera

for arg in sys.argv:
    if arg == '-h' or arg == '--help':
        print "%s USAGE" % sys.argv[0]
        print "  --path=/path/to/shp/content/folder"
        print "  --total=3 for just test 3 files"
        
        exit()
    
    if arg.split('=')[0] == '--path': path = arg.split('=')[1] # origin SHP folder contents
    if arg.split('=')[0] == '--total': total = int(arg.split('=')[1]) # total loops for test script    
    
archives = os.listdir(path)

tipos = [] # todos los tipos para parsear a algo legible
tmp = 'tmp' # for extract ZIPs
geojson_folder = 'geojson' # for created json
shp_folder = 'shp' # for renamed shp

try: os.mkdir(tmp)
except: pass

try: os.mkdir(geojson_folder)
except: pass

try: os.mkdir(shp_folder)
except: pass
        
from munis import getMunis
munis = getMunis().munis # obtener los municipios de municipedia
from find_muni_name import LeviMuni
myLevi = LeviMuni(munis=munis)
# cargar las proyecciones vinculadas a IDs de municipedia
myLevi.load()
projections = myLevi.projections


munis_missing = list(munis) # copia para saber cuales no se usan
final_munis = {} # relacion final desde el lado de los nombres de los archivos (localidad + tipo + anio)
final_municipedia = {} # uso de los IDs de municipedia
final_loc = {} # relacion final localidad -> municipio

c=0

from ogr import MyOGR # ejecutar ogr2ogr
myOGR = MyOGR()

for filename in archives:
    print '---------------------------------------------------'
    print 'Process file %s' % filename
        
    name_attr = processer.process(filename)
    if not name_attr:
        fl = ' xxxxxxxx CANT use file %s' % filename
        print fl
        exit(1)

    depto, localidad, tipo, anio = name_attr
    if tipo not in tipos: # solo para hacer una lista completa de tipos usados y disponer una version legibe (parses.SHP_TYPES)
        tipos.append(tipo)

    nice_tipo = SHP_TYPES.get(tipo, 'UNKNOWN SHP TYPE')
    full_path_filename = os.path.join(path, filename)
    
    print ' ----- OGR for %s' % localidad
    
    file_dir = '%s_%s_%s_%s' % (depto.replace(' ',''), localidad.replace(' ',''), nice_tipo.replace(' ',''), anio.replace(' ',''))
    
    try: # crear lacarpeta y descomprimir los ZIPs
        dest = os.path.join(tmp, file_dir)
        os.mkdir(dest)
        subprocess.call(["unzip", os.path.join(path, filename), "-d", os.path.join(os.getcwd(), dest)])
    except: # quizas ya existia
        pass

    # shp original (hay uno solo en cada zip)
    shp_orig = glob.glob(os.path.join(os.getcwd(), dest, "*.shp"))[0]


    # ver que proyeccion tiene segun los metadatos de 2010 
    # (supongo que es una extension de 2008 y es lo mismo)
    # esto esta en myLevi.projections[id municipedia]
    
    
    # buscar por cada archivo cual es el municipio oficial mas parecido segun Levi
    fname = filename if type(filename) == unicode else unicode(filename.decode('utf8'))
    fname = fname.replace('.zip', '')
    print ' ----- Leving MUNI %s' % fname
    # suponemos que localidad esta SIEMPRE escrito igual pero no,
    # las de 2010 y 2008 pueden diferir ... (por ejemplo Monte Maiz esta con y sin acento)

    res = myLevi.find(localidad, para="Mapa")
    locu = localidad if type(localidad) == unicode else unicode(localidad.decode('utf-8'))
    if not res:
        print "LEVI ERROR %s. Exiting" % locu
        exit(1)
    
    m = res['m']
    final_id_minicipedia = m['id']
    municipio = m['municipio']
    lev_res = res['levi']
    print "Usando %d %s (%.2f) para %s" % (final_id_minicipedia, municipio, lev_res, locu)

    if myLevi.fix_type: 
        nice_tipo = myLevi.fix_type
    
    # Mejorar los nombres de los campos interpretando los tipos con SHP_TYPES
    geojson_mcp_fld = 'GeoJSON ' + nice_tipo + " " + anio
    kml_mcp_fld = 'KML ' + nice_tipo + " " + anio
    shp_mcp_fld = 'SHP ' + nice_tipo + " " + anio

    print 'TIPO from %s to %s' % (tipo, nice_tipo)
    
    # ver si tengo su proyeccion
    projection = projections.get(final_id_minicipedia, None)
    if not projection:
        print "No tenemos la proyeccion (o es PDF) para (%d) %s %s" % (final_id_minicipedia, locu, municipio)
    
    if final_munis.get(localidad, False) == False:
        
        print '%s for %s is %.2f' % (municipio, locu, lev_res)
        geoJsonFile = fname + '.geojson' if not myOGR.lastError else myOGR.lastError
        geoKMLFile = fname + '.kml' if not myOGR.lastError else myOGR.lastError
        
        final_loc[localidad] = {'muni': municipio, 'muni_id': m['id'], 'max_levi': lev_res, 'filename': fname}
        final_munis[localidad] = {'muni_municipedia': municipio, 'id_municipedia':m['id'], 
                            'depto':depto, 'max_levi': lev_res, geojson_mcp_fld: geoJsonFile, 
                            kml_mcp_fld: geoKMLFile,  
                            shp_mcp_fld: fname + '.zip', 'anio': anio}
                
        
        if final_municipedia.get(final_id_minicipedia, None):
            final_municipedia[final_id_minicipedia]['uses'].append({'localidad': localidad, 'depto':depto, 'levi': lev_res})
            final_municipedia[final_id_minicipedia]['used'] += 1
        else:
            final_municipedia[final_id_minicipedia] = {'name': municipio, 'used': 0, 'uses': []}

        print 'USED [muni_id:%s] %s # %d' % (str(final_id_minicipedia), localidad, final_municipedia[final_id_minicipedia]['used'])
    
            
    else: # el mejor levi ya fue definido y vinculado con un ID en municipedia
        print 'Add %s field for %s' % (geojson_mcp_fld, localidad)
        final_munis[localidad][geojson_mcp_fld] = fname + '.geojson' if not myOGR.lastError else myOGR.lastError
        final_munis[localidad][kml_mcp_fld] = fname + '.kml' if not myOGR.lastError else myOGR.lastError
        # final_munis[loc][shp_mcp_fld] = fname + '.shp'
        
        municipio = final_munis[localidad]['muni_municipedia']
        
    new_filename = slugify('%s_%s_%s' % (municipio, nice_tipo, anio))
    new_filename_shp = '%s.shp.zip' % new_filename
    new_filename_gj = '%s.geojson' % new_filename
    new_filename_kml = '%s.kml' % new_filename
    
    # definir paths para los resultados
    new_path_shpfile = os.path.join(shp_folder, new_filename_shp)
    new_path_gjfile = os.path.join(geojson_folder, new_filename_gj)
    new_path_kmlfile = os.path.join(geojson_folder, new_filename_kml)
    final_munis[localidad][shp_mcp_fld] = new_filename_shp
    final_munis[localidad][geojson_mcp_fld] = new_filename_gj
    final_munis[localidad][kml_mcp_fld] = new_filename_kml



    
    # borrar el geoJson de destino si ya existe
    proc = subprocess.Popen(['rm', new_path_gjfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode == 1:
        print 'Error removing %s (probably doesn\'t exists)' % new_path_gjfile
        pass # No such file
    elif proc.returncode != 0:
        fl = 'ERROR[%d] %s -- %s' % (proc.returncode, stdout, stderr)
        print fl
        exit(1)


    # borrar el geoJson de destino si ya existe
    proc = subprocess.Popen(['rm', new_path_kmlfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode == 1:
        print 'Error removing %s (probably doesn\'t exists)' % new_path_kmlfile
        pass # No such file
    elif proc.returncode != 0:
        fl = 'ERROR[%d] %s -- %s' % (proc.returncode, stdout, stderr)
        print fl
        exit(1)


    # procesar con el comando OGR2OGR a GeoJSON
    # proyecciones encontradas
    if projection == u"PDF":
        print "NO TENGO PROYECCION (PDF) para %s" % municipio
        unknown_projection.append(municipio)
        # uso la mas usada (150 usos contra 83 de la 22194). Es mejor que nada
        projection_origin = 'EPSG:22174'
        
    elif projection == u"Gauss Kruger Zona 4 (Campo Inchauspe), -63\u00ba":
        projection_origin = 'EPSG:22194'
    elif projection == u"Gauss Kruger Zona 4 (WGS84), -63\u00ba (POSGAR98)":
        projection_origin = 'EPSG:22174'
    else:
        print "PROYECCION DESCONOCIDA=(%s) para %s" % (projection, municipio)
        exit(1)

    
    myOGR.load(localidad, anio, tipo)
    
    resOGR, errorOGR = myOGR.doit(shp_orig=shp_orig, dest_file=new_path_gjfile,
                                  projection_origin=projection_origin, 
                                  projection_dest="EPSG:4326", 
                                  format_dest='GeoJSON')
    if not resOGR:
        print errorOGR
    else:
        print "Process GeoJSON OK: %s " % shp_orig

    # procesar con el comando OGR2OGR a KML
    
    resOGR, errorOGR = myOGR.doit(shp_orig=shp_orig, dest_file=new_path_kmlfile, 
                                  projection_origin=projection_origin, 
                                  projection_dest="EPSG:4326", 
                                  format_dest='KML')
    if not resOGR:
        print errorOGR
    else:
        print "Process KML OK: %s " % shp_orig


    c += 1
    if total > 0 and c >= total: break

try:
    os.mkdir('results')
except:
    pass

# Ids usados de municipedia (salvo casos especiales ninguno debe ser 2)
import codecs

repetidos = 0
nousados = 0

for i, v in final_municipedia.iteritems():
    if v['used'] > 1:
        print 'GRAVE REPETIDO %s veces. Muni: %s' % (v['used'], v['name'])
        repetidos += 1
    elif v['used'] == 0:
        nousados += 1
    

print "Repetidos (grave): %d" % repetidos
print "No usados (no reciben datos en municipedia): %d" % nousados
print "No los reconocemos (grave, se pierde el dato): %d" % len(IGNORES)
print "Errores GeoJson: %d" % len(myOGR.errores)

# errores de codificacion de OGR
f = codecs.open('results/errores_gj.csv', 'w', encoding='utf8')
f.write('muni, command, ret_code, stdout, stderr')
for e in myOGR.errores:    
    f.write('\n%s,%s,%s,%s,%s' % (e['muni'], e['command'], e['ret_code'], e['stdout'], e['stderr']))

f.close()

# resultados final en JSON de todas las localidades parseadas
f = codecs.open('results/tmp.json', 'w', encoding='utf8')
f.write(json.dumps(final_munis, indent=4, sort_keys=True))
f.close()

# todos los tipos de poligonos usados (rios, ejes, manzanas, etc)
f = codecs.open('results/tipos.csv', 'w', encoding='utf8')
f.write('TIPOS USADOS')
for t in tipos:
    f.write('\n%s' % t)
f.close()

# full_log
f = codecs.open('results/full.log', 'w', encoding='utf8')
for t in full_log:
    if type(t) == str: t = t.decode('utf8')
    f.write('\n%s' % t)
f.close()

# listar todos los campos del CSV final. 
# esto es el formato similar a lo que municipedia necesita. Una fila
# por cada municipio, un campo por cada mapa
f = codecs.open('results/tmp.csv', 'w', encoding='utf8')
f.write('Localidad mapa')
# juntar todos los campos de todos los recursos para hacer una tabla unica
# primero los que me interesan mas
final_fields = ['muni_municipedia', 'id_municipedia', 'depto', 'max_levi', 'anio']
for especial in final_fields:
    f.write(',%s' % especial)
    
for loc, data in final_munis.iteritems():
    for c, v in data.iteritems():
        if c not in final_fields:
            f.write(',%s' % c)
            final_fields.append(c)

# escribir cada dato en la columna que corresponda
for loc, data in final_munis.iteritems():
    loc = loc if type(loc) == unicode else unicode(loc.decode('utf8'))
    
    f.write('\n%s' % loc)
    for fld in final_fields:
        d = data.get(fld, False)
        if type(d) == int: d = str(d)
        if type(d) == str: d = d.decode('utf8')
        if d:
            f.write(',%s' % d)
        else:
            f.write(',')
            

f.close()

print "Proyecciones desconocidas en %d municipios" % len(unknown_projection)
# print str(unknown_projection))
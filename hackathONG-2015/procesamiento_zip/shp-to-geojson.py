# -*- coding: utf-8 -*-
"""
Leer un directorio y procesa todos sus archivos SHP-ZIP
"""

import os, subprocess, sys, processer, json, glob, shutil
from parses import *
from slugify import slugify

path = 'GeoPortal-Cordoba/localidades' # my default value
total = 0 # do a full process. Use --total=3 for test 3 files
full_log = []

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
        
import Levenshtein as levi
from munis import getMunis
munis = getMunis().munis # obtener los municipios de municipedia
munis_missing = list(munis) # copia para saber cuales no se usan
final_munis = {} # relacion final desde el lado de los nombres de los archivos (localidad + tipo + anio)
final_municipedia = {} # uso de los IDs de municipedia
final_loc = {} # relacion final localidad -> municipio

c=0

from ogr import MyOGR # ejecutar ogr2ogr
myOGR = MyOGR()

for filename in archives:
    full_log.append('---------------------------------------------------')
    full_log.append('Process file %s' % filename)
        
    name_attr = processer.process(filename)
    if not name_attr:
        fl = ' xxxxxxxx CANT use file %s' % filename
        full_log.append(fl)
        print fl
        exit(1)

    depto, localidad, tipo, anio = name_attr
    if tipo not in tipos: # solo para hacer una lista completa de tipos usados y disponer una version legibe (parses.SHP_TYPES)
        tipos.append(tipo)

    nice_tipo = SHP_TYPES.get(tipo, 'UNKNOWN SHP TYPE')
    full_path_filename = os.path.join(path, filename)
    
    full_log.append(' ----- OGR for %s' % localidad)
    
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
    
    






    
    # borrar el geoJson de destino si ya existe
    fnamedest = filename.replace('.zip', '.geojson')
    fnamedest = fnamedest.replace(' ', '-')
    dest_geojson = os.path.join(geojson_folder,fnamedest) 
    
    proc = subprocess.Popen(['rm', dest_geojson], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode == 1:
        full_log.append('Error removing %s (probably doesn\'t exists)' % dest_geojson)
        pass # No such file
    elif proc.returncode != 0:
        fl = 'ERROR[%d] %s -- %s' % (proc.returncode, stdout, stderr)
        full_log.append(fl)
        print fl
        exit(1)


    # procesar con el comando OGR2OGR a GeoJSON
    myOGR.load(localidad, anio, tipo)
    
    resOGR, errorOGR = myOGR.doit(shp_orig=shp_orig, dest_file=dest_geojson,
                                  projection_origin="EPSG:22194", projection_dest="EPSG:4326", 
                                  format_dest='GeoJSON')
    if not resOGR:
        full_log.append(errorOGR)
        print errorOGR
        
    else:
        full_log.append("Process OK: %s " % shp_orig)

    # procesar con el comando OGR2OGR a KML
    dest_kml = dest_geojson.replace('.geojson', '.kml')
    resOGR, errorOGR = myOGR.doit(shp_orig=shp_orig, dest_file=dest_kml, 
                                  projection_origin="EPSG:22194", projection_dest="EPSG:4326", 
                                  format_dest='KML')
    if not resOGR:
        full_log.append(errorOGR)
        print errorOGR
        
    else:
        full_log.append("Process OK: %s " % shp_orig)



    # buscar por cada archivo cual es el municipio oficial mas parecido segun Levi
    fname = filename if type(filename) == unicode else unicode(filename.decode('utf8'))
    fname = fname.replace('.zip', '')
    full_log.append(' ----- Leving MUNI %s' % fname)
    # suponemos que localidad esta SIEMPRE escrito igual pero no,
    # las de 2010 y 2008 pueden diferir ... (por ejemplo Monte Maiz esta con y sin acento)
    loc = localidad if type(localidad) == unicode else unicode(localidad.decode('utf8'))
    # fix some none breaking space (used in latin 1)
    loc = loc.replace(u'\xa0', u' ')
    full_log.append('LOC: %s' % loc)
    
    if loc in IGNORES:
        full_log.append("Ignoring %s (MARK) " % loc)
        continue

    replaces = REPLACES
    if replaces.get(loc, False): 
        full_log.append("REPLACING %s for %s" % (loc, replaces[loc]))
        loc = replaces[loc]
    else:
        full_log.append("NOT REPLACING %s (%s - %s)" % (loc, repr(loc), type(loc)))
        

    extra_maps = EXTRA_MAPS
    if extra_maps.get(loc, False): 
        full_log.append("ADDING %s for %s" % (loc, extra_maps[loc]))
        nice_tipo = '%s %s' % (nice_tipo, extra_maps[loc]['tipomapa'])
        loc = extra_maps[loc]['nombre']
        
    """ 
    Mejorar los nombres de los campos interpretando los tipos con SHP_TYPES
    geojson_mcp_fld = 'geojson_mcp_' + tipo + " " + anio
    shp_mcp_fld = 'shp_mcp_' + tipo + " " + anio
    """
    geojson_mcp_fld = 'GeoJSON ' + nice_tipo + " " + anio
    shp_mcp_fld = 'SHP ' + nice_tipo + " " + anio

    full_log.append('TIPO from %s to %s' % (tipo, nice_tipo))
    
    if final_munis.get(loc, False) == False:
        max_levi = 0.0
        final_id_minicipedia = None
        final_muni = None
        for m in munis: # munis es mi base oficial de Municipedia
            muni = m['municipio'] if type(m['municipio']) == unicode else unicode(m['municipio'].decode('utf8'))
            
            # asegurarse que todo se inicialicen con cero usos
            if not final_municipedia.get(m['id'], False):
                final_municipedia[m['id']] = {'name': muni, 'used': 0, 'uses': []}
            
            
            lev_res = levi.ratio(loc, muni)
            if lev_res > max_levi:
                full_log.append('%s for %s is %.2f' % (muni, loc, lev_res))
                max_levi = lev_res
                geoJsonFile = fname + '.geojson' if not myOGR.lastError else myOGR.lastError
                final_loc[loc] = {'muni': muni, 'muni_id': m['id'], 'max_levi': lev_res, 'filename': fname}
                final_munis[loc] = {'muni_municipedia': muni, 'id_municipedia':m['id'], 
                                    'depto':depto, 'max_levi': lev_res, geojson_mcp_fld: geoJsonFile, 
                                    shp_mcp_fld: fname + '.zip', 'anio': anio}
                final_id_minicipedia = m['id']
                final_muni = muni
                
        if final_muni: # es la primera coincidencia de un municipio
            full_log.append('USED [muni_id:%s] %s # %d' % (str(final_id_minicipedia), loc, final_municipedia[final_id_minicipedia]['used']))
            final_municipedia[final_id_minicipedia]['uses'].append({'localidad': loc, 'depto':depto, 'levi': lev_res})
            final_municipedia[final_id_minicipedia]['used'] += 1
            # aprovecho para copiar el SHP a un nuevo nombre (ahora que se a que municipio corresponde)
            new_filename = slugify('%s_%s_%s' % (final_muni, nice_tipo, anio))
            new_filename_shp = '%s.shp.zip' % new_filename
            new_filename_gj = '%s.geojson' % new_filename
            new_path_shpfile = os.path.join(shp_folder, new_filename_shp)
            new_path_gjfile = os.path.join(geojson_folder, new_filename_gj)
            shutil.copy(full_path_filename, new_path_shpfile)
            final_munis[loc][shp_mcp_fld] = new_filename_shp
            # move old geoJSON to new
            shutil.move(dest_geojson, new_path_gjfile)
            final_munis[loc][geojson_mcp_fld] = new_filename_gj
            
            
    else: #el mejor levi ya fue definido
        # ya detecte el municpio pero este es otro mapa distinto que necesito tambien
        full_log.append('Add %s field for %s' % (geojson_mcp_fld, loc))
        final_munis[loc][geojson_mcp_fld] = fname + '.geojson' if not myOGR.lastError else myOGR.lastError
        # final_munis[loc][shp_mcp_fld] = fname + '.shp'
        
        finalmuni = final_munis[loc]['muni_municipedia']
        # aprovecho para copiar el SHP a un nuevo nombre (ahora que se a que municipio corresponde)
        
        # aprovecho para copiar el SHP a un nuevo nombre (ahora que se a que municipio corresponde)
        new_filename = slugify('%s_%s_%s' % (finalmuni, nice_tipo, anio))
        new_filename_shp = '%s.shp.zip' % new_filename
        new_filename_gj = '%s.geojson' % new_filename
        new_path_shpfile = os.path.join(shp_folder, new_filename_shp)
        new_path_gjfile = os.path.join(geojson_folder, new_filename_gj)
        shutil.copy(full_path_filename, new_path_shpfile)
        final_munis[loc][shp_mcp_fld] = new_filename_shp
        # move old geoJSON to new
        shutil.move(dest_geojson, new_path_gjfile)
        final_munis[loc][geojson_mcp_fld] = new_filename_gj
                
            
            
    c += 1
    if total > 0 and c >= total: break

try:
    os.mkdir('results')
except:
    pass

# Ids usados de municipedia (salvo casos especiales ninguno debe ser 2)
import codecs
f = codecs.open('results/errores.csv', 'w', encoding='utf8')
f.write('id,nombre,error,detalle')
repetidos = 0
nousados = 0

for i, v in final_municipedia.iteritems():
    if v['used'] > 1:
        error = 'Usado %s veces' % v['used']
        f.write('\n%s,%s,%s,%s' % (i, v['name'], 'repetido', error))
        repetidos += 1
    elif v['used'] == 0:
        nousados += 1
        f.write('\n%s,%s,%s,' % (i, v['name'], 'no usado'))
        
for i in IGNORES:
    f.write('\n%s,%s,%s,' % (0, i, 'no detectado'))

f.close()

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

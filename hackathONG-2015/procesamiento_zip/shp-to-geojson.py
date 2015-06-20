# -*- coding: utf-8 -*-
"""
Leer un directorio y procesa todos sus archivos SHP-ZIP
"""

import os, subprocess, sys, processer, json, glob

path = 'GeoPortal-Cordoba/localidades' # my default value
total = 0 # do a full process. Use --total=3 for test 3 files
doLevi=False # do a Levinshtein comparation
doGeoJson=False # process shp to GeoJson
for arg in sys.argv:
    if arg == '-h' or arg == '--help':
        print "%s USAGE" % sys.argv[0]
        print "  --doLevi do a Levinshtein comparation"
        print "  --doGeoJson process SHP to GeoJson"
        print "  --path=/path/to/shp/content/folder"
        print "  --total=3 for just test 3 files"
        
        exit()
    
    if arg.split('=')[0] == '--path': path = arg.split('=')[1] # origin SHP folder contents
    if arg.split('=')[0] == '--total': total = int(arg.split('=')[1]) # total loops for test script
    if arg == '--doLevi': doLevi = True
    if arg == '--doGeoJson': doGeoJson = True
    
    
archives = os.listdir(path)

if doGeoJson:
    # crear las carpetas de extraccion temporal y de destino de los geoJson
    tmp = 'tmp' # for extract ZIPs
    geojson_folder = 'geojson' # for created json
    try:
        os.mkdir(tmp)
    except:
        pass
    
    try:
        os.mkdir(geojson_folder)
    except:
        pass

if doLevi:
    import Levenshtein as levi
    from munis import getMunis
    munis = getMunis().munis
    munis_missing = list(munis) # copia para saber cuales no se usan
    final_munis = {} # relacion final desde el lado de los nombres de los archivos (localidad + tipo + anio)
    final_municipedia = {} # uso de los IDs de municipedia
    final_loc = {} # relacion final localidad -> municipio
    errores_gj = []
c=0
for filename in archives:
    name_attr = processer.process(filename)
    if not name_attr:
        continue

    depto, localidad, tipo, anio = name_attr
    errorGeoJson = None # for using at Levi time if needed
    if doGeoJson:
        file_dir = '%s_%s_%s_%s' % (depto.replace(' ',''), localidad.replace(' ',''), tipo.replace(' ',''), anio.replace(' ',''))
        
        try:
            dest = os.path.join(tmp, file_dir)
            os.mkdir(dest)
            subprocess.call(["unzip", os.path.join(path, filename), "-d", os.path.join(os.getcwd(), dest)])
        except:
            pass

        # shp original
        shp_orig = glob.glob(os.path.join(os.getcwd(), dest, "*.shp"))[0]
        
        # borrar el geoJson de destino si ya existe
        dest_geojson = os.path.join(geojson_folder,filename.replace('.zip', '.geojson')) # NO ESCAPAR PARA EL REMOVE (?), fallará)
        
        proc = subprocess.Popen(['rm', dest_geojson], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if proc.returncode == 1:
            pass # No such file
        elif proc.returncode != 0:
            print 'ERROR[%d] %s -- %s' % (proc.returncode, stdout, stderr)
            exit(1)
            
        command_parts = ["ogr2ogr", "-f", "GeoJSON", "-t_srs", "EPSG:4326","-s_srs", "EPSG:22194", dest_geojson, shp_orig]
        
        proc = subprocess.Popen(command_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        if proc.returncode != 0:
            errores_gj.append({'muni': localidad,
                               'command': ' '.join(command_parts), 
                               'ret_code': proc.returncode,
                               'stdout': stdout.replace('\n', ''),
                               'stderr': stderr.replace('\n', '')})
            errorGeoJson = 'ERROR'
            print "Error geoJson %s [%s]-> %s" % (localidad, anio, tipo)
            
            # exit(1)
        # else:
        #     print "Process OK: %s " % shp_orig
        

    if doLevi: # buscar por cada archivo cual es el municipio oficial mas parecido
        fname = filename if type(filename) == unicode else unicode(filename.decode('utf8'))
        fname = fname.replace('.zip', '')

        # suponemos que localidad esta SIEMPRE escrito igual pero no,
        # las de 2010 y 2008 pueden diferir ... (por ejemplo Monte Maiz esta con y sin acento)
        loc = localidad if type(localidad) == unicode else unicode(localidad.decode('utf8'))
        
        from parses import IGNORES
        ignores = IGNORES
        if loc in ignores:
            print "Ignoring %s" % loc
            continue

        from parses import REPLACES
        replaces = REPLACES
        
        if replaces.get(loc, False): 
            print "REPLACING %s for %s" % (loc, replaces[loc])
            loc = replaces[loc]

        from parses import EXTRA_MAPS
        extra_maps = EXTRA_MAPS
        
                    
        if extra_maps.get(loc, False): 
            print "ADDING %s for %s" % (loc, extra_maps[loc])
            loc = extra_maps[loc]
        
        
        #TODO limpiar tipos
        geojson_mcp_fld = 'geojson_mcp_' + tipo + " " + anio
        shp_mcp_fld = 'shp_mcp_' + tipo + " " + anio
                    
        if final_munis.get(loc, False) == False:
            max_levi = 0.0
            final_id_minicipedia = None
            final_muni = None
            for m in munis:
                muni = m['municipio'] if type(m['municipio']) == unicode else unicode(m['municipio'].decode('utf8'))
                
                # asegurarse que todo se inicialicen con cero usos
                if not final_municipedia.get(m['id'], False):
                    final_municipedia[m['id']] = {'name': muni, 'used': 0, 'uses': []}
                
                
                lev_res = levi.ratio(loc, muni)
                if lev_res > max_levi:
                    max_levi = lev_res
                    geoJsonFile = fname + '.geojson' if not errorGeoJson else errorGeoJson
                    final_loc[loc] = {'muni': muni, 'muni_id': m['id'], 'max_levi': lev_res, 'filename': fname}
                    final_munis[loc] = {'muni_municipedia': muni, 'id_municipedia':m['id'], 
                                        'depto':depto, 'max_levi': lev_res, geojson_mcp_fld: geoJsonFile, 
                                        shp_mcp_fld: fname + '.zip', 'anio': anio}
                    final_id_minicipedia = m['id']
                    final_muni = muni
                    
            if final_muni:
                final_municipedia[final_id_minicipedia]['uses'].append({'localidad': loc, 'depto':depto, 'levi': lev_res})
                final_municipedia[final_id_minicipedia]['used'] += 1
                
        else: #el mejor levi ya fuedefinido
            # ya detecte el municpio pero este es otro mapa distinto que necesito tambien
            final_munis[loc][geojson_mcp_fld] = fname + '.geojson' if not errorGeoJson else errorGeoJson
            final_munis[loc][shp_mcp_fld] = fname + '.shp'
            
    c += 1
    if total > 0 and c >= total: break

try:
    os.mkdir('results')
except:
    pass

if doLevi: # Ids usados de municipedia (salvo casos especiales ninguno debe ser 2)
    import codecs
    f = codecs.open('results/errores.csv', 'w', encoding='utf8')
    f.write('id,nombre,error,detalle')
    for i, v in final_municipedia.iteritems():
        if v['used'] > 1:
            error = 'Usado %s veces' % v['used']
            f.write('\n%s,%s,%s,%s' % (i, v['name'], 'repetido', error))
        elif v['used'] == 0:
            f.write('\n%s,%s,%s,' % (i, v['name'], 'no usado'))
            
    for i in ignores:
        f.write('\n%s,%s,%s,' % (0, i, 'no detectado'))

    f.close()

    # errores de codificacion de OGR
    f = codecs.open('results/errores_gj.csv', 'w', encoding='utf8')
    f.write('muni, command, ret_code, stdout, stderr')
    for e in errores_gj:    
        f.write('\n%s,%s,%s,%s,%s' % (e['muni'], e['command'], e['ret_code'], e['stdout'], e['stderr']))

    f.close()

    # resultados final en JSON de todas las localidades parseadas
    f = codecs.open('results/tmp.json', 'w', encoding='utf8')
    f.write(json.dumps(final_munis, indent=4, sort_keys=True))
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

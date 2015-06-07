# -*- coding: utf-8 -*-
"""
Leer un directorio y procesa todos sus archivos SHP-ZIP
"""

import os, subprocess, sys, processer, json

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
    final_munis = {} # relacion final desde el lado de los nombres de los archivos (localidad + tipo + anio)
    final_municipedia = {} # uso de los IDs de municipedia
    final_loc = {} # relacion final localidad -> municipio
    
c=0
for filename in archives:
    name_attr = processer.process(filename)
    if not name_attr:
        continue

    depto, localidad, tipo, anio = name_attr
    
    if doGeoJson:
        file_dir = '%s_%s_%s_%s' % (depto.replace(' ',''), localidad.replace(' ',''), tipo.replace(' ',''), anio.replace(' ',''))
        
        try:
            dest = os.path.join(tmp, file_dir)
            os.mkdir(dest)
            subprocess.call(["unzip", os.path.join(path, filename), "-d", os.path.join(os.getcwd(), dest)])
        except:
            print "Ya descomptido"
            pass
    
        # borrar el geoJson de destino si ya existe
        dest_geojson = os.path.join(geojson_folder,filename.replace('.zip', '.geojson').replace(' ', '\ '))
        try:
            os.remove(dest_geojson)
            print 'Borrado %s' % dest_geojson
        except OSError:
            print 'No existia %s' % dest_geojson
            
        command =  "ogr2ogr -f GeoJSON -t_srs EPSG:4326 -s_srs EPSG:22194"
        command += " " + dest_geojson
        command += " "+os.path.join(os.getcwd(), dest, "*.shp")
        print command
        os.system(command)

    if doLevi: # buscar por cada archivo cual es el municipio oficial mas parecido
        fname = filename if type(filename) == unicode else unicode(filename.decode('utf8'))
        fname = fname.replace('.zip', '')
        
        # suponemos que localidad esta SIEMPRE escrito igual pero no,
        # las de 2010 y 2008 pueden diferir ... (por ejemplo Monte Maiz esta con y sin acento)
        loc = localidad if type(localidad) == unicode else unicode(localidad.decode('utf8'))
        loc_check = loc + '-' + tipo + '-' + anio
        #limpiar tipos
        tipo_nice = tipo.replace('ejes_arc', 'Calles').replace('envolvente_poly', 'Envolvente')
        tipo_nice = tipo_nice.replace('envolventes_poly', 'Envolvente').replace('fraccion_poly', 'Fraccion')
        tipo_nice = tipo_nice.replace('manzana_poly', 'Manzanas').replace('manzanas_poly', 'Manzanas')
        tipo_nice = tipo_nice.replace('radio_poly', 'Radios').replace('radios_poly', 'Radios')
        tipo_nice = tipo_nice.replace('rios_arc', 'Rios')
        
        geojson_mcp_fld = 'geojson_mcp_' + tipo_nice + " " + anio
        shp_mcp_fld = 'shp_mcp_' + tipo_nice + " " + anio
                    
        if final_munis.get(loc, False) == False:
            max_levi = 0.0
            final_id_minicipedia = None
            final_muni = ''
            for m in munis:
                muni = m['municipio'] if type(m['municipio']) == unicode else unicode(m['municipio'].decode('utf8'))
                
                lev_res = levi.ratio(loc, muni)
                if lev_res > max_levi:
                    max_levi = lev_res
                    final_loc[loc] = {'muni': muni, 'muni_id': m['id'], 'max_levi': lev_res, 'filename': fname}
                    final_munis[loc] = {'loc': loc, 'muni_municipedia': muni, 'id_municipedia':m['id'], 
                                        'depto':depto, 'max_levi': lev_res, geojson_mcp_fld: fname + '.geojson', 
                                        'tipo': tipo, shp_mcp_fld: fname + '.zip', 'anio': anio}
                    final_id_minicipedia = m['id']
                    final_muni = muni
                    
            # print '%s ==> %s' % (loc, final_munis[loc])
            
            if final_municipedia.get(final_id_minicipedia, False):
                final_municipedia[final_id_minicipedia]['uses'].append({'localidad': loc, 'depto':depto, 'levi': lev_res})
                final_municipedia[final_id_minicipedia]['used'] += 1
                
            else:
                final_municipedia[final_id_minicipedia] = {'name': final_muni, 'used': 1, 
                                                           'uses': [{'localidad': loc, 
                                                           'levi': lev_res, 'filename': fname}]}
        else:
            # ya detecte el municpio pero este es otro mapa distinto que necesito tambien
            final_munis[loc][geojson_mcp_fld] = fname + '.geojson'
            final_munis[loc][shp_mcp_fld] = fname + '.shp'
            
    c += 1
    if total > 0 and c >= total: break

if doLevi: # Ids usados de municipedia (ninguno debve ser 2)
    # escribir el SQL final
    sql = """CREATE TABLE `tmp_99` (
         `id_muni` int(5) NOT NULL,
         `localidad` int(5) NOT NULL,
         `levi` float(10,2) NOT NULL,
         `shp` varchar(190) NOT NULL,
         `geojson` varchar(190) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    for i, v in final_municipedia.iteritems():
        if v['used'] > 1:
            print '****ALERTA %s Usado mas de una vez: %s=%d veces' % (v['name'], i, v['used'])
            print v['uses']

    import codecs
    f = codecs.open('tmp.json', 'w', encoding='utf8')
    f.write(json.dumps(final_munis, indent=4, sort_keys=True))
    """
    f.write('data, localidad, Municipio, id_muni, Levi, tipo, anio, SHP, GeoJSON')
    for i, v in final_munis.iteritems():
        muni = v['muni_municipedia']
        depto = v['depto']
        f.write('\n%s, %s, %s, %s, %s, %s, %s, %s, %s' % (i, v['loc'], muni, 
                v['id_municipedia'], v['max_levi'], v['tipo'], v['anio'],
                v['filename'] + '.zip', v['filename'] + '.geojson'))
        """
    f.close()
    
        
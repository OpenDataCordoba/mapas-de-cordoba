"""
Leer un directorio y procesa todos sus archivos SHP-ZIP
"""

import os, subprocess, sys, processer

path = '/home/casa/hton/GeoPortal-Cordoba/localidades' # my default value
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
    final_munis = {} # relacion final
    id_used = {} # ids usados (para no usar mas de una vez un ID)
    used = {} # how we use or connect names
    
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

    if doLevi:
        try:
            loc = unicode(localidad.decode('utf8'))
        except:
            print 'Fail to decode %s %s' % (localidad, type(localidad))
            exit()
            
        if final_munis.get(loc, False) == False:
            max_levi = 0.0
            final_id_minicipedia = None
            final_muni = ''
            for m in munis:
                muni = m['municipio']
                lev_res = levi.ratio(loc, muni)
                if lev_res > max_levi:
                    max_levi = lev_res
                    final_munis[loc] = '%s %s %f' % (muni, m['id'], lev_res)
                    final_id_minicipedia = m['id']
                    final_muni = muni
                    
            print '%s ==> %s' % (loc, final_munis[loc])
            if id_used.get(final_id_minicipedia, False):
                id_used[final_id_minicipedia] += 1
                used[final_id_minicipedia] += ' [%s]' % loc
            else:
                id_used[final_id_minicipedia] = 1
                used[final_id_minicipedia] = '%s: [%s]' % (final_muni, loc)
            
    c += 1
    if total > 0 and c >= total: break

if doLevi: # Ids usados de municipedia (ninguno debve ser 2)
    for i, v in id_used.iteritems():
        if v > 1:
            print '****ALERTA Usado mas de una vez: %s=%d veces' % (i, v)
            print used[i]
        
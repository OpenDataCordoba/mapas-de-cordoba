"""
Leer un directorio y procesa todos sus archivos SHP-ZIP
"""

import os, subprocess, shutil, sys, processer, re

path = '/home/casa/hton/GeoPortal-Cordoba/localidades' # my default value
total = 0 # do a full process. Use --total=3 for test 3 files
for arg in sys.argv:
    if arg == '-h' or arg == '--help':
        print "%s USAGE" % sys.argv[0]
        print "  --path=/path/to/shp/content/folder"
        print "  --total=3 (for just test 3 files)"
        exit()
        
    if arg.split('=')[0] == '--path': path = arg.split('=')[1] # origin SHP folder contents
    if arg.split('=')[0] == '--total': total = int(arg.split('=')[1]) # total loops for test script
    
archives = os.listdir(path)

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

c=0
for filename in archives:
    name_attr = processer.process(filename)
    if not name_attr:
        continue

    depto, localidad, tipo, anio = name_attr
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
    
    c += 1
    if total > 0 and c > total: exit()
    

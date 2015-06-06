import os, subprocess, shutil, sys, processer, re

path = sys.argv[1]

archives = os.listdir(path)

for file in archives:
    file_dir = file[:-4]
    os.mkdir(name_attr[0]+"_"+name_attr[1]+"_"+name_attr[2]+"_"+name_attr[3])
    name_attr = processer.process(file)
    subprocess.call(["unzip", os.path.join(path, file), "-d", os.path.join(os.getcwd(), file_dir)])

    command = "ogr2ogr -f \"GEOJSON\" "+name_attr[0]+"_"+name_attr[1]+"_"+name_attr[2]+"_"+name_attr[3]+".geojson -t_srs EPSG:4326 -s_srs EPSG:22194 "+file_dir+"/*.shp"

    print command

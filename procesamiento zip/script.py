import os, subprocess, shutil, sys, processer, re

path = sys.argv[1]

archives = os.listdir(path)

for file in archives:
    name_attr = processer.process(file)
    if not name_attr:
        continue
        
    file_dir = name_attr[0]+"_"+name_attr[1]+"_"+name_attr[2]+"_"+name_attr[3]
    
    try:
        os.mkdir(file_dir)
        subprocess.call(["unzip", os.path.join(path, file), "-d", os.path.join(os.getcwd(), file_dir)])
    except:
        print "Ya descomptido"
        pass
        
    command = "ogr2ogr -f \"GEOJSON\" "+file_dir+".geojson -t_srs EPSG:4326 -s_srs EPSG:22194 "+os.path.join(os.getcwd(), file_dir, "*.shp")
    print command
    os.system(command)

import os, subprocess, shutil

archivos = os.listdir(".")

# Se crea la carpeta de salida

os.mkdir("geojson")

for comprimido in archivos:
    # Se crea una carpeta con el nombre del zip, sin el ".zip"
    carpeta = comprimido[:-4]
    os.mkdir(carpeta)
    # Se descomprime en la carpeta "carpeta"
    subprocess.call(["unzip", comprimido, "-d", carpeta])
    os.chdir(carpeta)
    # Se busca al archivo de entrada
    nombre_entrada = os.listdir(".")[0][:-3] + "shp"
    nombre_salida =  os.listdir(".")[0][:-3] + "geojson"
    # Se comvierte a geojson
    subprocess.call(["ogr2ogr", "-f", "\"GEOJSON\"", nombre_salida ,"-t_srs", "EPSG:4326", "-s_srs", "EPSG:22194", nombre_entrada])

    # Se mueve el geojson a la carpeta geojson y se borra el resto 
    shutil.move(nombre_salida, "../geojson/" + nombre_salida)
    os.chdir("..")
    shutil.rmtree(carpeta)           
    
    

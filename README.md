Origen de estos datos
---------------------

Son publicados por el gobierno de la provincia de cordoba en 
http://estadistica.cba.gov.ar/Territorio/GeoPortal/tabid/564/language/es-AR/Default.aspx

#### Replica scrapeada
http://andresvazquez.com.ar/data/GeoPortal-Cordoba/

### Objetivos
 - Procesar los archivos **SHP** hacia formatos mas amigables.  
 - Conectar estos datos al portal [Municipedia](http://municipedia.com).  
 
#### Requerimientos
En ubuntu requiere instalar *gdal-bin* para procesar los archivos **SHP**.  
Usa la libreria *python-levenshtein* para comparar nombres de municipios.  
Descargue el 
[archivo con los SHPs](http://andresvazquez.com.ar/data/GeoPortal-Cordoba/full-down-GeoPortal-Cordoba.tar.gz) 
y colóquelo en el directorio *procesamiento_zip*.  
Extraiga el contenido y renombre el dictorio de *localidades* como **localidades**.  

Projectiones Geograficas
------------------------
Las entidades oficiales utilizan proyecciones **Campo Inchauspe - Gauss-Kruger 
Faja 4** o lo que es equivalente, **EPSG:22194**.
Para obtener informacion sobr estas proyecciones ver u otras
http://spatialreference.org/ref/epsg/22194/
o instalar GDAL (http://www.gdal.org/gdalsrsinfo.html) y usar
```
$ gdalsrsinfo EPSG:22194
```

Para convertir shapefiles en geojson, se utiliza el programa `ogr2ogr`. Por 
ejemplo, para convertir el shapefile `amboy_ejes.shp` a geojson con Latitudes y 
Longitudes, use
```
$ ogr2ogr -f "GEOJSON" amboy-22194.geojson -t_srs EPSG:4326 -s_srs EPSG:22194 amboy_ejes.shp
```

Otras

 - EPGS:22194 Datum campo inchauspe - Gauss-Kruger faja 4

## Uso del script principal
Ingresar al directorio *hackathONG2015/procesamiento_zip*.  
```
python shp-to-geojson.py -h

 -  --doLevi do a Levinshtein comparation
 -  --doGeoJson process SHP to GeoJson
 -  --path=/path/to/shp/content/folder
 -  --total=3 for just test 3 files
```
Creará un directorio **geojson** para los archivos resultantes y otro
**tmp** para la descompresión de los archivos *shp-ZIP*.  

## Contacto

- Gaston: avila.gas (at) gmail.com @avilaton
- Andres: Andres (at) data99.com.ar @avdata99
- Lucas: lbellomo (at) protonmail.ch @lbellomo
- Mauricio: xmauryvrockx (at) gmail.com @maurygreen
- Matias: matias-sosa (at) outlook.com

#### Fuentes de inspiracion para usar estos datos

## Github como API GeoJSON

Ver https://github.com/JasonSanford/gitspatial para usar el repo como API a los 
recursos GeoJSON.

## Visualizacion de GeoJSON online

https://github.com/mapbox/geojson.io

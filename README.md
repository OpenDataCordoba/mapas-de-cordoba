Origen de estos datos
---------------------

Son publicados por el gobierno de la provincia de cordoba en 
http://estadistica.cba.gov.ar/Territorio/GeoPortal/tabid/564/language/es-AR/Default.aspx

Projectiones Geograficas
------------------------
Las entidades oficiales utilizan proyecciones **Gauss-Kruger Faja 4** o lo que 
es equivalente, **EPSG:5346**. Para obtener informacion sobr estas proyecciones 
u otras, instalar GDAL (http://www.gdal.org/gdalsrsinfo.html) y usar

```
$ gdalsrsinfo EPSG:5346
```

Para convertir shapefiles en geojson, se utiliza el programa `ogr2ogr`. Por 
ejemplo, para convertir el shapefile `amboy_ejes.shp` a geojson con Latitudes y 
Longitudes, use
```
$ ogr2ogr -f "GEOJSON" amboy.geojson -t_srs EPSG:4326 -s_srs EPSG:5346 amboy_ejes.shp
```

Fuentes de inspiracion para usar estos datos
--------------------------------------------

## Github como API GeoJSON

Ver https://github.com/JasonSanford/gitspatial para usar el repo como API a los 
recursos GeoJSON.

## Visualizacion de GeoJSON online

https://github.com/mapbox/geojson.io
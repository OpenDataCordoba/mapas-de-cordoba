Origen de los datos
===================


GEOSERVER de la muni recientemente publicado.


Descargate los datos
--------------------

Esto descarga un enorme CSV con las parcelas de la ciudad.

```
$ wget 'https://gobiernoabierto.cordoba.gob.ar/geoserver/sde/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=sde:catastro-sde-parcela&outputFormat=csv&srsName=EPSG:4326' -O /tmp/parcelas.csv
```


Carga estos datos a PostGIS
---------------------------

Crea y accede a una base de datos
```
$ createdb catastro
$ psql catastro
```

Crea las tablas
```
catastro=# CREATE EXTENSION postgis;
catastro=# CREATE TABLE parcelas (
	FID TEXT,
	destino INTEGER,
	definitiva INTEGER,
	utilidadpu INTEGER,
	nombreofic TEXT,
	numeroparc INTEGER,
	nomenclatu TEXT,
	shape_area FLOAT,
	shape_len FLOAT
);
catastro=# SELECT AddGeometryColumn ('public','parcelas','geom', 0,'MULTIPOLYGON',2);
```

Copia los datos descargados a la tabla con
```
catastro=# \copy parcelas FROM '/tmp/parcelas.csv' WITH CSV HEADER;
```

Actualiza el SRID 
```
catastro=# SELECT UpdateGeometrySRID('parcelas','geom', 4326);
```

Ver los datos
-------------

Por ejemplo, puede verse los fid y features usando
```
SELECT fid, ST_AsEWKT(geom) from parcelas limit 2;
```

# -*- coding: utf-8 -*-
"""
Hardcodeadas para parchar datos
"""

# nombres de archivos que no encajan en la norma 
FILENAME_REPLACES = {'radio_poly- 2010': 'radio_poly - 2010',
                     '-ffcc_arc': '- ffcc_arc',
                     'envolvente_poly-': 'envolvente_poly -',
                     '-envolvente_poly': '- envolvente_poly',
                     '- 1 Seccion': ' 1 Seccion',
                     '- 3 Seccion': ' 3 Seccion',
                     'Villa Los Llanos - Juarez Celman': 'Villa Los Llanos Juarez Celman'}
    
# ciudades no resuletas en municipedia
IGNORES = [] # usado temporalmente para anotar los que no identifico

# Ciudaes a ignorar en la busqueda de la lista de proyecciones
IGNORES_PROY = []


REPLACES_PROY={u'VILLAS LOS LLANOS - JUAREZ CELMAN': u'Estación Juárez Celman',
               u'VILLA REDUCCION': u'Reducción', u'VILLA OESTE': u'Villa Nueva', 
               u'VILLA QUILINO': u'Quilino', u'SANTA MARIA DE PUNILLA': u'Santa María',
               u'BARRIO NUEVO RIO CEBALLOS': u'Río Ceballos', u'GENERAL PAZ': u'Estación General Paz', 
               u'YOCSINA': u'Malagueño', u'VILLA STA. EUGENIA': u'Alpa Corral', 
               u'SAN IGNACIO  (LOTEO SAN JAVIER)': u'San Ignacio', 
               u'COUNTRY SAN ISIDRO - COUNTRY CHACRAS DE LA VILLA': u'Villa San Isidro', 
               u'BROWN - GUIÑAZU NORTE - 1 DE AGOSTO': u'Estación Juárez Celman',
               u'SANTA MAGDALENA': u'Jovita'}

# reemplazos de municipios que cambian de nombre entre la denominacion que se les 
# dio en el 2008 y en 2010. Necesito que estos dos sean el mismo
REPLACES = {u'Cura Brochero': u'Villa Cura Brochero', 
            u'Cruz de Ca¤a': u'Cruz de Caña',
            u'Ba¤ado de Soto': u'Bañado de Soto',
            u'Cañada de Rio Pinto': u'Cañada de Río Pinto',
            u'De n Funes': u'Deán Funes',
            u'Dean Funes': u'Deán Funes',
            u'Guazimotin': u'Guatimozín',
            u'Guatimozin': u'Guatimozín',
            u'Los Cha¤aritos': u'Los Chañaritos',
            u'Marcos Juarez': u'Marcos Juárez',
            u'Mina clavero': u'Mina Clavero',
            u'Monte Maiz': u'Monte Maíz',
            u'Pozo del molle': u'Pozo del Molle',
            u'Rio Tercero': u'Río Tercero',
            u'Rio Ceballos': u'Río Ceballos',
            u'Transito': u'Tránsito',
            u'Villa dle Totoral': u'Villa del Totoral',
            u'Villa Mar¡a': u'Villa María',
            u'Ca¤ada del Sauce': u'Cañada del Sauce',
            u'Va Cdad Pque Los Reartes': u'Villa Ciudad Parque Los Reartes',
            u'Villa Maria': u'Villa María',
            u'General Paz': u'Estación General Paz',
            u'Villa Los Llanos Juarez Celman': u'Estación Juárez Celman',
            u'Canteras el Sauce': u'Canteras El Sauce'}

# algunas ciudades tienen mapas de diferentes zonas. 
# primero la zona extra, segundo la ciudad a la que corresponde
# se le adapta el nombre para que levi funcione y se agrega un sufijo para el tipo de mapa
# Con esto se creara un nuevo campo para la base de datos en la misma ciudad.
# Hecho asi todos estos mapas extras apareceran como parte de la misma ciudad
EXTRA_MAPS={u'B Nvo Rio Ceballos': {'nombre': u'Río Ceballos', 'tipomapa': u'Barrio Nuevo'},
            u'Va Cdad Pque Los Reartes  1 Seccion': {'nombre': u'Villa Ciudad Parque Los Reartes', 'tipomapa': u'Seccion 1'},
            u'Va Cdad Pque Los Reartes  3 Seccion': {'nombre': u'Villa Ciudad Parque Los Reartes', 'tipomapa': u'Seccion 3'},
            u'Va Ciudad Pque Los Reartes  1 Seccion': {'nombre': u'Villa Ciudad Parque Los Reartes', 'tipomapa': u'Seccion 1b'},
            u'San Ignacio (Loteo Velez Crespo)': {'nombre': u'San Ignacio', 'tipomapa': u'Loteo Velez Crespo'},
            u'San Ignacio (Loteo San Javier)': {'nombre': u'San Ignacio', 'tipomapa': u'Loteo San Javier'},
            u'Country Ch de la Villa-San Isidro': {'nombre': u'Villa San Isidro', 'tipomapa': u'Country Ch'},
            u'Country San Isidro': {'nombre': u'Villa San Isidro', 'tipomapa': u'Country'},
            u'Country Chacras de la Villa': {'nombre': u'Villa Allende', 'tipomapa': u'Country Chacras de la Villa'},
            u'El Potrerillo': {'nombre': u'Alta Gracia', 'tipomapa': u'El Potrerillo'},
            u'La Banda': {'nombre': u'San Marcos Sierras', 'tipomapa': u'La Banda'},
            u'La Travesia': {'nombre': u'Luyaba', 'tipomapa': u'La Travesia'},
            u'Las Chacras': {'nombre': u'La Paz', 'tipomapa': u'Las Chacras'},
            u'Las Corzuelas': {'nombre': u'Mendiolaza', 'tipomapa': u'Las Corzuelas'},
            u'Loma Bola': {'nombre': u'La Paz', 'tipomapa': u'Loma Bola'},
            u'Quebracho Ladeado': {'nombre': u'La Paz', 'tipomapa': u'Quebracho Ladeado'},
            u'Santa Magdalena': {'nombre': u'Jovita', 'tipomapa': u'Santa Magdalena'},
            u'Villa Oeste': {'nombre': u'Villa Nueva', 'tipomapa': u'Villa Oeste'},
            u'Villa Quilino': {'nombre': u'Quilino', 'tipomapa': u'Villa Quilino'},
            u'Villa Santa Eugenia': {'nombre': u'Alpa Corral', 'tipomapa': u'Villa Santa Eugenia'},
            u'Yocsina': {'nombre': u'Malagueño', 'tipomapa': u'Yocsina'},
            }

        
# tipos de archivos detectados leyendo el filename
SHP_TYPES={'canal_ffcc_arc': 'Canal y FFCC',
            'eje_arc': 'Ejes',
            'ejes_arc': 'Ejes',
            'Ejes_arc': 'Ejes',
            'ejes_poly': 'Ejes', # son solo dos
            'embalse_arc': 'Embalse',
            'embalse_ffcc_arc': 'Embalse FFCC',
            'envolente_poly': 'Envolvente',
            'envolv_poly': 'Envolvente',
            'envolvente_arc': 'Envolvente', # solo hay uno y es poly
            'envolvente_poly': 'Envolvente',
            'Envolvente_poly': 'Envolvente',
            'envolventes_poly': 'Envolvente',
            'ffcc': 'FFCC',
            'ffcc_arc': 'FFCC',
            'ffcc_poly': 'FFCC',
            'ffcc_rio_arc': 'FFCC y Rios',
            'ffcc_rios_arc': 'FFCC y Rios',
            'fracc_poly': 'Fracciones',
            'fraccion': 'Fracciones',
            'fraccion_arc': 'Fracciones',
            'fraccion_poly': 'Fracciones',
            'Fraccion_poly': 'Fracciones',
            'fraccion-poly': 'Fracciones',
            'fracicon_poly': 'Fracciones',
            'lagos_ffcc_arc': 'Lagos y FFCC',
            'lagos_rios_arc': 'Lagos y Rios',
            'lagos_rios_ffcc_arc': 'Lagos y Rios',
            'laguna_ffcc_arc': 'Lagunas y FFCC',
            'manz_poly': 'Manzanas',
            'manzana_poly': 'Manzanas',
            'Manzana_poly': 'Manzanas',
            'manzanas_poly': 'Manzanas',
            'manzanaz_poly': 'Manzanas',
            'radio_arc': 'Radios',
            'radio_poly': 'Radios',
            'Radio_poly': 'Radios',
            'radio-poly': 'Radios',
            'radios_poly': 'Radios',
            'rio_arc': 'Rios',
            'rio_ffcc': 'Rios y FFCC',
            'rio_ffcc_arc': 'Rios y FFCC',
            'rio_ffcc_poly': 'Rios y FFCC',
            'rios_arc': 'Rios',
            'rios_dique_arc': 'Rios y Diques',
            'rios_emb_arc': 'Rios y Embalses',
            'rios_embalses_arc': 'Rios y Embalses',
            'Rios_Ffcc_arc': 'Rios y FFCC',
            'rios_ffcc_arc': 'Rios y FFCC',
            'Rios_ffcc_arc': 'Rios y FFCC',
            'rios_ffcc_poly': 'Rios y FFCC',
            'rios_poly': 'Rios',
            }

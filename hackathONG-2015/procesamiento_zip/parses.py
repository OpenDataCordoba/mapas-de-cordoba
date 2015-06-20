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

# ciudades no resuletas en municipedia
IGNORES = [u'Canteras Quilpo', u'Canteras el Sauce', u'Colonia Veinticinco',
           u'Costa Azul', u'Country Chacras de la Villa', u'Dos Arroyos',
           u'El Corcovado-El Torreon', u'El Pantanillo', u'El Potrerillo', 
           u'El Rincon', u'Estacion Lecueder', u'General Paz', u'Jose de la Quintana', 
           u'La Banda', u'La Boca del Rio', u'La Travesia', u'Las Chacras', 
           u'Las Corzuelas', u'Las Mojarras', u'Loma Bola', u'Los Callejones',
           u'Los Molles', u'Parque Norte', u'Quebracho Ladeado', u'Quebrada de los Pozos', 
           u'San Pedro de los Toyos', u'Sanabria', u'Villa Albertina',
           u'Santa Magdalena', u'Villa Berna', u'Villa La Rivera', 
           u'Villa Los Llanos Juarez Celman', u'Villa Oeste', u'Villa Quilino', 
           u'Villa Santa Eugenia', u'Yocsina']

# reemplazos de municipios que cambian de nombre entre la denominacion que se les 
        # dio en el 2008 y en 2010. Necesito que estos dos sean el mismo
REPLACES = {u'Cura Brochero': u'Villa Cura Brochero', 
            u'Cruz de Ca¤a': u'Cruz de Caña',
            u'Ba¤ado de Soto': u'Bañado de Soto',
            u'Cañada de Rio Pinto': u'Cañada de Río Pinto',
            u'De n Funes': u'Dean Funes',
            u'Deán Funes': u'Dean Funes',
            u'Guazimotin': u'Guatimozín',
            u'Guatimozin': u'Guatimozín',
            u'Los Cha¤aritos': u'Los Chañaritos',
            u'Marcos Juarez': u'Marcos Juárez',
            u'Mina clavero': u'Mina Clavero',
            u'Monte Maiz': u'Monte Maíz',
            u'Pozo del molle': u'Pozo del Molle',
            u'Rio Tercero': u'Río Tercero',
            u'Transito': u'Tránsito',
            u'Villa dle Totoral': u'Villa del Totoral',
            u'Villa Mar¡a': u'Villa María',
            u'Ca¤ada del Sauce': u'Cañada del Sauce',
            u'Villa Maria': u'Villa María'}

# algunas ciudades tienen mapas de diferentes zonas. 
# primero la zona extra, segundo la ciudad a la que corresponde
EXTRA_MAPS={u'B Nvo Rio Ceballos': u'Río Ceballos -II',
            u'Va Cdad Pque Los Reartes': u'Villa Ciudad Parque Los Reartes -II',
            u'Va Cdad Pque Los Reartes  1 Seccion': u'Villa Ciudad Parque Los Reartes -III',
            u'Va Cdad Pque Los Reartes  3 Seccion': u'Villa Ciudad Parque Los Reartes -IV',
            u'Va Ciudad Pque Los Reartes  1 Seccion': u'Villa Ciudad Parque Los Reartes -V',
            u'San Ignacio (Loteo Velez Crespo)': u'San Ignacio I',
            u'San Ignacio (Loteo San Javier)': u'San Ignacio II',
            u'Country Ch de la Villa-San Isidro': u'Villa San Isidro I',
            u'Country San Isidro': u'Villa San Isidro II',
            }
        

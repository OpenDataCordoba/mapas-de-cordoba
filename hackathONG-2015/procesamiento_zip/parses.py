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
        

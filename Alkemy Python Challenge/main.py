import csv
import requests
import datetime
import os

import numpy as np
import pandas as pd

import BD
import warnings
warnings.filterwarnings('ignore')  #Evitamos que salgan advertencias no criticas en la terminal
import logging                     #Almacenamos la información util en un archivo .log
logging.basicConfig(filename='info.log',level=logging.INFO,format='%(asctime)s:%(levelname)s:%(message)s')

#Descargaremos los datos en archivos .csv desde sus fuentes

URLS = {'Museos':'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos_datosabiertos.csv',
    'Salas de cine':"https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv",
    'Bibliotecas populares':"https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv"}
now = datetime.datetime.now()  #Almacenamos el momento de la ejecución para ser utilizado a posterior
dirs = {}

for key in URLS:
    response = requests.get(URLS[key], auth=('user', 'pass'))
    if response.status_code == 200:
        response.encoding = 'utf-8'
        os.makedirs(f'{key}/{now.year}-{now.strftime("%B")}', exist_ok=True)
        dir = f'{key}/{now.year}-{now.strftime("%B")}/{key}-{now.day}-{now.month}-{now.year}.csv'
        f = open(dir,'w',encoding='utf-8')
        f.write(response.text)
        f.close()
        logging.info(f'{key}: Descarga exitosa')
        dirs[key]=dir
    elif response.status_code == 404:
        logging.info(f'{key}: Archivo no encontrado')
    else:
        logging.info(f'{key}:Ocurrio un error')

#Creamos los DataFrame con los archivos descargados para su procesamiento

museos = pd.read_csv(dirs['Museos'])
cines = pd.read_csv(dirs['Salas de cine'],na_values=['s/d'])
bibliotecas = pd.read_csv(dirs['Bibliotecas populares'],na_values=['s/d'])

#Creamos los DataFrame vacios que servirán luego para exportar a nuesta base de datos

columns_all_data=['cod_localidad','id_provincia','id_departamento','categoria','provincia','localidad','nombre',
'domicilio','código postal','número de teléfono','mail','web']
all_data=pd.DataFrame(columns=columns_all_data)

columns_description=['Cantidad de registros']
description=pd.DataFrame(columns=columns_description)

columns_movie_summary=['Cantidad de pantallas','Cantidad de butacas','Cantidad de espacios INCAA']
movie_summary=pd.DataFrame(columns=columns_movie_summary)

#Organizaremos los datos de las fuentes para cargar la primera tabla

#1° fuente: Museos (Haremos cada tabla por separado ya que su estructura no es igual por lo que no se puede procesar simultáneamente)
columns_seleccion1=['Cod_Loc','IdProvincia','IdDepartamento',
       'categoria','provincia','localidad','nombre',
       'direccion','CP','cod_area', 'telefono','Mail','Web']
seleccion1=museos[columns_seleccion1]
#Combinaremos las columnas de cod área y teléfono en una sola
seleccion1['cod_area'] = (seleccion1['cod_area'].astype(str)).replace('.0','',regex=True)
seleccion1['telefono'] = seleccion1['telefono'].replace(' ','',regex=True)
seleccion1['telefono'] = '('+seleccion1['cod_area'] + ') ' + seleccion1['telefono']
seleccion1 = seleccion1.drop('cod_area',axis=1)
#Asignamos los nombres deseados a las columnas para poder concatenar todos los registros
seleccion1.columns=columns_all_data
logging.info('Museos: Datos procesados')

#2° fuente: Cines
columns_seleccion2=['Cod_Loc','IdProvincia','IdDepartamento',
       'Categoría','Provincia','Localidad','Nombre',
       'Dirección','CP','cod_area', 'Teléfono','Mail','Web']
seleccion2=cines[columns_seleccion2]
#Combinaremos las columnas de cod area y teléfono en una sola
seleccion2['cod_area'] = (seleccion2['cod_area'].astype(str)).replace('.0','',regex=True)
seleccion2['Teléfono'] = (seleccion2['Teléfono'].astype(str)).replace(' ','',regex=True)
seleccion2['Teléfono'] = (seleccion2['Teléfono'].astype(str)).replace('.0','',regex=True)
seleccion2['Teléfono'] = '('+seleccion2['cod_area'] + ') ' + seleccion2['Teléfono']
seleccion2['Teléfono'].loc[seleccion2['Teléfono']=='(nan) nan'] = np.nan
seleccion2 = seleccion2.drop('cod_area',axis=1)
#Asignamos los nombres deseados a las columnas para poder concatenar todos los registros
seleccion2.columns=columns_all_data
logging.info('Cines: Datos procesados')

#3° fuente: Bibliotecas
columns_seleccion3=['Cod_Loc','IdProvincia','IdDepartamento',
       'Categoría','Provincia','Localidad','Nombre',
       'Domicilio','CP','Cod_tel', 'Teléfono','Mail','Web']
seleccion3=bibliotecas[columns_seleccion3]
#Combinaremos las columnas de cod área y teléfono en una sola
seleccion3['Cod_tel'] = (seleccion3['Cod_tel'].astype(str)).replace('.0','',regex=True)
seleccion3['Teléfono'] = (seleccion3['Teléfono'].astype(str)).replace(' ','',regex=True)
seleccion3['Teléfono'] = (seleccion3['Teléfono'].astype(str)).replace('.0','',regex=True)
seleccion3['Teléfono'] = '('+seleccion3['Cod_tel'] + ') ' + seleccion3['Teléfono']
seleccion3['Teléfono'].loc[seleccion3['Teléfono']=='(nan) nan'] = np.nan
seleccion3 = seleccion3.drop('Cod_tel',axis=1)
#Asignamos los nombres deseados a las columnas para poder concatenar todos los registros
seleccion3.columns=columns_all_data
logging.info('Bibliotecas: Datos procesados')

#Procederemos a concatenar todos nuestros datos en la tabla general, y crearemos el motor de la base de datos para exportar

all_data = pd.concat([seleccion1,seleccion2,seleccion3])
all_data['upload_date'] = now.date()  #Añadimos una columna con la fecha de carga
engine = BD.get_engine()
all_data.to_sql('All data',engine,if_exists='replace')
logging.info('All Data: Tabla sql creada y cargada')

#Procesaremos los datos para completar nuestra tabla Description

#1° consulta: Cantidad de registros totales por categoria
primer_consulta=all_data.categoria.value_counts()
for x in (primer_consulta.index):
    description.loc[x]=[primer_consulta[x]]

#2° consulta: Cantidad de registros totales por fuente
description.loc['Museos']=[museos.size]
description.loc['Cines']=[cines.size]
description.loc['Bibliotecas populares']=[bibliotecas.size]
description

#3° consulta: Cantidad de registros por provincia y categoría
tercera_consulta=all_data.provincia.unique()
for x in tercera_consulta:
    data_provincia = all_data[all_data['provincia']==x]
    cant_provincia=data_provincia.categoria.value_counts()
    for y in (cant_provincia.index):
        description.loc[f'{x}-{y}']=[cant_provincia[y]]

#Procederemos a cargar nuestra nueva tabla a la base de datos
description['upload_date'] = now.date()  #Añadimos una columna con la fecha de carga
description.to_sql('Description',engine,if_exists='replace')
logging.info('Description: Tabla sql creada y cargada')

#Procesaremos el DataFrame cines para crear nuestra tabla movie_summary

provincias=cines.Provincia.unique()
for x in provincias:
    data_provincia = cines[cines['Provincia']==x]
    cant_pantallas = data_provincia.Pantallas.sum()
    cant_butacas = data_provincia.Butacas.sum()
    cant_INCAA = 0
    for e in data_provincia.espacio_INCAA:
        if e:
            cant_INCAA += 1
    movie_summary.loc[x]=[cant_pantallas,cant_butacas,cant_INCAA]

#Procederemos a cargar nuestra nueva tabla a la base de datos
movie_summary['upload_date'] = now.date()  #Añadimos una columna con la fecha de carga
movie_summary.to_sql('Movie Summary',engine,if_exists='replace')
logging.info('Movie Summary: Tabla sql creada y cargada')

logging.info(f'Base de datos creada y actualizada a la fecha de {now.day}-{now.month}-{now.year}')
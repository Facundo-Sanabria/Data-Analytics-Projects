#Este es el módulo donde genero la base de datos y retorno el motor para su utilización en el archivo main.py
#Utilizaremos PostgreSQL (14.4)

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from decouple import config

user,passw,host,port,db = config('user'),config('passw'),config('host'),config('port'),config('db')

def get_engine():
	connection_string=f'postgresql://{user}:{passw}@{host}:{port}/{db}'
	if not database_exists(connection_string):
		create_database(connection_string)
	engine = create_engine(connection_string)
	return engine
�Bienvenidos al desaf�o Alkemy - Challenge Data Analytics!


---Ejecuci�n del proyecto---
Nuestro proyecto realizar� la creaci�n, carga, y actualizaci�n de la base de datos, como tambi�n
la descarga de los archivos fuentes y procesamiento de los datos, de forma autom�tica, todo desde
el archivo main.py, dejando tras su ejecuci�n una base de datos con las tres tablas solicitadas.

---Configuraci�n del entorno---
Este proyecto puede deployarse de forma sencilla con la creaci�n de un entorno virtual, e instalando
en �l las librer�as del archivo requirements.txt mediando pip:

pip install -r requirements.txt 
Importante: Recuerde tener el enterno virtual activado antes de ejecutar la instalaci�n.

Si prefiere no crear un entorno virtual, puede controlar si las librer�as y sus versiones que ya
tenga instaladas sean compatibles con las que necesitaremos, gui�ndose del archivo ya mencionado.

---Configuraci�n de la Base de Datos---
Sqlalquemy utilizara las credenciales de acceso, cargadas como variables de entorno, en la linea 8
(ocho) del archibo BD.py para la creaci�n del motor de nuestra base de datos, variables que no 
estar�n disponibles en un nuevo entorno. Para nuevos entornos, crear en el directorio base del 
proyecto el archivo ".env" y asignar las credencias locales nuevas. Las variables a completar son:

user = 
passw = 
host = 
port = 
db =

Como el archivo principal (main.py) ejecuta las funciones necesarias para actualizar la base
de datos, no es necesario ninguna ejecuci�n previa para la limpieza y carga de informaci�n nueva.

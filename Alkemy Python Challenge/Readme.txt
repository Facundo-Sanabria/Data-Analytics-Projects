¡Bienvenidos al desafío Alkemy - Challenge Data Analytics!


---Ejecución del proyecto---
Nuestro proyecto realizará la creación, carga, y actualización de la base de datos, como también
la descarga de los archivos fuentes y procesamiento de los datos, de forma automática, todo desde
el archivo main.py, dejando tras su ejecución una base de datos con las tres tablas solicitadas.

---Configuración del entorno---
Este proyecto puede deployarse de forma sencilla con la creación de un entorno virtual, e instalando
en él las librerías del archivo requirements.txt mediando pip:

pip install -r requirements.txt 
Importante: Recuerde tener el enterno virtual activado antes de ejecutar la instalación.

Si prefiere no crear un entorno virtual, puede controlar si las librerías y sus versiones que ya
tenga instaladas sean compatibles con las que necesitaremos, guiándose del archivo ya mencionado.

---Configuración de la Base de Datos---
Sqlalquemy utilizara las credenciales de acceso, cargadas como variables de entorno, en la linea 8
(ocho) del archibo BD.py para la creación del motor de nuestra base de datos, variables que no 
estarán disponibles en un nuevo entorno. Para nuevos entornos, crear en el directorio base del 
proyecto el archivo ".env" y asignar las credencias locales nuevas. Las variables a completar son:

user = 
passw = 
host = 
port = 
db =

Como el archivo principal (main.py) ejecuta las funciones necesarias para actualizar la base
de datos, no es necesario ninguna ejecución previa para la limpieza y carga de información nueva.

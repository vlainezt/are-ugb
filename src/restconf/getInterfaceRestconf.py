# Importamos modulos del sistema para leer rutas de carpetas
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(here, "../.."))

sys.path.insert(0, project_root)

# Importamos modulos necesarios para la conexion RESTCONF
import env_workspace 
import requests
import json

# Inhabilitamos advertencias de certificado invalido
requests.packages.urllib3.disable_warnings()

# Creamos variables del nombre de host y el puerto por el corre el RESTCONF
host = env_workspace.IOS_XE_1["host"]
port = env_workspace.IOS_XE_1["restconf_port"]

# Creamos la URL para conectarnos por RESTCONF
url = f"https://{host}:{port}/restconf/data/ietf-interfaces:interfaces"

# Agregamos credenciales basicas nombre de usuario y contraseña
basicAuth = (env_workspace.IOS_XE_1["username"], env_workspace.IOS_XE_1["password"])

# Especificamos el tipo de respuesta que enviaremos y esperamos por parte del servidor tipo JSON
headers = {
    "Accept" : "application/yang-data+json",
    "Content-Type" : "application/yang-data+json" 
}

# Usamos el metodo GET para obtener información del servidor
print("Abriendo la conexión RESTCONF a {}".format(env_workspace.IOS_XE_1["host"]))
send = requests.get(url, auth=basicAuth, headers=headers, verify=False)

# Obtenemos Respuesta del servidor de tipo JSON sin procesar
print("Estos son los datos JSON sin procesar devueltos desde el dispositivo.\n")
json_response = send.json()
print(json.dumps(json_response, indent=2))
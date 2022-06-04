# Importamos modulos del sistema para leer rutas de carpetas
import os
import sys


here = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(here, "../.."))

sys.path.insert(0, project_root)

# Importamos modulos necesarios para la conexion NETCONF
import env_workspace 
from ncclient import manager
import xmltodict
import xml.dom.minidom

# Creamos nuestro filtro NETCONF en tipo XML
netconf_filter = """
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface></interface>
  </interfaces>
</filter>"""

print("Abriendo la conexión NETCONF a {}".format(env_workspace.IOS_XE_1["host"]))

# Abra una conexión al dispositivo de red usando ncclient
with manager.connect(
  host=env_workspace.IOS_XE_1["host"],
  port=env_workspace.IOS_XE_1["netconf_port"],
  username=env_workspace.IOS_XE_1["username"],
  password=env_workspace.IOS_XE_1["password"],
  hostkey_verify=False
  ) as m:
  
  print("Envío de una operación <get-config> al dispositivo.\n")
    # Haga una consulta NETCONF <get-config> usando el filtro
  netconf_reply = m.get_config(source = 'running', filter = netconf_filter)

print("Estos son los datos XML sin procesar devueltos desde el dispositivo.\n")
# Imprima el XML sin procesar que devolvió
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
print("")

# Analizar el XML devuelto a un diccionario ordenado
netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]

# Crear una lista de interfaces
interfaces = netconf_data["interfaces"]["interface"]

print("Estado de las interfaces del dispositivo: ")
# Recorra las interfaces y el estado del informe
for interface in interfaces:
    print("El estado habilitado de la interfaz {} es {}".format(
            interface["name"],
            interface["enabled"]
            )
        )
print("\n")
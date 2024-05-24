import requests
import os
from dotenv import load_dotenv
import time
from scrappingCore import crear_estaciones
import datetime
import json
import sqlite3
import unidecode

load_dotenv()
TOKEN=os.getenv("ENV_TOKEN")

# Creando una lista de alertas accediendo a la base de datos de las alertas
conexion=sqlite3.connect("bbdd.db") 
cursor=conexion.execute("select codigo,id_usuario,meteo,lindar,valor,localidad from alertas")

alertas_bbdd=[]
for alerta_bbdd in cursor:
    alertas_bbdd.append(alerta_bbdd)
conexion.close()


# Recorriendo 
for alerta_bbdd in alertas_bbdd:
    id_user = alerta_bbdd[1]

    text="✉️  Notificació general  \nEs van a borrar en breus les alertes que teniu guardades perque la base de dades va a ser modificada per a afegir mes funcionalitats, disculpeu les molesties, podreu configurarles de nou en uns dies."

    requests.post("https://api.telegram.org/bot"+TOKEN+"/sendMessage", data={"chat_id":id_user,"text":text})
    print("va ok" + str(id_user))

    time.sleep(1)


    #text="/alerta_crear vent superior 1 Sueca \n/alerta_crear vent inferior 100 Sueca \n/alerta_crear estat Sueca"


    #requests.post("https://api.telegram.org/bot"+TOKEN+"/sendMessage", data={"text":text})


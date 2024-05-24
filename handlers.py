import sqlite3
import unidecode
import requests
import os
from dotenv import load_dotenv
from colorama import init, Fore, Back, Style
from clases import Estacion

load_dotenv()
TOKEN=os.getenv("ENV_TOKEN")


def normalizar_argumentos_provisional(argumentos):

    meteo = argumentos["meteo"]
    meteo = unidecode.unidecode(meteo)
    meteo = meteo.lower()

    
    lindar = argumentos["lindar"]
    if lindar != "null":
        lindar = unidecode.unidecode(lindar)
        lindar = lindar.lower()
        if lindar != "superior" and lindar != "inferior":
            return print("Lindar debe ser superior o inferior")
    
   
    valor = argumentos["valor"]
    if valor != "null":
        valor = unidecode.unidecode(valor)
        valor = valor.replace(",",".")
        valor = float(valor)


    localidad = argumentos["localidad"]
    localidad = ' '.join(localidad) #puede contener varias palabras
    localidad = unidecode.unidecode(localidad)
    localidad = localidad.lower()

    user_id = argumentos["user_id"]
    
    argumentos_normalizados = { "user_id":user_id,                  # Extrae la id del usuario que desea programar la alerta 
                                "meteo":meteo,                      # Se establece el tipo de alerta 
                                "lindar":lindar,                    # La alerta por lluvia siempre va a ser por lindar superior
                                "valor":valor,                      # Extrae el valor                                                     
                                "localidad":localidad,              # La localidad puede contener varias palabras
                                "partida":argumentos["partida"],
                                "subpartida":argumentos["subpartida"],
                                "fecha":argumentos["fecha"],
                                "tipoalerta":argumentos["tipoalerta"],
                                "activa":argumentos["activa"]
                }

    return argumentos_normalizados


def almacenador_de_alertas_provisional(argumentos):

    conexion=sqlite3.connect("bbdd.db")  
    conexion.execute("insert into alertas(id_usuario,meteo,lindar,valor,localidad,partida,subpartida,fecha,tipoalerta,activa) values (?,?,?,?,?,?,?,?,?,?)", (argumentos["user_id"],argumentos["meteo"],argumentos["lindar"],argumentos["valor"],argumentos["localidad"],argumentos["partida"],argumentos["subpartida"],argumentos["fecha"],argumentos["tipoalerta"],argumentos["activa"]))
    conexion.commit()
    conexion.close()


def enviar_alerta_a_usuario(alerta_bbdd,estacion):

    """
    Funcion que comprueba si hay alguna alerta programada que se cumple, para ello utiliza como parametros.

    -alerta: la alerta de la bbdd
    -estacion: la estacion a checkear

    """

    # Se normalizan los datos
    localidad_json = estacion.localidad
    localidad_json = unidecode.unidecode(localidad_json)
    localidad_json = localidad_json.lower()

    localidad_bbdd = alerta_bbdd[5]
    localidad_bbdd = unidecode.unidecode(localidad_bbdd)
    localidad_bbdd = localidad_bbdd.lower()

    meteo_bbdd = alerta_bbdd[2]
    meteo_bbdd = unidecode.unidecode(meteo_bbdd)
    meteo_bbdd = meteo_bbdd.lower()

    superioroinferior_bbdd = alerta_bbdd[3]
    if superioroinferior_bbdd != "null":
        superioroinferior_bbdd = unidecode.unidecode(superioroinferior_bbdd)
        superioroinferior_bbdd = superioroinferior_bbdd.lower()
 
    valor_bbdd = alerta_bbdd[4]
    if valor_bbdd != "null":
        valor_bbdd = float(valor_bbdd)

    ################################### Se comprueban las alertas de precipitacion ###################################

    if localidad_bbdd == localidad_json and meteo_bbdd == "pluja":


        if estacion.precipitacion == "null":
            return print(Fore.YELLOW + "Las alertas de " + meteo_bbdd + " de " + estacion["localidad"]+ " " + estacion["partida"] + " " + estacion["subpartida"] + " no pueden ser ejecutadas porque el valor de la estacion es nulo" + Fore.RESET)                   
        else:
            estacion_estaciones = float(estacion["precipitacion"])
                                
        estacion_bbdd = float(alerta_bbdd[4])

        if estacion_estaciones > estacion_bbdd:

            text="☔️  Alerta de plutja de mes de " + str(alerta_bbdd[4]) + " en: \n " + estacion["localidad"]+ " " + estacion["partida"] + " " + estacion["subpartida"]

            requests.post("https://api.telegram.org/bot"+TOKEN+"/sendMessage", data={"chat_id":alerta_bbdd[1],"text":text})

            codigo = alerta_bbdd[0]

            conexion=sqlite3.connect("bbdd.db") 
            cursor=conexion.execute("select codigo,id_usuario,meteo,lindar,valor,localidad from alertas")
            cursor.execute("DELETE FROM alertas WHERE codigo=?", (codigo,))
            conexion.commit()
            conexion.close()


################################### Se comprueban las alertas de temperatura ###################################

    if localidad_bbdd == localidad_json and meteo_bbdd == "temperatura" and superioroinferior_bbdd == "superior":

        if estacion["temperatura"] == "null":
            return print("Las alertas de " + meteo_bbdd + " de " + estacion["localidad"]+ " " + estacion["partida"] + " " + estacion["subpartida"] + " no pueden ser ejecutadas porque el valor de la estacion es nulo")
        else:
            estacion_estaciones = float(estacion["temperatura"])
            estacion_bbdd = float(alerta_bbdd[4])


        if estacion_estaciones > estacion_bbdd:
                                             
            text="☀️  Alerta de temperatura per mes de " + str(alerta_bbdd[4]) + " en: \n " + estacion["localidad"]+ " " + estacion["partida"] + " " + estacion["subpartida"]

            requests.post("https://api.telegram.org/bot"+TOKEN+"/sendMessage", data={"chat_id":alerta_bbdd[1],"text":text})

            codigo = alerta_bbdd[0]

            conexion=sqlite3.connect("bbdd.db") 
            cursor=conexion.execute("select codigo,id_usuario,meteo,lindar,valor,localidad from alertas")
            cursor.execute("DELETE FROM alertas WHERE codigo=?", (codigo,))
            conexion.commit()
            conexion.close()
                                            



    if localidad_bbdd == localidad_json and meteo_bbdd == "temperatura" and superioroinferior_bbdd == "inferior":
                                
        if estacion["temperatura"] == "null":
            return print("Las alertas de " + meteo_bbdd + " de " + estacion["localidad"]+ " " + estacion["partida"] + " " + estacion["subpartida"] + " no pueden ser ejecutadas porque el valor de la estacion es nulo")
        else:
            estacion_estaciones = float(estacion["temperatura"])
            estacion_bbdd = float(alerta_bbdd[4])

                                         
        if estacion_estaciones < estacion_bbdd:

            text="❄️  Alerta de temperatura per menys de " + str(alerta_bbdd[4]) + " en: \n " + estacion["localidad"]+ " " + estacion["partida"] + " " + estacion["subpartida"]

            requests.post("https://api.telegram.org/bot"+TOKEN+"/sendMessage", data={"chat_id":alerta_bbdd[1],"text":text})

            codigo = alerta_bbdd[0]


            conexion=sqlite3.connect("bbdd.db") 
            cursor=conexion.execute("select codigo,id_usuario,meteo,lindar,valor,localidad from alertas")
            cursor.execute("DELETE FROM alertas WHERE codigo=?", (codigo,))
            conexion.commit()
            conexion.close()


################################### Se comprueban las alertas de viento ###################################

    if localidad_bbdd == localidad_json and meteo_bbdd == "vent" and superioroinferior_bbdd == "superior":

        if estacion["viento"] == "null":
            return print("Las alertas de " + meteo_bbdd + " de " + estacion["localidad"]+ " " + estacion["partida"] + " " + estacion["subpartida"] + " no pueden ser ejecutadas porque el valor de la estacion es nulo")
        else:
            estacion_estaciones = float(estacion["viento"])
            estacion_bbdd = float(alerta_bbdd[4])
                                         
        if estacion_estaciones > estacion_bbdd:
                                             

            text="💨  Alerta de vent superior a " + str(alerta_bbdd[4]) + " en: \n " + estacion["localidad"]+ " " + estacion["partida"] + " " + estacion["subpartida"]

            requests.post("https://api.telegram.org/bot"+TOKEN+"/sendMessage", data={"chat_id":alerta_bbdd[1],"text":text})

            codigo = alerta_bbdd[0]


            conexion=sqlite3.connect("bbdd.db") 
            cursor=conexion.execute("select codigo,id_usuario,meteo,lindar,valor,localidad from alertas")
            cursor.execute("DELETE FROM alertas WHERE codigo=?", (codigo,))
            conexion.commit()
            conexion.close()
                                            



    if localidad_bbdd == localidad_json and meteo_bbdd == "vent" and superioroinferior_bbdd == "inferior":
                                
        if estacion["viento"] == "null":
            return print("Las alertas de " + meteo_bbdd + " de " + estacion["localidad"]+ " " + estacion["partida"] + " " + estacion["subpartida"] + " no pueden ser ejecutadas porque el valor de la estacion es nulo")
        else:
            estacion_estaciones = float(estacion["viento"])
            estacion_bbdd = float(alerta_bbdd[4])
                                         
        if estacion_estaciones < estacion_bbdd:
                                             

            text="💨  Alerta de vent inferior a " + str(alerta_bbdd[4]) + " en: \n " + estacion["localidad"]+ " " + estacion["partida"] + " " + estacion["subpartida"]

            requests.post("https://api.telegram.org/bot"+TOKEN+"/sendMessage", data={"chat_id":alerta_bbdd[1],"text":text})

            codigo = alerta_bbdd[0]


            conexion=sqlite3.connect("bbdd.db") 
            cursor=conexion.execute("select codigo,id_usuario,meteo,lindar,valor,localidad from alertas")
            cursor.execute("DELETE FROM alertas WHERE codigo=?", (codigo,))
            conexion.commit()
            conexion.close()


################################### Se comprueban las alertas de estado ###################################

    if localidad_bbdd == localidad_json and meteo_bbdd == "estat" and estacion["estado"] == False:
                        


        text="🆘  Alerta de estacio sense actualitzar en: \n " + estacion["localidad"]+ " " + estacion["partida"] + " " + estacion["subpartida"]

        requests.post("https://api.telegram.org/bot"+TOKEN+"/sendMessage", data={"chat_id":alerta_bbdd[1],"text":text})

        codigo = alerta_bbdd[0]


        conexion=sqlite3.connect("bbdd.db") 
        cursor=conexion.execute("select codigo,id_usuario,meteo,lindar,valor,localidad from alertas")
        cursor.execute("DELETE FROM alertas WHERE codigo=?", (codigo,))
        conexion.commit()
        conexion.close()

    
def comprueba_si_existe_la_localidad_provisional(argumentos,estaciones):

    existe = False

    for estacion in estaciones:
        estacion_localidad = estacion["localidad"]
        estacion_localidad = unidecode.unidecode(estacion_localidad)
        estacion_localidad = estacion_localidad.lower()

        if str(argumentos["localidad"]) == str(estacion_localidad):
            existe = True

    return existe
                                            
                                

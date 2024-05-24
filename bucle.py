import requests
import os
from dotenv import load_dotenv
import time
from scrappingCore import crear_estaciones
import datetime
import json
import sqlite3
from colorama import init, Fore, Back, Style

from handlers import enviar_alerta_a_usuario
from clases import Estacion, Alerta

load_dotenv()
TOKEN=os.getenv("ENV_TOKEN")


def bucle():

    while 1:
        try:
            # Obteniendo las estaciones
            estaciones = crear_estaciones()
            # Obteniendo alertas
            alertas = Alerta.obtener_desde_ddbb()    

            # Extrayendo diccionario a json
            lista_de_estaciones = []
            for estacion in estaciones:
                estacion = estacion.estacion_to_dict()
                lista_de_estaciones.append(estacion)
            archivo = open("estaciones.json", "w")
            json.dump(lista_de_estaciones,archivo)
            archivo.close()
      
            # Se recorre la lista de alertas y por cada alerta se recorre la lista de estaciones para ver si alguna de ellas supera el lindar de la alerta.
            print( Fore.BLUE + "Iniciando el envio de alertas al usuario" + Fore.RESET)  
            for alerta in alertas:
                for estacion in estaciones:
                    if alerta.meteo == "pluja" and alerta.localidad == estacion.localidad and alerta.valor < estacion.precipitacion:
                        print (estacion)
                    if alerta.meteo == "temperatura" and alerta.localidad == estacion.localidad and alerta.valor < estacion.temperatura:
                        print (estacion)
                    if alerta.meteo == "temperatura" and alerta.localidad == estacion.localidad and alerta.valor > estacion.temperatura:
                        print (estacion)
                    if alerta.meteo == "estat" and alerta.localidad == estacion.localidad and alerta.valor < estacion.temperatura:
                        print (estacion)
        except: pass                    
    time.sleep(120)





"""try:pass#enviar_alerta_a_usuario(alerta,estacion)
                    except: print(Fore.RED + "\nError al intentar enviar alerta a usuario: " + str(alerta) + "\n \n" + str(estacion)+ "\n" + Fore.RESET)
                    pass"""
"""           print(Fore.BLUE + "Finalizado el envio de alertas al usuario" + Fore.RESET)
            print("")
        except: pass
        

        # Comprueba que la última actualización no tiene mas de 3 minutos respecto a la anterior, eso significaría que no se actualiza correctamente.
        try:
            for estacion in estaciones:
                actualizacion_actual = str(datetime.datetime.now())
                actualizacion_pasada = str(estacion["actualizacion"])

                actualizacion_actual = int(actualizacion_actual[14:16])
                actualizacion_pasada = int(actualizacion_pasada[14:16])

                if (actualizacion_actual - actualizacion_pasada) > 3:
                    print(str(Fore.RED + actualizacion_pasada + " " + estacion["localidad"] + Fore.RESET))
        except: pass



        print("------------- FIN DE BUCLE ------------- ")
        print("")
"""

    

  


if __name__=="__main__":

    bucle()


                            
        
        














        

        

        
        







        

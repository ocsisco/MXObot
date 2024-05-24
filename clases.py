import datetime
import sqlite3

class Estacion():

    def __init__(self):
        self.localidad = "localidad"
        self.partida = "partida"
        self.subpartida = "subpartida"
        self.temperatura = "temperatura"
        self.temperatura_min = "temperatura_min"
        self.temperatura_max = "temperatura_max"
        self.precipitacion = "precipitacion"
        self.humedad_relativa = "humedad_relativa"
        self.viento = "viento"
        self.estado = "estado"
        self.actualizacion = str(datetime.datetime.now())

    def dict_to_estacion(self,diccionario):
        self.localidad = diccionario["localidad"]
        self.partida = diccionario["partida"]
        self.subpartida = diccionario["subpartida"]
        self.temperatura = diccionario["temperatura"]
        self.temperatura_min = diccionario["temperatura_min"]
        self.temperatura_max = diccionario["temperatura_max"]
        self.precipitacion = diccionario["precipitacion"]
        self.humedad_relativa = diccionario["humedad_relativa"]
        self.viento = diccionario["viento"]
        self.estado = diccionario["estado"]
        self.actualizacion = str(datetime.datetime.now())

    def estacion_to_dict(self):
        estacion = {
        "localidad": self.localidad,
        "partida": self.partida,
        "subpartida": self.subpartida,
        "temperatura": self.temperatura,
        "temperatura_min": self.temperatura_min,
        "temperatura_max": self.temperatura_max,
        "precipitacion": self.precipitacion,
        "humedad_relativa": self.humedad_relativa,
        "viento": self.viento,
        "estado": self.estado,
        "actualizacion":str(datetime.datetime.now())
        }
        return estacion
    
    def __str__(self):
        localidad = self.localidad
        partida = self.partida
        subpartida = self.subpartida
        return "Estación de: " + localidad + " " + partida + " " + subpartida


class Alerta():

    def __init__(self):
        self.localidad = "localidad"
        self.partida = "partida"
        self.subpartida = "subpartida"
        self.meteo = "meteo"
        self.lindar = "lindar"
        self.valor = "valor"
        self.tipoalerta = "tipoalerta"
        self.activa = False
        self.fecha = str(datetime.datetime.now())
        self.codigo = "codigo"
        self.id_usuario = "id_usuario"

    def dict_to_alerta(self,diccionario):
        self.localidad = diccionario["localidad"]
        self.partida = diccionario["partida"]
        self.subpartida = diccionario["subpartida"]
        self.meteo = diccionario["meteo"]
        self.lindar = diccionario["lindar"]
        self.valor = diccionario["valor"]
        self.tipoalerta = diccionario["tipoalerta"]
        self.activa = diccionario["activa"]
        self.fecha = str(datetime.datetime.now())
        self.codigo = diccionario["codigo"]
        self.id_usuario = ["id_usuario"]

    def alerta_to_dict(self):
        alerta = {
        "localidad": self.localidad,
        "partida": self.partida,
        "subpartida": self.subpartida,
        "meteo": self.meteo,
        "lindar": self.lindar,
        "valor": self.valor,
        "tipoalerta": self.tipoalerta,
        "activa": self.activa,
        "fecha": self.fecha,
        "codigo": self.codigo,
        "id_usuario":str(datetime.datetime.now())
        }
        return alerta


    def __str__(self):
        localidad = self.localidad
        partida = self.partida
        subpartida = self.subpartida
        return "Alerta de: " + localidad + " " + partida + " " + subpartida

    @staticmethod
    def obtener_desde_ddbb():       
        # Obteniendo una lista de alertas accediendo a la base de datos de las alertas
        conexion=sqlite3.connect("bbdd.db") 
        cursor=conexion.execute("select codigo,id_usuario,meteo,lindar,valor,localidad,partida,subpartida,fecha,tipoalerta,activa from alertas")
        alertas=[]
        for alerta_db in cursor:
            # Creando y llenando de datos el objeto alerta
            alerta = Alerta()
            alerta.codigo       =alerta_db[0]
            alerta.id_usuario   =alerta_db[1]
            alerta.meteo        =alerta_db[2]
            alerta.lindar       =alerta_db[3]
            alerta.valor        =alerta_db[4]
            alerta.localidad    =alerta_db[5]
            alerta.partida      =alerta_db[6]
            alerta.subpartida   =alerta_db[7]
            alerta.fecha        =alerta_db[8]
            alerta.tipoalerta   =alerta_db[9]
            alerta.activa       =alerta_db[10]
                    
            # Añadiendo la alerta a la lista de alertas
            alertas.append(alerta)
        conexion.close()
        return alertas


    def subir_a_ddbb():
        pass

    
    @property
    def comprobar_si_localidad_existe():

        pass


import datetime
from colorama import Fore
from scrappingFunctions import extract_datasets_en_bruto_de_estaciones, extractor_de_datos_de_dataset
from clases import Estacion






def crear_estaciones():

    # Creando la lista para poner los objetos estacion
    estaciones = []

    # Extrae de la url una lista de datasets donde cada elemento es un bloque de cada una de las estaciones
    try: datasets = extract_datasets_en_bruto_de_estaciones()    
    except: print(Fore.RED + "No se ha podido efectuar la request a la URL" + Fore.RESET)

    # Recorre la lista de datasets y extrae de ellos la informacion relevante en forma de diccionario
    for dataset in datasets:
        estacion_diccionario = extractor_de_datos_de_dataset(dataset)
        # Crea objeto estación
        estacion = Estacion()
        # Rellena la estacion de datos introduciendo el diccionario
        estacion.dict_to_estacion(estacion_diccionario)
        # Añade los objetos de la clase estacion a una lista de estaciones.
        estaciones.append(estacion)
        
    print(Fore.GREEN + "Actualizadas las estaciones " + str(datetime.datetime.now()) + Fore.RESET)
    print("")

    return estaciones




#### TESTING ###

if __name__=="__main__":

    estaciones = crear_estaciones()
    for estacion in estaciones:
        print (estacion)
        print (str(estacion.partida))
        print (str(estacion.subpartida))
        print (str(estacion.temperatura))
        print (str(estacion.temperatura_min))
        print (str(estacion.temperatura_max))
        print (str(estacion.humedad_relativa))
        print("___________________________")

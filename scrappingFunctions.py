import requests
import time
import datetime
from bs4 import BeautifulSoup
from colorama import Fore
import pprint





def extract_datasets_en_bruto_de_estaciones():

    """
    Extrae del bloque de el conjunto de datos de la request, bloques separados por estaciones

    """


    # Url de la MXO
    url = "https://www.avamet.org/mxo-meteoxarxaonline.html"

    # Palabras que contienen los bloques que no son estaciones y por lo tanto superfluos
    keywords = ["resetOrdre","rVal sortable","ocultarFilera","estacions operatives actualitzades","Zones limítrofes"]

    r = requests.get(url)
    time.sleep(5)

    # Extrae el html de la página y lo separa en bloques por estaciones.
    soup = BeautifulSoup(r.content, "html.parser")
    results = soup.find_all('div', class_='estacions')
    results = str(results)
    results = results.split("</tr>")

    # Borra los bloques que no pertenecen a las estaciones.
    newresults = []
    for result in results:
        okresult = True
        for keyword in keywords:
            if keyword in result:
                okresult = False
        if okresult:
            newresults.append(result)

    estaciones = newresults

    return estaciones


def extractor_de_datos_de_dataset(dataset):

    """ 
    Limpia los datos del dataset en bruto y devuelve diccionario con los datos de la estación

    """

    try:
        #limpiando localidad
        localidad = dataset.split("href")
        localidad = localidad[1]
        localidad = localidad.split(">") 
        localidad = localidad[1]
        localidad = localidad.split("<span")
        localidad = localidad[0]
        localidad = localidad.rstrip()
        localidad = localidad.lstrip()
    except: print("El scrapeador no ha podido extraer la localidad" + str(localidad))

    try:
        #limpiando partida
        partida = dataset.split(localidad)
        partida = partida[1]
        partida = partida.split('ptda">')
        partida = partida[1]
        partida = partida.split("</span>")
        partida = partida[0]
    except: print("El scrapeador no ha podido extraer la partida" +str(localidad) + "/" +str(partida))

    try:
        #limpiando subpartida.
        #no siempre hay subpartida y por ello queda fuera del rango a veces "out of list" por eso try 
        subpartida = dataset.split(localidad)
        subpartida = subpartida[1]
        subpartida = subpartida.split('ptda">')
        subpartida = subpartida[1]
        subpartida = subpartida.split("</span>")
    except: print("El scrapeador no ha podido extraer la subpartida 1" +str(localidad)+ "/" +str(partida)+ "/" +str(subpartida))
    try:
        if str(localidad) == "Nules" and str(partida) == "Platja de " :
            subpartida = "L'Estany"
        else:
            subpartida = subpartida[1]
            subpartida = subpartida.split("<img")
            subpartida = subpartida[0]
    except: print("El scrapeador no ha podido extraer la subpartida 2" +str(localidad)+ "/" +str(partida)+ "/" +str(subpartida))

    try:
        #limpiando temperatura actual
        temperatura = dataset.split("rValm")
        temperatura = temperatura[1]
        temperatura = temperatura.split(">")
        temperatura = temperatura[1]
        temperatura = temperatura.split("</td")
        temperatura = temperatura[0]
        temperatura = temperatura.replace(",",".")
        temperatura = temperatura.rstrip()
        temperatura = temperatura.lstrip()
    except: print("El scrapeador no ha podido extraer la temperatura actual" +str(localidad)+ "/" +str(partida)+ "/" +str(subpartida)+ "/" +str(temperatura))

    try:
        #limpiando temperatura minima
        temperatura_min = dataset.split('"rValn">')
        temperatura_min = temperatura_min[1]
        temperatura_min = temperatura_min.split("<")
        temperatura_min = temperatura_min[0]
    except: print("El scrapeador no ha podido extraer la temperatura minima" +str(localidad)+ "/" +str(partida)+ "/" +str(subpartida)+ "/" +str(temperatura_min))

    try:
        #limpiando temperatura maxima
        temperatura_max = dataset.split('"rValx">')
        temperatura_max = temperatura_max[1]
        temperatura_max = temperatura_max.split("<")
        temperatura_max = temperatura_max[0]
        temperatura_max = temperatura_max.replace(",",".")
        temperatura_max = temperatura_max.rstrip()
        temperatura_max = temperatura_max.lstrip()
    except: print("El scrapeador no ha podido extraer la temperatura maxima" +str(localidad)+ "/" +str(partida)+ "/" +str(subpartida)+ "/" +str(temperatura_max))

    try:
        #limpiando precipitacion
        precipitacion = dataset.split("rValm")
        precipitacion = precipitacion[2]
        precipitacion = precipitacion.split(">")
        precipitacion = precipitacion[1]
        precipitacion = precipitacion.split("</td")
        precipitacion = precipitacion[0]
        precipitacion = precipitacion.replace(",",".")
        precipitacion = precipitacion.rstrip()
        precipitacion = precipitacion.lstrip()
        if not precipitacion:
            precipitacion = "null"
    except: print("El scrapeador no ha podido extraer la precipitacion" +str(localidad)+ "/" +str(partida)+ "/" +str(subpartida)+ "/" +str(precipitacion))

    try:
        #limpiando humedad relativa
        humedad = dataset.split("rVal color")
        humedad = humedad[1]
        humedad = humedad.split(">")
        humedad = humedad[1]
        humedad = humedad.split("</td")
        humedad = humedad[0]
    except: print("El scrapeador no ha podido extraer la temperatura" +str(localidad)+ "/" +str(partida)+ "/" +str(subpartida)+ "/" +str(humedad))

    try:
        #limpiando viento
        viento = str(dataset)
        viento = dataset.split("rval color")
        viento = viento[0]
        viento = viento.split("<!--")
        viento = viento[1]
        viento = viento.split("<td class=")
        viento = viento[5]
        viento = viento.split('"rVal">')
        viento = viento[1]
        viento = viento.split("</td>")
        viento = viento[0]
        if not viento:
            viento="null"
    except: print("")#"El scrapeador no ha podido extraer el viento" +str(localidad)+ "/" +str(partida)+ "/" +str(subpartida)+ "/" +str(viento))

    try:
        #limpiando estado
        estado = False
        if "imatges/mxo/icones/icon_clock.gif" in dataset:
            estado = True
    except: print("El scrapeador no ha podido obtener el estado" +str(localidad)+ "/" +str(partida)+ "/" +str(subpartida)+ "/" +str(estado))
        
    try:
        localidad = str(localidad)
        partida = str(partida)
        subpartida = str(subpartida)

        estacion_diccionario = {
            "localidad":localidad,
            "partida":partida,
            "subpartida":subpartida,
            "temperatura":temperatura,
            "temperatura_min":temperatura_min,
            "temperatura_max":temperatura_max,
            "precipitacion":precipitacion,
            "humedad_relativa":humedad,
            "viento":viento,
            "estado":estado,
            "actualizacion":str(datetime.datetime.now())
            }
    except:
            print(Fore.RED + "El scrapeador no ha podido guardar el diccionario" +str(localidad)+ " " +str(partida)+ " " +str(subpartida) + Fore.RESET)
            print("")

    return estacion_diccionario






#### TESTING ####

if __name__=="__main__":

    datasets = extract_datasets_en_bruto_de_estaciones()

    #pprint.pprint(datasets[10])

    for dataset in datasets:
        estacion = (extractor_de_datos_de_dataset(dataset))
        pprint.pprint(estacion)
        print(" ")

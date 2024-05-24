from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
import unidecode
import datetime
import os
from multiprocessing import Process
import json
import sqlite3
from dotenv import load_dotenv

from bucle import bucle
from clases import Alerta
from handlers import normalizar_argumentos_provisional,almacenador_de_alertas_provisional,comprueba_si_existe_la_localidad_provisional


load_dotenv()
TOKEN=os.getenv("ENV_TOKEN")



conexion=sqlite3.connect("bbdd.db")
conexion.execute("""create table if not exists alertas (
                        codigo integer primary key AUTOINCREMENT, 
                        id_usuario,
                        meteo,
                        lindar,
                        valor,
                        localidad,
                        partida,
                        subpartida,
                        fecha,
                        tipoalerta,
                        activa   
)""")
conexion.close()



if __name__ == "__main__":
    generate_images = Process(target=bucle)
    generate_images.start()
    print("Ejecutando programa principal")



async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Benvingut {update.effective_user.first_name} aci et deixe uns exemples de els comandaments a emprar i com fer-los funcionar')
    await update.message.reply_text("VISUALITZACIO DE DADES PER LOCALITAT:\n \n/out (Estacions que no actualitzen)\n/temp (Temperatura actual, mínima i màxima)\n/tempact (Temperatura actual)\n/tempmin (Temperatura mínima)\n/tempmax (Temperatura màxima)\n/pluja (Acumulat de pluja diaria)\n .")
    await update.message.reply_text("ALERTES:\n \nCrear alertes:\n/alerta_pluja\n/alerta_temperatura\n/alerta_vent\n/alerta_estat\n \nVisualitzar alertes:\n/alerta\n \nBorrar alertes:\n/alerta_borrar\n .")


    hora_actual = datetime.datetime.now()
    print(hora_actual)
    print((str(context._user_id))+("/ajuda"))
    print(" ")


async def data_act(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    archivo = open("estaciones.json", "r")
    estaciones = json.load(archivo)
    data_act = estaciones[0]["actualizacion"]

    await update.message.reply_text(str('📎  '+str(data_act)))



############## Visualització ############## 


async def estaciones_out(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    archivo = open("estaciones.json", "r")
    estaciones = json.load(archivo)
    presencia_estaciones_out=False

    for estacion in estaciones:
        
        if not estacion["estado"]:

            presencia_estaciones_out = True

            await update.message.reply_text("🆘  "+estacion["localidad"]+" "+estacion["partida"]+" "+estacion["subpartida"])


    if presencia_estaciones_out == False:

        await update.message.reply_text("Todas las estaciones de la MXO funcionan correctamente")

        

    hora_actual = datetime.datetime.now()
    print(hora_actual)
    print((str(context._user_id))+("/estaciones out"))
    print(" ")


async def temperatura(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    archivo = open("estaciones.json", "r")
    estaciones = json.load(archivo)
    
    #adquiriendo argumentos de el comando y comprobando que no están vacíos
    peticion_de_estacion = context.args
    peticion_de_estacion = " ".join(peticion_de_estacion)
    existe_dato = True
    existe_estacion = False

    if peticion_de_estacion == "":
        existe_dato = False
        await update.message.reply_text(str('📎  Introdueix el comandament seguit de un espai i la localitat \n(per exemple "/temp Sueca")'))


    #creando las estaciones


    for estacion in estaciones:
        
        def normalizar_strings(estacion):

            estacion_normalizada = estacion["localidad"]
            estacion_normalizada = unidecode.unidecode(estacion_normalizada)
            peticion_de_estacion_normalizada = unidecode.unidecode(peticion_de_estacion)
            estacion_normalizada = estacion_normalizada.lower()
            peticion_de_estacion_normalizada = peticion_de_estacion_normalizada.lower()

            return estacion_normalizada,peticion_de_estacion_normalizada
        
        #Quitando tildes y carácteres extraños, tanto de el argumento como de la lista de estaciones
        valores_normalizados = normalizar_strings(estacion)
        estacion_normalizada = valores_normalizados[0]
        peticion_de_estacion_normalizada = valores_normalizados[1]

        #comparando si el argumento i la estacion son iguales
        if estacion_normalizada == peticion_de_estacion_normalizada:

            existe_estacion=True
            if estacion["estado"]:
                icono = "✅"
            else: icono = "🆘"

            if estacion["temperatura"] == "null":
                estacion["temperatura"] = "❓"
            if estacion["temperatura_min"] == "null":
                estacion["temperatura_min"] = "❓"
            if estacion["temperatura_max"] == "null":
                estacion["temperatura_max"] = "❓"
            

                

            await update.message.reply_text(str(icono+"  "+estacion["partida"]+" "+estacion["subpartida"]+"\n" + "Actual "+estacion["temperatura"]+"ºC"  "\n" "Mínima "+estacion["temperatura_min"]+"ºC" "\n"  "Máxima "+estacion["temperatura_max"]+"ºC"))

    if not existe_estacion and existe_dato:

        await update.message.reply_text(str("No existeixen estacions de la MXO en aquesta localitat"))


    hora_actual = datetime.datetime.now()
    print(hora_actual)
    print((str(context._user_id))+("/temperatura/")+(peticion_de_estacion_normalizada))
    print(" ")


async def temperatura_actual(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    archivo = open("estaciones.json", "r")
    estaciones = json.load(archivo)
    
    peticion_de_estacion = context.args
    peticion_de_estacion = " ".join(peticion_de_estacion)
    existe_dato = True

    if peticion_de_estacion == "":
        existe_dato = False
        
        await update.message.reply_text(str('📎  Introdueix el comandament seguit de un espai i la localitat \n(per exemple "/tempact Sueca")'))

    existe_estacion = False


    
    for estacion in estaciones:

        #Quitando tildes y carácteres extraños
        estacion_normalizada = estacion["localidad"]
        estacion_normalizada = unidecode.unidecode(estacion_normalizada)
        peticion_de_estacion_normalizada = unidecode.unidecode(peticion_de_estacion)
        estacion_normalizada = estacion_normalizada.lower()
        peticion_de_estacion_normalizada = peticion_de_estacion_normalizada.lower()

        if estacion_normalizada == peticion_de_estacion_normalizada:
            existe_estacion=True

            if estacion["estado"]:
                icono = "✅"
            else: icono = "🆘"

            await update.message.reply_text(str(icono+"  "+estacion["partida"]+" "+estacion["subpartida"]+"\n" + "Actual "+estacion["temperatura"]+"ºC"))

    if not existe_estacion and existe_dato:

        await update.message.reply_text(str("No existeixen estacions de la MXO en aquesta localitat"))

    hora_actual = datetime.datetime.now()
    print(hora_actual)
    print((str(context._user_id))+("/temperatura actual/")+(peticion_de_estacion_normalizada))
    print(" ")


async def temperatura_maxima(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    
    archivo = open("estaciones.json", "r")
    estaciones = json.load(archivo)
    
    peticion_de_estacion = context.args
    peticion_de_estacion = " ".join(peticion_de_estacion)
    existe_dato = True

    if peticion_de_estacion == "":
        existe_dato = False
        await update.message.reply_text(str('📎  Introdueix el comandament seguit de un espai i la localitat \n(per exemple "/tempmax Sueca")'))

    existe_estacion = False


    
    for estacion in estaciones:

        #Quitando tildes y carácteres extraños
        estacion_normalizada = estacion["localidad"]
        estacion_normalizada = unidecode.unidecode(estacion_normalizada)
        peticion_de_estacion_normalizada = unidecode.unidecode(peticion_de_estacion)
        estacion_normalizada = estacion_normalizada.lower()
        peticion_de_estacion_normalizada = peticion_de_estacion_normalizada.lower()

        if estacion_normalizada == peticion_de_estacion_normalizada:
            existe_estacion=True

            if estacion["estado"]:
                icono = "✅"
            else: icono = "🆘"

            await update.message.reply_text(str(icono+"  "+estacion["partida"]+" "+estacion["subpartida"]+"\n" + "Màxima "+estacion["temperatura_max"]+"ºC"))

    if not existe_estacion and existe_dato:

        await update.message.reply_text(str("No existeixen estacions de la MXO en aquesta localitat"))

    hora_actual = datetime.datetime.now()
    print(hora_actual)
    print((str(context._user_id))+("/temperatura maxima/")+(peticion_de_estacion_normalizada))
    print(" ")


async def temperatura_minima(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:


    archivo = open("estaciones.json", "r")
    estaciones = json.load(archivo)

    peticion_de_estacion = context.args
    peticion_de_estacion = " ".join(peticion_de_estacion)
    existe_dato = True

    if peticion_de_estacion == "":
        existe_dato = False
        await update.message.reply_text(str('📎  Introdueix el comandament seguit de un espai i la localitat \n(per exemple "/tempmin Sueca")'))

    existe_estacion = False

    
    for estacion in estaciones:

        #Quitando tildes y carácteres extraños
        estacion_normalizada = estacion["localidad"]
        estacion_normalizada = unidecode.unidecode(estacion_normalizada)
        peticion_de_estacion_normalizada = unidecode.unidecode(peticion_de_estacion)
        estacion_normalizada = estacion_normalizada.lower()
        peticion_de_estacion_normalizada = peticion_de_estacion_normalizada.lower()

        if estacion_normalizada == peticion_de_estacion_normalizada:
            existe_estacion=True

            if estacion["estado"]:
                icono = "✅"
            else: icono = "🆘"

            await update.message.reply_text(str(icono+"  "+estacion["partida"]+" "+estacion["subpartida"]+"\n" + "Mínima "+estacion["temperatura_min"]+"ºC"))

    if not existe_estacion and existe_dato:

        await update.message.reply_text(str("No existeixen estacions de la MXO en aquesta localitat"))

    hora_actual = datetime.datetime.now()
    print(hora_actual)
    print((str(context._user_id))+("/temperatura minima/")+(peticion_de_estacion_normalizada))
    print(" ")


async def precipitacion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    archivo = open("estaciones.json", "r")
    estaciones = json.load(archivo)
    
    peticion_de_estacion = context.args
    peticion_de_estacion = " ".join(peticion_de_estacion)
    existe_dato = True

    if peticion_de_estacion == "":
        existe_dato = False
        await update.message.reply_text(str('📎  Introdueix el comandament seguit de un espai i la localitat \n(per exemple "/pluja Sueca")'))
    

    existe_estacion = False

    

    
    
    for estacion in estaciones:

        #Quitando tildes y carácteres extraños
        estacion_normalizada = estacion["localidad"]
        estacion_normalizada = unidecode.unidecode(estacion_normalizada)
        peticion_de_estacion_normalizada = unidecode.unidecode(peticion_de_estacion)
        estacion_normalizada = estacion_normalizada.lower()
        peticion_de_estacion_normalizada = peticion_de_estacion_normalizada.lower()
      

        if estacion_normalizada == peticion_de_estacion_normalizada:

            existe_estacion=True

            if estacion["precipitacion"] == "null":
                estacion["precipitacion"] = "❓"

            if estacion["estado"]:
                icono = "✅"
            else: icono = "🆘"

            await update.message.reply_text(str(icono+"  "+estacion["partida"]+" "+estacion["subpartida"]+"\n" + "Màxima "+estacion["precipitacion"]+"mm"))

    if not existe_estacion and existe_dato:

        await update.message.reply_text(str("No existeixen estacions de la MXO en aquesta localitat"))

    hora_actual = datetime.datetime.now()
    print(hora_actual)
    print((str(context._user_id))+("/pluja/")+(peticion_de_estacion_normalizada))
    print(" ")

        

############## Alertes ############## 


async def alerta_pluja(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    argumentos = context.args
    if not argumentos:
        await update.message.reply_text("📎  Introdueix el comandament seguit de un espai, el valor, i la localitat (per exemple: '/alerta_pluja 20 Sueca')")
    

    # Extraer argumentos de la request
    argumentos_de_la_request = context.args

    # Normalizar argumentos
    valor = argumentos_de_la_request[0]
    localidad = argumentos_de_la_request[1:]
    valor = unidecode.unidecode(valor)
    valor = valor.replace(",",".")
    valor = float(valor)
    localidad = ' '.join(localidad)                     #puede contener varias palabras
    localidad = unidecode.unidecode(localidad)
    localidad = localidad.lower()

    # Creando objeto alerta
    alerta = Alerta()
    alerta.id_usuario = context._user_id                # Extrae la id del usuario que desea programar la alerta 
    alerta.meteo = "pluja"                              # Se establece el tipo de alerta 
    alerta.lindar = "superior"                          # La alerta por lluvia siempre va a ser por lindar superior
    alerta.valor = valor                                # Extrae el valor  
    alerta.localidad = localidad                        # La localidad puede contener varias palabras
    #alerta.partida = partida
    #alerta.subpartida = subpartida
    alerta.fecha = datetime.datetime.now()
    alerta.tipoalerta = "unica"
    alerta.activa = True

    # Comprueba la existencia de la localidad del argumento en la lista de estaciones
    if comprueba_si_existe_la_localidad_provisional(argumentos,estaciones):
        # Guarda la alerta con los argumentos proporcionados
        almacenador_de_alertas_provisional(argumentos)

        await update.message.reply_text("🔔  Alerta de "+ argumentos["meteo"]+" "+argumentos["lindar"]+" a "+str(argumentos["valor"])+ " mm" +" per a "+(str(argumentos["localidad"]).capitalize())+", creada amb èxit.")
    else:
        await update.message.reply_text("❓  No existeixen estacions en aquesta localitat o la localitat introduida no es vàlida ")


    hora_actual = datetime.datetime.now()
    print(hora_actual)
    print((str(context._user_id))+("/-crear alerta de lluvia provisional"))
    print(" ")


async def alerta_vent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    argumentos = context.args
    if not argumentos:
        await update.message.reply_text("📎  Introdueix el comandament seguit de un espai, si es superior o inferior, el valor, i la localitat (per exemple: '/alerta_vent superior 20 Sueca')")
    

    #abrir estaciones
    archivo = open("estaciones.json", "r")
    estaciones = json.load(archivo)

    # Extraer argumentos de la request
    argumentos_de_la_request = context.args

    
    argumentos = {  "user_id":context._user_id,                 # Extrae la id del usuario que desea programar la alerta 
                    "meteo":"vent",                            # Se establece el tipo de alerta 
                    "lindar":argumentos_de_la_request[0],                        # La alerta por lluvia siempre va a ser por lindar superior
                    "valor":argumentos_de_la_request[1],        # Extrae el valor                                                     
                    "localidad":argumentos_de_la_request[2:],   # La localidad puede contener varias palabras
                    "partida":"null",
                    "subpartida":"null",
                    "fecha":datetime.datetime.now(),
                    "tipoalerta":"unica",
                    "activa":True
                }
    
    # Normaliza los argumentos para poder compararlos, eliminando tildes, mayusculas...
    argumentos = normalizar_argumentos_provisional(argumentos)

    # Comprueba la existencia de la localidad del argumento en la lista de estaciones
    if comprueba_si_existe_la_localidad_provisional(argumentos,estaciones):
        # Guarda la alerta con los argumentos proporcionados
        almacenador_de_alertas_provisional(argumentos)

        await update.message.reply_text("🔔  Alerta de "+ argumentos["meteo"]+" "+argumentos["lindar"]+" a "+str(argumentos["valor"])+ " km/h" +" per a "+(str(argumentos["localidad"]).capitalize())+", creada amb èxit.")
    else:
        await update.message.reply_text("❓  No existeixen estacions en aquesta localitat o la localitat introduida no es vàlida ")


    hora_actual = datetime.datetime.now()
    print(hora_actual)
    print((str(context._user_id))+("/-crear alerta de viento provisional"))
    print(" ")


async def alerta_temperatura(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    argumentos = context.args
    if not argumentos:
        await update.message.reply_text("📎  Introdueix el comandament seguit de un espai, si es superior o inferior, el valor, i la localitat (per exemple: '/alerta_vent superior 20 Sueca')")
    

    #abrir estaciones
    archivo = open("estaciones.json", "r")
    estaciones = json.load(archivo)


    # Extraer argumentos de la request
    argumentos_de_la_request = context.args

    
    argumentos = {  "user_id":context._user_id,                 # Extrae la id del usuario que desea programar la alerta 
                    "meteo":"temperatura",                            # Se establece el tipo de alerta 
                    "lindar":argumentos_de_la_request[0],                        # La alerta por lluvia siempre va a ser por lindar superior
                    "valor":argumentos_de_la_request[1],        # Extrae el valor                                                     
                    "localidad":argumentos_de_la_request[2:],   # La localidad puede contener varias palabras
                    "partida":"null",
                    "subpartida":"null",
                    "fecha":datetime.datetime.now(),
                    "tipoalerta":"unica",
                    "activa":True
                }
    
    # Normaliza los argumentos para poder compararlos, eliminando tildes, mayusculas...
    argumentos = normalizar_argumentos_provisional(argumentos)

    # Comprueba la existencia de la localidad del argumento en la lista de estaciones
    if comprueba_si_existe_la_localidad_provisional(argumentos,estaciones):
        # Guarda la alerta con los argumentos proporcionados
        almacenador_de_alertas_provisional(argumentos)

        await update.message.reply_text("🔔  Alerta de "+ argumentos["meteo"]+" "+argumentos["lindar"]+" a "+str(argumentos["valor"])+ " ºC" +" per a "+(str(argumentos["localidad"]).capitalize())+", creada amb èxit.")
    else:
        await update.message.reply_text("❓  No existeixen estacions en aquesta localitat o la localitat introduida no es vàlida ")


    hora_actual = datetime.datetime.now()
    print(hora_actual)
    print((str(context._user_id))+("/-crear alerta de temperatura provisional"))
    print(" ")


async def alerta_estat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    argumentos = context.args
    if not argumentos:
        await update.message.reply_text("📎  Introdueix el comandament seguit de un espai i la localitat (per exemple: '/alerta_estat Sueca')")
    

    #abrir estaciones
    archivo = open("estaciones.json", "r")
    estaciones = json.load(archivo)


    # Extraer argumentos de la request
    argumentos_de_la_request = context.args

    
    argumentos = {  "user_id":context._user_id,                 # Extrae la id del usuario que desea programar la alerta 
                    "meteo":"estat",                            # Se establece el tipo de alerta 
                    "lindar":"null",                        # La alerta por lluvia siempre va a ser por lindar superior
                    "valor":"null",        # Extrae el valor                                                     
                    "localidad":argumentos_de_la_request[0:],   # La localidad puede contener varias palabras
                    "partida":"null",
                    "subpartida":"null",
                    "fecha":datetime.datetime.now(),
                    "tipoalerta":"unica",
                    "activa":True
                }


    # Normaliza los argumentos para poder compararlos, eliminando tildes, mayusculas...
    argumentos = normalizar_argumentos_provisional(argumentos)

    # Comprueba la existencia de la localidad del argumento en la lista de estaciones
    if comprueba_si_existe_la_localidad_provisional(argumentos,estaciones):
        # Guarda la alerta con los argumentos proporcionados
        almacenador_de_alertas_provisional(argumentos)

        await update.message.reply_text("🔔  Alerta de estacions offline per a la localitat de "+(str(argumentos["localidad"]).capitalize())+", creada amb èxit.")
    else:
        if context.args:
            await update.message.reply_text("❓  No existeixen estacions en aquesta localitat o la localitat introduida no es vàlida ")


    hora_actual = datetime.datetime.now()
    print(hora_actual)
    print((str(context._user_id))+("/-crear alerta de temperatura provisional"))
    print(" ")


async def alerta_borrar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:


    argumentos = context.args
    if not argumentos:
        await update.message.reply_text("📎  Introdueix el comandament seguit de el número de identificació de la alerta, ( si no el saps presiona el comandament /alerta ) tambe pots escriure ' /alerta_borrar totes ' per a borrarles totes")
    
    
    user_id = context._user_id
    argumento = context.args
    argumento = argumento[0]

    conexion=sqlite3.connect("bbdd.db") 
    cursor=conexion.execute("select codigo,id_usuario,meteo,lindar,valor,localidad from alertas")

    for fila in cursor:
        if fila[1] == user_id:

            if argumento == "totes" or argumento == "todas":

                cursor.execute("DELETE FROM alertas WHERE id_usuario=?", (user_id,))
                await update.message.reply_text("✅  Totes les alertes borrades amb èxit")
                break


            if float(fila[0]) == float(argumento):

                cursor.execute("DELETE FROM alertas WHERE codigo=?", (argumento,))
                await update.message.reply_text("✅  Alerta de "+fila[2]+" "+fila[3]+" a "+str(fila[4])+" per a "+(str(fila[5]).capitalize())+" borrada amb èxit")
                break

    else:await update.message.reply_text("⛔️  No hi ha cap alarma amb aquest número (" +(str(argumento))+ ")" )

    conexion.commit()
    conexion.close()

    hora_actual = datetime.datetime.now()
    print(hora_actual)
    print((str(context._user_id))+("/borrar alerta"))
    print(" ")


async def alerta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    user_id = context._user_id

    conexion=sqlite3.connect("bbdd.db") 
    cursor=conexion.execute("select codigo,id_usuario,meteo,lindar,valor,localidad from alertas")
    existen_alertas = False

    for fila in cursor:

        if fila[1] == user_id:

            mensaje = ("🔔  Alerta programada de "+str(fila[2])+" "+str(fila[3])+" a "+str(fila[4])+" en "+str(fila[5])+" amb el número de identificació: \n"+str(fila[0]))
            existen_alertas = True
            await update.message.reply_text(mensaje)

    conexion.close()

    if not existen_alertas:
        await update.message.reply_text("📎  No tens ninguna alerta programada en aquest moment")


    hora_actual = datetime.datetime.now()
    print(hora_actual)
    print((str(context._user_id))+("/alerta"))
    print(" ")







def main() -> None:

    app = ApplicationBuilder().token(TOKEN).build()

    ############## Visualització ############## 

    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(CommandHandler("temp", temperatura))
    app.add_handler(CommandHandler("tempact", temperatura_actual))
    app.add_handler(CommandHandler("tempmax", temperatura_maxima))
    app.add_handler(CommandHandler("tempmin", temperatura_minima))
    app.add_handler(CommandHandler("plutja", precipitacion))
    app.add_handler(CommandHandler("pluja", precipitacion))
    app.add_handler(CommandHandler("out", estaciones_out))
    app.add_handler(CommandHandler("datact", data_act))

    ############## Alertes ############## 

    app.add_handler(CommandHandler("alerta_borrar", alerta_borrar))
    app.add_handler(CommandHandler("alerta", alerta))
    app.add_handler(CommandHandler("alerta_pluja", alerta_pluja))
    app.add_handler(CommandHandler("alerta_vent", alerta_vent))
    app.add_handler(CommandHandler("alerta_temperatura", alerta_temperatura))
    app.add_handler(CommandHandler("alerta_estat", alerta_estat))


    app.run_polling()


if __name__ == "__main__":
    main()



    



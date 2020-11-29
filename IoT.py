import mysql.connector as mysql
import time
import paho.mqtt.client as mqtt
import json 
from datetime   import datetime 
#*local variables 

now = datetime.now()
current_time = now.strftime("%H:$M:%S")

#*  connection to databse
db = mysql.connect(host="localhost", user="root", passwd="root",database = "iot")

#* create obect with A.K.A MySQL    
mycursor = db.cursor() 
# mycursor.execute("INSERT INTO Home(user_id, F_name, L_name) VALUE (%s, %s, %S)", (1,"Victor","Ponce"))
# mycursor.commit()


# Callback Function on Connection with MQTT Server
# Callback Function on Connection with MQTT Server
# Función Callback que se ejecuta cuando se conectó con el servidor MQTT

def on_connect(client, userdata, flags, rc):
    print("Connected with Code :" + str(rc))
    # Subscribe Topic from here
    # Aprovechando que se conectó, hacemos un subscribe a los tópicos
    #client.subscribe("fjhp6619mxIn")
    client.subscribe("tc1004b/g6")

# Callback Function on Receiving the Subscribed Topic/Message
# Cuando nos llega un mensaje a los tópicos suscritos, se ejecuta
# esta función. Convertimos el mensaje de llegada a diccionario
# asumiendo que nos llega un formto json en el payload
# si nos llega otro tipo de mensaje marcará error, falta
# codificar el manejador del error


def on_message(client, userdata, msg):
    # print the message received from the subscribed topic
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    m_in = json.loads(m_decode)

# Checar si el tópico es el que deseamos
# Para Debug: iprimimos lo que generamos
# Aquí es donde podemos almacenar en la BD la información
# que envía el dispositivo
    # print()
    # print('------------Llegada de mensaje-----------')
    # print('Tópico: ', topic)
    # print(type(m_decode), ' ', m_decode)
    # print(type(m_in), ' ', m_in)
    # print('Dispositivo: ', type(m_in['dispositivo']), ' ', m_in['dispositivo'])
    # print('       Tipo: ', type(m_in['tipo']), ' ', m_in['tipo'])
    # print('       Dato: ', type(m_in['dato']), ' ', m_in['dato'])
    # print()
    # print('------------Llegada de mensaje-----------')
    # print('Tópico: ', topic)
    # print(type(m_decode), ' ', m_decode)
    # print(type(m_in), ' ', m_in)
    # print('  dato_id', type(m_in['dato'],' ')m_in['dato'])
    # print('sensor_id', type(m_in['sensor']),' ', m_in['sensor'])
    # print('    valor', type(m_in['valor']),' ', m_in['valor'])
    # print('time'+ current_time)
    # print('\ntesting')
    # TODO: jason works, need to implement to the data base and test
    # dato_id = (type(m_in['dato']),' ', m_in['dato'])
    sensor_id = m_in['sensor']
    valor = m_in['valor']
    # print(dato_id)
    print(sensor_id)
    print(valor)
    

    mycursor.execute("INSERT INTO datos(valor, time) VALUE (%s, %s)", (valor, current_time))
    mycursor.commit()
    # print ("Recibido--->", str(msg.payload) )

# En esta función pedimos datos al usuario para saber a qué
# dispositivo vamos a enviar el mensaje y lo formatemos a json


def envia_dispositivo():
    dispositivo = input('Nombre del dispositivo:')
    sensor_actuador = input('Sensor del dispositivo:')
    accion = int(input('Acción:'))
    dicSalida = {'dispositivo': dispositivo,
                 'tipo': sensor_actuador, 'dato': accion}
    salidaJson = json.dumps(dicSalida)
    print('Salida Json:', salidaJson)
    client.publish("tc1004b/g6", salidaJson)
    #time.sleep(4)
    #client.publish("fjhp6619mxIn",salidaJson)

# Envía un mensaje de prueba para que se procese en la llegada de mensajes


def mensaje_debug():
    salida = '{"dispositivo":"Debug1","tipo":"Debug_Tipo","dato":5}'
    input('Mensaje de prueba: ' + salida)
    client.publish("tc1004b/g6", salida)


# Generamos el cliente y las funciones para recibir mensajes y
# cuando se genera la conexión.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# Hacemos la conexión al Broker
client.connect("broker.mqtt-dashboard.com", port=1883)
# Las siguientes instrucciones son para el caso que requiera password
# client.username_pw_set("setsmjwc", "apDnKqHRgAjA")
# y para ejecutar un loop forever, nosotros haremos un loop_start()
# solamente
# client.loop_forever()
# Iniciamos el ciclo del cliente MQTT
# Por lo que se va a conectar y le damos tres segundos
client.loop_start()
time.sleep(3)

#Programa principal
opc = 'x'
while opc != 's':
    opc = input('e)nvía p)rocesa c)onsulta s)alir d)ebug ')
    if opc == 'e':
        envia_dispositivo()
    elif opc == 'p':
        procesa()
    elif opc == 'c':
        consulta()
    elif opc == 'd':
        mensaje_debug()

# al salir paramos el loop y nos desconectamos
client.loop_stop()
client.disconnect()

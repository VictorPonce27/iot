import mysql.connector as mysql
import time
import paho.mqtt.client as mqtt
import json 
from datetime   import datetime as dt 
from datetime import timedelta 
#!local variables 
#*  connection to databse
db = mysql.connect(host="localhost", user="root", passwd="root",database = "iot")

#* create obect with A.K.A MySQL    
mycursor = db.cursor() 

# Callback Function on Connection with MQTT Server
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
    #* current time variable
    current_time = (dt.now() - timedelta(1)).strftime('%Y-%m-%d %H:%M:%S.%f')
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print(m_decode); 
    print("before m_in")
    m_in = json.loads(m_decode)

# Checar si el tópico es el que deseamos
# Para Debug: iprimimos lo que generamosdata
# Aquí es donde podemos almacenar en la BD la información
# que envía el dispositivo
    action =  m_in['action']

    if(action == 1):
        device_id = m_in['device']
        sensor_id = m_in['sensor']
        valor = m_in['valor']
        mycursor.execute("INSERT INTO data(device_id, sensor_id, value, time) VALUE (%s,%s,%s,%s)",(device_id,sensor_id,valor,current_time))   
        db.commit()
    else:
        user_id = m_in['user']
        device_id = m_in['device']
        sensor_id = m_in['sensor']
        room_id = device_id
        value = m_in['value']
        mycursor.execute("INSERT INTO changes(user_id, device_id, sensor_id, value, time) VALUE (%s,%s,%s,%s,%s)",(user_id,device_id,sensor_id,valor,current_time))   
        db.commit()


    #!sends data from nodeMCU to mysql 
    
# En esta función pedimos datos al usuario para saber a qué 
# dispositivo vamos a enviar el mensaje y lo formatemos a json


def envia_dispositivo():
    dispositivo = input('Nombre del dispositivo:')
    sensor_actuador = input('Sensor del dispositivo:')
    action = int(input('Acción:'))
    user = int(input('user:  '))
    dicSalida = (str(dispositivo)+ str(sensor_actuador)+ str(action))
    salidaJson = json.dumps(dicSalida)

    client.publish("tc1004b/g6/control", salidaJson)
    print("message sent")

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

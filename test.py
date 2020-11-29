import time
import paho.mqtt.client as mqtt

# Callback Function on Connection with MQTT Server


def on_connect(client, userdata, flags, rc):
    print("Connected with Code :" + str(rc))
    # Subscribe Topic from here
    # client.subscribe("fjhp6619mxOut")
    client.subscribe("tc1004b/g6")


# Callback Function on Receiving the Subscribed Topic/Message
def on_message(client, userdata, msg):
    # print the message received from the subscribed topic
    print("on message function")
    topicoLlegada = msg.topic
    mensajeLlegada = str(msg.payload.decode("utf-8", "ignore"))
    print('------------------------------------------')
    print("RECEPCIÓN    tópico:", topicoLlegada, " Msg:", mensajeLlegada)
    print('------------------------------------------')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.mqtt-dashboard.com", port=1883)
#client.username_pw_set("setsmjwc", "apDnKqHRgAjA")


# client.loop_forever()
client.loop_start()
time.sleep(1)
while True:
    # client.publish("fjhp6619mxOut", "Mensaje Py para fjhpOut")
    # print("--->Mensaje enviado a fjhp6610mxOut")
    time.sleep(3)
    # client.publish("tc1004b/profe", "Mensaje Py para tc1004b/profe")
    # print("--->Mensaje enviado a tc1004b/profe")
    time.sleep(7)

client.loop_stop()
client.disconnect()

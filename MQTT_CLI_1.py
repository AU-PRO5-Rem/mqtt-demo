# Imports
import paho.mqtt.client as mqtt
import time # Used for sleeping function (although it's kinda irrelevant, and can be done in other ways)

# Callback definitions
# it's possible to create a callback function, so when a certain function is done or "accomplished", it will call these
# functions, and execute the definition code.
def on_connect(client, userdata, flags, rc):
    print("Connection returned with result code:" + str(rc))


def on_disconnect(client, userdata, rc):
    print("Disconnection returned result:" + str(rc) + " ")


def on_publish(client, userdata, mid):
    print("msq: " + str(mid) + " send")


# Client definitions:
def client_setup():
    # This function will set up the client and its properties, as well as directing the callback's to their functions
    client = mqtt.Client(client_id="jinx/publisher", clean_session=False)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.will_set("jinx/died", payload="pub died unexpected")
    return client


def start_client(host, port, timer):
    # This function will start the MQTT client.
    client = client_setup()
    client.connect(host, port, timer)
    # loop_start makes a loop thread, so it's possible to let the main program do other work
    client.loop_start()
    return client


# MQTT client publisher start
client = start_client("test.mosquitto.org", 1883, 60)

# just a value used for different things inthe while loop
rando_val = 0
while 1:
    time.sleep(5)  # wait till all messages are processed
    if rando_val < 10:
        print("sending topic batch: " + str(rando_val))
        client.publish("jinx/hello", payload="Hello world!")
        client.publish("jinx/temperature", payload=rando_val)
        # wait_for_publish is a blocking call, so the program will not go further, before the msg is published
        client.publish("jinx/humidity", payload="65%").wait_for_publish()
        rando_val += 1
    else:
        rando_val += 1
        print("waiting for: " + str(15 - rando_val))

    if rando_val == 11:
        print("disconnecting")
        # disconnecting wipes either the client or loop (not sure which one), as weel as removing unsent msg's
        # though this can be circumvented
        client.disconnect()

    if rando_val == 15:
        # There is a reconnect function, but it's confusing, so just run the client setup again instead for now
        client = start_client("test.mosquitto.org", 1883, 60)
        rando_val = 0

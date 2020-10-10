# Imports
import paho.mqtt.client as mqtt

# Callback definitions
# it's possible to create a callback function, so when a certain function is done or "accomplished", it will call these
# functions, and execute the definition code.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Client subscribe topics, alternatives to this is writing them in their own subscribe function.
    client.subscribe([("jinx/hello", 0), ("jinx/temperature", 0), ("jinx/humidity", 0), ("jinx/died", 0)])


def on_message(client, userdata, msg):
    # If necessary it's possible to have individual callbacks for topics, instead of 1 collective
    # could be necessary whit multiple sensors, function for this is "message_callback_add()"
    print(str(msg.topic) + " : " + str(msg.payload))


# Client setup
client = mqtt.Client(client_id="jinx/subscriber")
client.on_connect = on_connect
client.on_message = on_message

# Client connection, syntax: [host, port, alive-timer]
client.connect("test.mosquitto.org", 1883, 60)

# loop_forever is a blocking call, and makes it "impossible" to do other tasks in this program
client.loop_forever(timeout=5, retry_first_connection=False)

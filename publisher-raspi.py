import paho.mqtt.publish as publish
publish.single("ifn649", "Hello world", hostname="3.27.164.138")
print("Done")

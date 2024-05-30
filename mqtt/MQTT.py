import paho.mqtt.client as mqtt
import json
import ssl
from geopy.geocoders import Nominatim
import _mysql


# MQTT přihlašovací údaje       
MQTT_HOST = "Mqtt.portabo.cz"
MQTT_PORT = 8883
MQTT_USER = "hackithon"
MQTT_PASSWORD = "zuk8uy9aZXU2wM9trqqA"

db = _mysql.Database()

# Callback funkce při úspěšném připojení
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        # Přihlášení k odběru všech témat
        client.subscribe("/#")
    else:
        print(f"Connection failed with code {rc}")



# Callback funkce při přijetí zprávy
def on_message(client, userdata, msg):
    try:

        # Převedení zprávy na JSON a výpis
        # msg.topic obsahuje téma zprávy
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)

        sql_data = {
            "nazev" : "Bez nazvu",
            "misto" : "Bez pozice",
            "typ" : "Bez typu"
        }
        # Zpracování zprávy podle formátu


        if 'vodomery' in msg.topic: # vodomery
            sql_data["typ"] = "vodomer"
            sql_data["nazev"] = data[0]["misto"]
            
        elif 'sensor' in data: # kamery
            # Zpracování zprávy z MQTT, která obsahuje informace o senzoru
            sql_data["nazev"] = data['sensor']
            sql_data["typ"] = data['detectionType']
        elif data["correlation_ids"]: # zachranka
            # Zpracování zprávy z TTN, která obsahuje informace o geolokaci, pokud jsou k dispozici
            latitude = data["uplink_message"]["rx_metadata"][0]["location"]["latitude"]
            longitude = data["uplink_message"]["rx_metadata"][0]["location"]["longitude"]
            geolocator = Nominatim(user_agent="geoapiExercises")
            sql_data["misto"] = geolocator.reverse((latitude, longitude)).address
            sql_data["nazev"] = data["end_device_ids"]["application_ids"]["application_id"]
            sql_data["typ"] = data["uplink_message"]["decoded_payload"]["sensor"]   
        elif not data["uplink_message"] and data["end_device_ids"]: # provoz aplikace
            sql_data["nazev"] = data["end_device_ids"]["device_id"]
            sql_data["typ"] = data["end_device_ids"]["application_id"] 
        elif data["end_device_ids"] and data["uplink_message"]:
            latitude = data["uplink_message"]["rx_metadata"][0]["location"]["latitude"]
            longitude = data["uplink_message"]["rx_metadata"][0]["location"]["longitude"]
            geolocator = Nominatim(user_agent="geoapiExercises")
            sql_data["misto"] = geolocator.reverse((latitude, longitude)).address
            sql_data["nazev"] = data["end_device_ids"]["device_id"]
            sql_data["typ"] = data["uplink_message"]["decoded_payload"]["sensor"]
        
        if(sql_data['nazev'] == 'test-provozu-aplikace'):
            sql_data['nazev'] = msg.topic.split('/')[2]
        
        db.insert_senzorV3(sql_data)

    except(Exception) as error:
        pass

# Nastavení klienta
client = mqtt.Client(protocol=mqtt.MQTTv31)
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# Nastavení TLS/SSL
client.tls_set(cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)

# Připojení k brokeru
client.connect(MQTT_HOST, MQTT_PORT, 60)

# Funkce pro odesílání zpráv
def publish_message(topic, message):
    client.publish(topic, message)

# Spuštění smyčky
client.loop_start()

# Příklad odeslání zprávy
publish_message("/hackithon/test", "Hello, MQTT!")

# Udržování skriptu v chodu pro příjem zpráv
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()

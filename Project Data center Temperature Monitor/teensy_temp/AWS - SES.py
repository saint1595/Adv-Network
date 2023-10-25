import paho.mqtt.client as mqtt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import re

# MQTT configuration
mqtt_broker = "3.27.222.106"
mqtt_port = 1883
mqtt_topic = "temperature_data"

# Temperature threshold
temperature_threshold = 25.0  # Adjust as needed

# AWS SES configuration
aws_ses_smtp_username = "AKIA5JBWHHY3F7RIKV66"
aws_ses_smtp_password = "BBLddazZdMxl65VDiDF11yDURn+bnjkF8F5+7X+/jLau"
aws_ses_region = "ap-southeast-2"  # Adjust to your AWS region
sender_email = "n11168781@qut.edu.au"
recipient_email = "jimin619@gmail.com"

def send_email(subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    body = message
    msg.attach(MIMEText(body, 'plain'))

    try:
        ses_client = smtplib.SMTP('email-smtp.' + aws_ses_region + '.amazonaws.com', 587)
        ses_client.starttls()
        ses_client.login(aws_ses_smtp_username, aws_ses_smtp_password)
        ses_client.sendmail(sender_email, recipient_email, msg.as_string())
        ses_client.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Email could not be sent:", e)

def on_message(client, userdata, message):
    data = message.payload.decode()
    print("Received data:", data)

    # Use a regular expression to extract the temperature value
    temperature_match = re.search(r"Temperature:\s+(\d+\.\d+)C", data)

    if temperature_match:
        temperature_str = temperature_match.group(1)
        try:
            temperature = float(temperature_str)
            print("Extracted temperature:", temperature)

            # Check if the temperature is above the threshold
            if temperature > temperature_threshold:
                alert_message = f"Temperature alert: {temperature}°C is above the threshold of {temperature_threshold}°C."
                send_email("Temperature Alert", alert_message)
        except ValueError:
            print("Failed to convert extracted temperature to float.")
    else:
        print("Temperature value not found in the message.")

    # Handle other parts of the message if needed

def on_connection(client, udata, flags, rc):
    print("Connected to MQTT broker")
    mqtt_client.subscribe(mqtt_topic)

# Configure the MQTT client
mqtt_client = mqtt.Client()

try:
    mqtt_client.on_message = on_message
    mqtt_client.on_connect = on_connection
    mqtt_client.connect(mqtt_broker, mqtt_port)
    mqtt_client.loop_start()

    while True:
        pass

except Exception as e:
    print("Error:", e)
import os
import json
from datetime import datetime
from sense_hat import SenseHat
from time import sleep
from google.cloud import pubsub_v1

sense = SenseHat()

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
topic_id = os.getenv('GOOGLE_CLOUD_TOPIC_ID')
device_id = os.getenv('DEVICE_ID')

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

while True:
    temperature = sense.get_temperature()

    event = {
        'measured_at': datetime.utcnow().isoformat(),
        'device': device_id,
        'temperature': temperature
    }

    future = publisher.publish(topic_path, json.dumps(event, default=str).encode('utf-8'))
    sleep(7200)

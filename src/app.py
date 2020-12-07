import os
import json
from datetime import datetime
from sense_hat import SenseHat
from time import sleep
from google.cloud import pubsub_v1

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
topic_id = os.getenv('GOOGLE_CLOUD_TOPIC_ID')
device_id = os.getenv('DEVICE_ID')

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

sense = SenseHat()

while True:
    temp = sense.get_temperature()
    t = os.popen('/opt/vc/bin/vcgencmd measure_temp')
    cputemp = t.read()
    cputemp = cputemp.replace('temp=','')
    cputemp = cputemp.replace('\'C\n','')
    cputemp = float(cputemp)
    temperature = temp - ((cputemp - temp) / 2)

    event = {
        'measured_at': datetime.utcnow().isoformat(),
        'device': device_id,
        'temperature': temperature,
    }

    payload = json.dumps(event, default=str).encode('utf-8')

    print(payload)

    future = publisher.publish(topic_path, payload)

    sleep(15)

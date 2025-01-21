import uuid
import json
import logging
import requests
from kafka import KafkaProducer
import time


def get_data():
    try:
        res = requests.get("https://randomuser.me/api/", timeout=10)
        res.raise_for_status()
        res = res.json()
        return res['results'][0]

    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des données : {e}")
        return None


def format_data(res):
    try:
        data = {}
        location = res['location']
        data['id'] = str(uuid.uuid4())
        data['first_name'] = res['name']['first']
        data['last_name'] = res['name']['last']
        data['gender'] = res['gender']
        data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                          f"{location['city']}, {location['state']}, {location['country']}"
        data['post_code'] = location['postcode']
        data['email'] = res['email']
        data['username'] = res['login']['username']
        data['dob'] = res['dob']['date']
        data['phone'] = res['phone']

        return data
    except KeyError as e:
        print(f"Clé manquante dans les données : {e}")
        return None


def send_to_kafka(data, producer, topic):
    try:
        producer.send(topic, value=data)
        producer.flush()
        print(f"Données envoyées au topic '{topic}' : {data}")
    except Exception as e:
        print(f"Erreur lors de l'envoi des données à Kafka : {e}")


def main():
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    topic = 'userdata'

    while True:
       res = get_data()
       if res:
         formatted_data = format_data(res)
         if formatted_data:
            send_to_kafka(formatted_data, producer, topic)
       time.sleep(10)


if __name__ == "__main__":
    main()

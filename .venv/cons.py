from kafka import KafkaConsumer
import json
import happybase
import time


def connect_to_hbase_table():
    try:
        connection = happybase.Connection('localhost')
        table_name = 'userdata'
        return connection.table(table_name)
    except Exception as e:
        print(f"Erreur lors de la connexion à la table HBase : {e}")
        return None
def consume_messages(table):
    try:
        consumer = KafkaConsumer(
            'userdata',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='userdata-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        print("En attente des messages sur le topic 'userdata'...")

        for message in consumer:
            data = message.value
            print(f"Message reçu : {data}")
            process_data(data, table)
    except Exception as e:
        print(f"Erreur lors de la consommation des messages : {e}")

def process_data(data, table):
    try:
        table.put(data['id'], {
            b'info:first_name': str(data['first_name']).encode('utf-8'),
            b'info:last_name': str(data['last_name']).encode('utf-8'),
            b'info:gender': str(data['gender']).encode('utf-8'),
            b'info:dob': str(data['dob']).encode('utf-8'),
            b'contact:email': str(data['email']).encode('utf-8'),
            b'contact:username': str(data['username']).encode('utf-8'),
            b'contact:phone': str(data['phone']).encode('utf-8'),
            b'address:street': str(data['address']).encode('utf-8'),
            b'address:post_code': str(data['post_code']).encode('utf-8')
        })
        print(f"Données insérées dans HBase pour l'ID : {data['id']}")
    except Exception as e:
        print(f"Erreur lors du traitement des données pour l'ID : {data.get('id', 'inconnu')} - {e}")


if __name__ == "__main__":
 table=connect_to_hbase_table()
if table:
    consume_messages(table)
else:
 print("Impossible de créer ou accéder à la table HBase.")


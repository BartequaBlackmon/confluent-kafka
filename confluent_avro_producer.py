# Import the necessary libraries
from confluent_kafka import avro
from uuid import uuid4, UUID
import time

from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer

def delivery_report(err, msg):
    """
    Reports the success or failure of a message delivery.
    Args:
        err (KafkaError): The error that occurred, or None on success.
        msg (Message): The message that was produced or failed.
    Note:
        In the delivery report callback, the Message.key() and Message.value() will be the binary format as encoded by any configured serializers and not the same objectthat was passed to the producer().
        If you wish to pass the original object(s) for key and value to delivery report callback, you can use the opaque argument of produce() to pass them as a tuple or dict.
    """ 
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
    print("==================================")

# Define the kafka configuration
kafka_config = {
    'bootstrap.servers': 'localhost:9092',
    'sasl.mechanism': 'PLAIN',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.username': 'admin',
    'sasl.password': 'admin'
}

# Create a schema registry client
schema_registry_client = SchemaRegistryClient({'url': 'http://localhost:8081', 'basic.auth.user.info': 'admin:admin'})

# Fetch the latest Avro schema for the value
subject_name = 'my-topic-value'
schema_str = schema_registry_client.get_latest_version(subject_name).schema.schema_str
print("Schema from Registry---")
print(schema_str)
print("==================================")

# Create an Avro serializer for the value
Key_serializer = StringSerializer('utf_8')
avro_serializer = AvroSerializer(schema_registry_client, schema_str)

# Define the SerializingProducer
producer = SerializingProducer({
    'bootstrap.servers': kafka_config['bootstrap.servers'],
    'security.protocol': kafka_config['security.protocol'],
    'sasl.mechanism': kafka_config['sasl.mechanism'],
    'sasl.username': kafka_config['sasl.username'],
    'sasl.password': kafka_config['sasl.password'],
    'key.serializer': Key_serializer, # Key will be serialized using the String
    'value.serializer': avro_serializer # value will be serialized using the Avro
})

# Load the csv data into pandas dataframe
df = pd.read_csv('Healthcare.csv')
df =df.fillna('null') # Fill NaN values with empty string
print(df.head(5))
print("==================================")

# Iterate through the dataframe and produce messages to Kafka
for index, row in df.iterrows():
    # Create a dictionary for the Avro message value
    data_value = row.to_dict()
    print(data_value)
    data_value['PatientID'] = str(data_value['PatientID']) # Convert PatientID to string
    # Produce the message to Kafka
    producer.produce(
        topic='my-topic', 
        key=str(uuid4()), 
        value=data_value, 
        on_delivery=delivery_report
    )
    producer.flush() # Flush the producer to ensure all messages are sent
    time.sleep(3) # Sleep for a while before sending the next message
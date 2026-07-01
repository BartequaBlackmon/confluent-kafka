import json
from google.cloud import pubsub_v1
from config import PROJECT_ID, SUBSCRIPTION_ID

subscriber = pubsub_v1.SubscriberClient()

subscription_path = subscriber.subscription_path(
    PROJECT_ID,
    SUBSCRIPTION_ID
)


def callback(message):

    patient = json.loads(message.data.decode("utf-8"))

    print("=" * 50)
    print("Received Patient Record")
    print("=" * 50)

    print(f"Patient ID      : {patient['Patient_ID']}")
    print(f"Age             : {patient['Age']}")
    print(f"Gender          : {patient['Gender']}")
    print(f"Symptoms        : {patient['Symptoms']}")
    print(f"Symptom Count   : {patient['Symptom_Count']}")
    print(f"Disease         : {patient['Disease']}")

    message.ack()

    print("Message Acknowledged\n")


streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=callback
)

print(f"Listening on {subscription_path}...\n")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
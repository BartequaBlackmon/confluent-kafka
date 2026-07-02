import json
import pandas as pd
from google.cloud import pubsub_v1
#from config import PUBSUB_PROJECT_ID, TOPIC_ID, CVS_FILE

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(hadoopcluster-496518, healthcare)  

df =pd.read_csv(Healthcare.csv)

print(f"Publishing {len(df)} records....\n")

for _, row in df.iterrows():

    record = {
        "Patient_ID": int(row["Patient_ID"]),
        "Age": int(row["Age"]),
        "Gender": row["Gender"],
        "Symptoms": row["Symptoms"],
        "Symptom_Count": int(row["Symptom_Count"]),
        "Disease": row["Disease"]
    }

    message_json = json.dumps(record).encode("utf-8")

    future = publisher.publish(topic_path, data=message_json)
    print(f"Published Patient {record['Patient_ID']} -> {future.result()}")

print("\nFinished publishing records.")
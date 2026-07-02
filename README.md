# Google Cloud Pub/Sub Order Processing Demo

## Overview

This project demonstrates a simple messaging pipeline using **Google Cloud Pub/Sub**.

The application consists of two Python programs:

* **Producer** – Generates mock order data and publishes it to a Pub/Sub topic.
* **Consumer** – Reads messages from a Pub/Sub subscription, deserializes the JSON payload, prints the order information, and acknowledges each message.

This project is useful for learning event-driven architectures and message-based communication using Google Cloud Pub/Sub.

---

# Architecture

```
+-----------------+       +-------------------+       +----------------------+
|   Producer      | ----> | Pub/Sub Topic     | ----> | Pub/Sub Subscription |
| (publisher.py)  |       | orders_data       |       | orders_data          |
+-----------------+       +-------------------+       +----------------------+
                                                             |
                                                             |
                                                             v
                                                  +------------------+
                                                  | Consumer         |
                                                  | (consumer.py)    |
                                                  +------------------+
```

---

# Features

## Producer

* Generates random order data
* Converts the order to JSON
* Publishes messages to Google Cloud Pub/Sub
* Displays the published message ID
* Sends a new order every 2 seconds

## Consumer

* Pulls messages from a Pub/Sub subscription
* Decodes UTF-8 message data
* Deserializes JSON into a Python dictionary
* Prints each order
* Acknowledges processed messages

---

# Prerequisites

* Python 3.9 or later
* Google Cloud Project
* Pub/Sub API enabled
* A Pub/Sub topic named:

```
orders_data
```

* A Pub/Sub subscription named:

```
orders_data
```

* Google Cloud service account credentials

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

Install dependencies:

```bash
pip install google-cloud-pubsub
```

---

# Authentication

Set your Google Cloud credentials.

### Windows

```cmd
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service-account.json
```

### Linux/macOS

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

Or authenticate using the Google Cloud CLI:

```bash
gcloud auth application-default login
```

---

# Project Configuration

Both applications use the following Google Cloud project:

```python
project_id = "hadoopcluster-496518"
```

Topic:

```python
topic_name = "orders_data"
```

Subscription:

```python
subscription_name = "orders_data"
```

---

# Project Structure

```
.
├── producer.py
├── consumer.py
└── README.md
```

---

# Producer

The producer continuously creates mock order records and publishes them to the Pub/Sub topic.

Each message contains information such as:

* Order ID
* Customer ID
* Product
* Quantity
* Price
* Shipping Address
* Order Status
* Creation Date

The producer waits **2 seconds** before publishing the next order.

Example output:

```
Published message with ID: 947516824593624
Published message with ID: 947516824593625
Published message with ID: 947516824593626
```

Run the producer:

```bash
python producer.py
```

---

# Consumer

The consumer continuously polls the Pub/Sub subscription.

For every received message it:

1. Pulls messages from the subscription
2. Decodes the JSON payload
3. Converts the payload into a Python dictionary
4. Prints the order
5. Acknowledges the message

Example output:

```
{
    'order_id': 1,
    'customer_id': 540,
    'item': 'Laptop',
    'quantity': 2,
    'price': 1299.95,
    'shipping_address': '123 Main St, City A, Country',
    'order_status': 'Pending',
    'creation_date': '2024-11-30'
}
==================
```

Run the consumer:

```bash
python consumer.py
```

Stop the application using **Ctrl + C**.

---

# Example Message

```json
{
  "order_id": 1,
  "customer_id": 542,
  "item": "Laptop",
  "quantity": 2,
  "price": 1299.95,
  "shipping_address": "123 Main St, City A, Country",
  "order_status": "Pending",
  "creation_date": "2024-11-30"
}
```

---

# Workflow

1. The producer generates mock order data.
2. The order is serialized into JSON.
3. The JSON message is published to the **orders_data** topic.
4. Google Cloud Pub/Sub stores the message.
5. The consumer retrieves messages from the **orders_data** subscription.
6. The consumer deserializes and prints the order.
7. The consumer acknowledges the message to prevent redelivery.

---

# Troubleshooting

## 404 Resource not found

Example:

```
google.api_core.exceptions.NotFound:
404 Resource not found (resource=orders_data)
```

Verify that:

* The Pub/Sub topic exists.
* The Pub/Sub subscription exists.
* The subscription is attached to the correct topic.
* The application is using the correct Google Cloud project.
* Your service account has permission to access Pub/Sub resources.

---

## Authentication Errors

If authentication fails:

* Verify `GOOGLE_APPLICATION_CREDENTIALS` points to a valid service account key.
* Ensure the service account has the **Pub/Sub Publisher** and **Pub/Sub Subscriber** IAM roles.

---

# Future Improvements

* Configuration using environment variables
* Logging instead of console output
* Dead-letter queue support
* Retry handling
* Docker support
* Unit tests
* Message filtering
* Graceful shutdown
* Async publisher and subscriber
* Configuration via `.env` file

---

# Technologies Used

* Python
* Google Cloud Pub/Sub
* JSON
* Google Cloud SDK

---

# License

This project is intended for educational purposes and demonstrates the fundamentals of building an event-driven messaging application using Google Cloud Pub/Sub.

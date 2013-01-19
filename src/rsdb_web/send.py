
import json
import pika

OUT_QUEUE = 'outbound'

def hand_off(body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=OUT_QUEUE, durable=True)
    channel.basic_publish(exchange='',
                          routing_key=OUT_QUEUE,
                          body=body,
                          properties=pika.BasicProperties(delivery_mode=2))
    connection.close()

def send(template, recipient):
    msg = {
        "from": "test outbound <nobody@nowhere.com>",
        "to": "recipient <martin@no.ucant.org>",
        "subject": "the subject",
        "message": template
        }
    payload = json.dumps(msg)
    hand_off(payload)

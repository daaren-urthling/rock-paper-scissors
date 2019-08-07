#!/usr/bin/env python
import pika
import game_objects

#------------------------------------------------------------------------------
def on_request(ch, method, props, body):

    # request = game_objects.json2obj(body.decode('utf-8'))
    request = game_objects.Action.fromJson(body.decode('utf-8'))

    print (f"Player {request.value} has joined the game")

    ch.basic_publish(
        exchange='',
        routing_key='log',
        body=f"Player {request.value} has joined the game"
    )
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id = props.correlation_id),
        body=f"Welcome, {request.value}"
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

#==============================================================================
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.queue_declare(queue='game')
channel.queue_declare(queue='log')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='game', on_message_callback=on_request)

print("Awaiting players to connect")
channel.start_consuming()
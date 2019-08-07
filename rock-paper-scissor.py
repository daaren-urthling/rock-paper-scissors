#!/usr/bin/env python
import pika
import uuid
import json
import game_objects

def on_response(ch, method, props, body):
    print("[private] ",body.decode('utf-8'))

def on_log(ch, method, props, body):
    print(body.decode('utf-8'))

server = input("Game Server ")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=server))
channel = connection.channel()
result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue
channel.basic_consume(
    queue=callback_queue,
    on_message_callback=on_response,
    auto_ack=True
)
channel.basic_consume(
    on_message_callback=on_log,
    queue='log',
    auto_ack=True
)
player = input("Player name ")
request = game_objects.Action('join', player)
channel.basic_publish(
    exchange='',
    routing_key='game',
    properties=pika.BasicProperties(
        reply_to=callback_queue,
        correlation_id='0'
    ),
    body=request.toJson()
)
while True:
    connection.process_data_events()

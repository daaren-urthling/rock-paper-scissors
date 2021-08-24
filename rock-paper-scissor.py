#!/usr/bin/env python
import pika
import uuid
import json
import game_objects

playerID = None

def on_private(ch, method, props, body):
    msg = game_objects.Message.fromJson(body.decode('utf-8'))
    if msg.action == "message":
        print("[private] ", msg.value)
    elif msg.action == "joined":
        print("[private] ", msg.value)
        playerID = msg.playerID
        print(f"joined as Player {playerID}")


def on_log(ch, method, props, body):
    msg = game_objects.Message.fromJson(body.decode('utf-8'))
    if msg.action == "message":
        print(msg.value)

server = input("Game Server ")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=server))
channel = connection.channel()
result = channel.queue_declare(queue='', exclusive=True)
private_queue = result.method.queue
channel.basic_consume(
    queue=private_queue,
    on_message_callback=on_private,
    auto_ack=True
)
channel.basic_consume(
    queue='log',
    on_message_callback=on_log,
    auto_ack=True
)
player = input("Player name ")
request = game_objects.Message('join', player)
channel.basic_publish(
    exchange='',
    routing_key='game',
    properties=pika.BasicProperties(
        reply_to=private_queue,
        correlation_id='0'
    ),
    body=request.toJson()
)
while True:
    connection.process_data_events()

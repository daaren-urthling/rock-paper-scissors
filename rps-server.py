#!/usr/bin/env python
import pika
import game_objects

player1 = None
player2 = None

#------------------------------------------------------------------------------
def on_request(ch, method, props, body):

    request = game_objects.Message.fromJson(body.decode('utf-8'))
    if request.action == "join":
        response = game_objects.Message("message", f"Player {request.value} has joined the game")
        print (response.value)

        ch.basic_publish(
            exchange='',
            routing_key='log',
            body=response.toJson()
        )
        response =  game_objects.Message("joined", f"Welcome, {request.value}")
        global player1, player2
        if player1 == None:
            player1 = request.value
            response.playerID = 1
        else:
            player2 = request.value
            response.playerID = 2
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id = props.correlation_id),
            body=response.toJson()
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
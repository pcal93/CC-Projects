#!/usr/bin/env python3
import connexion
import time
import pika
import threading
from swagger_server import encoder
from swagger_server.controllers import containers_controller


lock = threading.Lock()


def rabbit_setup():
    # Connect to a queue
    connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.3.201'))
    channel = connection.channel()
    channel.queue_purge('risposte')
    queue_state = channel.queue_declare(queue='risposte', durable=True, passive=True)
    
    # Subscribe to the queue and assign the callback
    channel.basic_consume(queue='risposte', on_message_callback=callback, auto_ack=True)
    
    #start to listen, and when a msg reply comes jump to callback function
    channel.start_consuming()


# Define a callback invoked every time a message is received from agents
def callback(ch, method, properties, body):
      
      decoded_body = body.decode('ascii')
      header, payload = decoded_body.split('&')
      print("[V] Received updated list of active containers from "+ header)
      
      if header in containers_controller.list_containers:
        containers_controller.list_containers.pop(header)
      
      append_list = []
      pair_list = payload.split("@")
      for st in pair_list:
        dit = eval(st)
        if(dit["host"] == "---"):
          containers_controller.list_containers[header] = ""
          return
        append_list.append(dit)
        
      containers_controller.list_containers[header] = append_list
          

# Function to start the APIs
def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Docker Containers Monitoring System'})
    app.run(port=8080)
    

if __name__ == '__main__':
    x = threading.Thread(target=rabbit_setup)
    x.start() 
    y = threading.Thread(target=main)
    y.start() 
    
    
    

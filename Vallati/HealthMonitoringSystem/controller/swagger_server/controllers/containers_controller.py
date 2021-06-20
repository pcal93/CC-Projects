import connexion
import six
import docker
import pika
import uuid
import os
import time
import threading
from swagger_server import util


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.3.201'))
channel = connection.channel()
list_containers = {}
lock = threading.Lock()


def get_containers_list(): 
    
    #purging global variables
    global list_containers
    
    unpack = list_containers.items()  # { (172.16.3.201, [host_ip, container_id, etc.]) / (172.16.3.202, [...]) ... }
    for item in unpack:
      key, value = item  # key = 172.16.3.201, value = [host_ip, container_id, etc.]
      print("\n>> Active containers list from "+ key)
      print ("{:<15} {:<15} {:<30} {:<20} {:<20}".format('Host','Id','Name','Ip Address', 'Update Timestamp'))
      
      for nested_dictionary in value:
        host, id, name, ip_add, timestamp = nested_dictionary.values()
        print ("{:<15} {:<15} {:<30} {:<20} {:<20}".format(host, id, name, ip_add, timestamp))
    
    print("\n")
    risposta = str(list_containers)
    return risposta



def monitor_all_containers_on_host(host):

    channel.exchange_declare(exchange='containers', exchange_type='fanout')

    channel.basic_publish(exchange='containers', routing_key='', body='start_monitoring_all_containers@'+host)
    
    confirm_msg = "New monitorizing request has been sent successfully to "+host+" !"
    print(confirm_msg)
    
    return confirm_msg 
    


def stop_monitorizing_all_containers_on_host(host):

    channel.exchange_declare(exchange='containers', exchange_type='fanout')

    channel.basic_publish(exchange='containers', routing_key='', body='stop_monitoring_all_containers@'+host)
    
    confirm_msg = "New monitorizing request has been sent successfully to "+host+" !"
    print(confirm_msg)
    
    return confirm_msg 
    


def set_monitored_container(host, containerID): 

    channel.exchange_declare(exchange='containers', exchange_type='fanout')

    channel.basic_publish(exchange='containers', routing_key='', body='new_container_to_be_monitorized@'+host+'@'+containerID)
    
    confirm_msg = "New monitorizing request has been sent successfully to "+host+" !"
    print(confirm_msg)
    
    return confirm_msg
   
    

def stop_monitorizing_container(host, containerID): 
    
    # Create a queue
    channel.exchange_declare(exchange='containers', exchange_type='fanout')

    channel.basic_publish(exchange='containers', routing_key='', body='stop_monitor_container@'+host+'@'+containerID)
    
    confirm_msg = "Stop monitorizing request has been sent successfully to "+host+" !"
    print(confirm_msg)
    
    return confirm_msg


    

def change_treshold(treshold_value): 
    new_treshold = str(treshold_value)

    # Create a queue
    channel.exchange_declare(exchange='containers', exchange_type='fanout')

    channel.basic_publish(exchange='containers', routing_key='', body='set_new_treshold_value@'+new_treshold)
    
    confirm_msg = "New treshold ("+new_treshold+") value has been correctly updated!"
    print(confirm_msg)
       
    return confirm_msg
    

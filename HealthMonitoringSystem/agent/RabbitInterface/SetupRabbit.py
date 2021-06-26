import pika
import configparser

from ContainerManagement import Handler

# Load parameters from Config.ini
config = configparser.ConfigParser()
config.read("agent/config.ini")

my_ip = config['host']['my_ip']
treshold = float(config['host']['treshold'])
rabbit_server_ip = config['server']['broker_ip']
rabbit_server_port = config['server']['broker_port']


def setup_rabbit():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_server_ip, port=rabbit_server_port))
    channel = connection.channel()
    channel.exchange_declare(exchange='containers', exchange_type='fanout')

    # I let the system to create the queue name
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to one or more keys/exchanges (it can be done at runtime)
    channel.queue_bind(exchange='containers', queue=queue_name, routing_key='')

    # Setting the callback function as the one to be triggered every time a command is received
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Agents will block here waiting for incoming commands to execute
    print('[*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


# Define a callback invoked every time a message is received
def callback(ch, method, properties, body):
    # Get the command sent by the Controller (172.16.3.201) through APIs
    body_decoded = body.decode('ascii')
    body_splitted = body_decoded.split('@')
    command = body_splitted[0]
    if len(body_splitted) == 2:
        payload = body_splitted[1]
    elif len(body_splitted) == 3:
        host_ip = body_splitted[1]
        containerID_to_be_monitorized = body_splitted[2]

    # Multiplexing the actions to perform basing on the content of the command received

    # OPTION 1
    if command == "set_new_treshold_value":
        # Trimming the body value to get the new treshold value
        # new_treshold = float(payload)
        Handler.update_treshold(float(payload))
        print("[V] New treshold value received: %r" % payload)



    # OPTION 2
    elif command == "new_container_to_be_monitorized" and host_ip == my_ip:
        # Inserting the id of the container into the list of the monitorized ones
        Handler.add_to_monitorized(containerID_to_be_monitorized)
    elif command == "new_container_to_be_monitorized":
        return


    # OPTION 3
    elif command == "stop_monitor_container" and host_ip == my_ip:
        Handler.stop_monitorizing_container(containerID_to_be_monitorized)
    elif command == "stop_monitor_container":
        return

    # OPTION 4
    elif command == "start_monitoring_all_containers" and payload == my_ip:
        Handler.start_monitoring_all_containers()
    elif command == "start_monitoring_all_containers":
        return

    # OPTION 5
    elif command == "stop_monitoring_all_containers" and payload == my_ip:
        Handler.stop_monitoring_all_containers()
    elif command == "stop_monitoring_all_containers":
        return


    # ESCAPE OPTION
    else:
        print("[x] Error: unknown command!")

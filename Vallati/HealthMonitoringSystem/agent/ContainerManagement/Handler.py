import pika
import docker
import threading
import configparser
from datetime import datetime

# Load parameters from Config.ini
config = configparser.ConfigParser()
config.read("config.ini")

my_ip = config['host']['my_ip']
treshold = float(config['host']['treshold'])
rabbit_server_ip = config['server']['broker_ip']
rabbit_server_port = config['server']['broker_port']

monitorized_containers = []

lock = threading.Lock()


def update_treshold(new_treshold):
    global treshold
    treshold = new_treshold
    return


def kill_and_restart_container(target_container):
    global monitorized_containers

    container = ""

    client = docker.from_env()
    try:
        container = client.containers.get(target_container.get("id"))
    except:
        print("[X] Error: the Container with ID: " + target_container.get("id") + " does not exist anymore!")
        return

    if container.status == "exited":
        print("[X] Error: the Container with ID: " + target_container.get("id") + " does not exist anymore!")
        stop_monitorizing_container(target_container.get("id"))
        return

    name_cont = target_container.get("name")
    image = target_container.get("image")

    container.stop()
    container.remove()
    print("[*] Stopping Container ID: " + target_container.get("id"))

    # Deleting the old container from the monitorized list
    container = client.containers.run(image, name=name_cont, detach=True)
    with lock:
        monitorized_containers = [i for i in monitorized_containers if not (i["id"] == target_container.get("id"))]

    print("[V] Container restarted with new ID: " + container.short_id)

    # Start monitoring the restarted container
    add_to_monitorized(container.short_id)
    return


def add_to_monitorized(target_container_id):
    global monitorized_containers

    client = docker.from_env()
    # Check if the requested container is actually running on the target host
    try:
        container = client.containers.get(target_container_id)
    except:
        print("[X] The requested container does not exist on this host!")
        return

    if any(item['id'] == target_container_id for item in monitorized_containers):
        print("[X] Error: the requested container is already monitorized !")
        return

    ip_addr = str(container.attrs["NetworkSettings"]["IPAddress"])
    dict_cont = {"id": target_container_id, "name": container.name, "ip_address": ip_addr, "image": container.image}
    with lock:
        monitorized_containers.append(dict_cont)

    print("[V] Container "+ container.name + " ( " + target_container_id + " ) added to the monitoring list!")
    return


def stop_monitorizing_container(target_container_id):
    global monitorized_containers

    # If client request to stop monitorizing but never asked to monitor one before, return
    if not monitorized_containers:
        print("[X] Error: the monitorized containers list is empty!")
        return

    # Check if the requested container is currently monitorized
    if not any(item['id'] == target_container_id for item in monitorized_containers):
        print("[X] Error: the requested container is not monitorized yet!")
        return

    with lock:
        # Updating the monitorized_containers list by deleting the target container
        monitorized_containers = [i for i in monitorized_containers if not (i['id'] == target_container_id)]
    print("[V] Container " + target_container_id + " deleted from the monitoring list!")
    return


def start_monitoring_all_containers():
    global monitorized_containers

    client = docker.from_env()

    for container in client.containers.list():
        if not any(item['id'] == container.short_id for item in monitorized_containers):
            add_to_monitorized(container.short_id)

    print("[V] All the running containers have been added to the monitoring list!")
    return


def stop_monitoring_all_containers():
    global monitorized_containers

    # If client request to stop monitorizing but never asked to monitor one before, return
    if not monitorized_containers:
        print("[X] Error: the monitorized containers list is empty!")
        return

    for container in monitorized_containers:
        stop_monitorizing_container(container['id'])

    print("[V] All the monitorized containers have been deleted from the monitoring list!")
    return


def get_active_containers():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_server_ip, port=rabbit_server_port))
    channel = connection.channel()

    # Create a queue to send the reply
    channel.queue_declare(queue='risposte')
    # Gather the list of the Docker Container Up & Running
    client = docker.from_env()
    running_containers = my_ip + "&"

    if not client.containers.list():

        print('[X] No Active containers running!')
        now = datetime.now()
        now = now.strftime("%d-%m-%Y, %H:%M:%S")
        running_containers += "{'host': '" + "---" + "', 'id': '" + "---" + "', 'name': '" + "---" + "', 'ip_address': '" + "---" + "', 'update_timestamp': '" + now + "'}"

    else:

        num_containers = len(client.containers.list())
        for n, container in enumerate(client.containers.list()):
            container_ip = str(container.attrs["NetworkSettings"]["IPAddress"])
            now = datetime.now()
            now = now.strftime("%d-%m-%Y, %H:%M:%S")

            # Handling the EOF of the string
            if n == num_containers - 1:
                running_containers += "{'host': '" + my_ip + "', 'id': '" + container.short_id + "', 'name': '" + container.name + "', 'ip_address': '" + container_ip + "', 'update_timestamp': '" + now + "'}"
            else:
                running_containers += "{'host': '" + my_ip + "', 'id': '" + container.short_id + "', 'name': '" + container.name + "', 'ip_address': '" + container_ip + "', 'update_timestamp': '" + now + "'}@"
                
        print('[V] Active containers list sent !')
    # Send the message with the list of the active containers
    channel.basic_publish(exchange='', routing_key='risposte', body=running_containers)
    return

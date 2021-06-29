import time
import docker
import subprocess

from subprocess import PIPE
from random import randint
from random import seed

loss_percentage = '15%'

UNREMOVABLE_CONTAINERS = ["some-rabbit"]

print("Add PAcket Loss")

command = subprocess.run(['tc', 'qdisc', 'add', 'dev', 'docker0', 'root', 'netem', 'loss', loss_percentage], stdout=PIPE, stderr=PIPE)

cmd_str = command.stderr.decode("ascii").strip("\n")

if cmd_str == "RTNETLINK answers: File exists":
    command = subprocess.run(['tc', 'qdisc', 'change', 'dev', 'docker0', 'root', 'netem', 'loss', loss_percentage], stdout=PIPE, stderr=PIPE)
    
while 1:
    
    time.sleep(10)
    

    client = docker.from_env()

    aux = client.containers.list()
    
    upper_bound = len(client.containers.list())-1

    value = randint(0, upper_bound)


    container = aux[value]

    if container.name not in UNREMOVABLE_CONTAINERS:
        print(container.name) 
        container.stop()
        container.remove()

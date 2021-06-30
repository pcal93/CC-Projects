import time
import docker
import subprocess

from subprocess import PIPE
from random import randint

def rollDice():
    roll = randint(1,100)

    if roll <= 20:
        return False
    else:
        return True
        

loss_percentage = '15%'

UNREMOVABLE_CONTAINERS = ["some-rabbit"]

print("[V] Antagonist program started")

command = subprocess.run(['tc', 'qdisc', 'add', 'dev', 'docker0', 'root', 'netem', 'loss', loss_percentage], stdout=PIPE, stderr=PIPE)

cmd_str = command.stderr.decode("ascii").strip("\n")

if cmd_str == "RTNETLINK answers: File exists":
    command = subprocess.run(['tc', 'qdisc', 'change', 'dev', 'docker0', 'root', 'netem', 'loss', loss_percentage], stdout=PIPE, stderr=PIPE)
    
while 1:
    
    time.sleep(20)

    if not rollDice():
        continue
        
    client = docker.from_env()

    aux = client.containers.list()
    
    upper_bound = len(client.containers.list())-1

    if upper_bound < 0:
      continue
      
    value = randint(0, upper_bound)
    
    container = aux[value]

    if container.name not in UNREMOVABLE_CONTAINERS:
        print("[X] Antagonist program has just shutted down the container: "+container.name) 
        container.stop()
        container.remove()

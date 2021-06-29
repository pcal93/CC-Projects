import time
import docker
import subprocess
import random

from subprocess import PIPE
from random import randint
from random import seed


def rollDice():
    roll = random.randint(1,100)

    if roll <= 50:
        return False
    elif roll >= 51:
        return True
        

loss_percentage = '15%'

UNREMOVABLE_CONTAINERS = ["some-rabbit"]

print("[V] Antagonist program started")

command = subprocess.run(['tc', 'qdisc', 'add', 'dev', 'docker0', 'root', 'netem', 'loss', loss_percentage], stdout=PIPE, stderr=PIPE)

cmd_str = command.stderr.decode("ascii").strip("\n")

if cmd_str == "RTNETLINK answers: File exists":
    command = subprocess.run(['tc', 'qdisc', 'change', 'dev', 'docker0', 'root', 'netem', 'loss', loss_percentage], stdout=PIPE, stderr=PIPE)
    
while 1:
    
    time.sleep(120)

    if rollDice():
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

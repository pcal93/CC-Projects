import time
import threading

from ContainerManagement import Pinger
from ContainerManagement import Handler
from RabbitInterface import SetupRabbit


def send_periodic_container_updates():
    while True:
        Handler.get_active_containers()
        time.sleep(20)

if __name__ == "__main__":

    x = threading.Thread(target=Pinger.ping_containers)
    x.start()
    y = threading.Thread(target=SetupRabbit.setup_rabbit)
    y.start()
    z = threading.Thread(target=send_periodic_container_updates)
    z.start()
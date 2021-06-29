import time
import pingparsing

from ContainerManagement import Handler


def ping_containers():
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()

    while True:

        time.sleep(10)
        
        if not Handler.monitorized_containers:
            time.sleep(2)
            continue

        for item in Handler.monitorized_containers:

            transmitter.destination = item.get("ip_address")
            transmitter.count = 10
            result = transmitter.ping()
            result_dict = ping_parser.parse(result).as_dict()

            if result_dict.get('packet_loss_rate') >= Handler.treshold:
                print("[X] Ping NOT GOOD (" +
                      str(result_dict.get('packet_loss_rate')) +
                      "% PL) - deleting and restarting container " +
                      item.get("name") + " ...")
                Handler.kill_and_restart_container(item)
            else:
                print("[V] Ping OK " +
                      item.get("name") + ' - PL %: ' + str(result_dict.get('packet_loss_rate')))

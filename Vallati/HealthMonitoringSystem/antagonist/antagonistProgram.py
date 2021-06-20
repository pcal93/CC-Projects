import subprocess
import sys
from subprocess import PIPE


'''RITARDO'''

'''
# inserire un ritardo di 200ms
command = subprocess.run(['tc', 'qdisc', 'add', 'dev', 'docker0', 'root', 'netem', 'delay', '200ms'], stdout=PIPE, stderr=PIPE)
'''
'''
# modificare il valore del ritardo inserito
command = subprocess.run(['tc', 'qdisc', 'change', 'dev', 'docker0', 'root', 'netem', 'delay', '500ms'], stdout=PIPE, stderr=PIPE)
'''
'''
# rimuovere il ritardo inserito
command = subprocess.run(['tc', 'qdisc', 'del', 'dev', 'docker0', 'root', 'netem', 'delay', '500ms'], stdout=PIPE, stderr=PIPE)
'''



'''PERDITA DI PACCHETTI'''

'''
# inserire una packet_loss del 15%
command = subprocess.run(['tc', 'qdisc', 'add', 'dev', 'docker0', 'root', 'netem', 'loss', '15%'], stdout=PIPE, stderr=PIPE)
'''
'''
# modificare il valore della packet_loss inserita
command = subprocess.run(['tc', 'qdisc', 'change', 'dev', 'docker0', 'root', 'netem', 'loss', '15%'], stdout=PIPE, stderr=PIPE)
'''
'''
# rimuovere la packet_loss inserita
command = subprocess.run(['tc', 'qdisc', 'del', 'dev', 'docker0', 'root', 'netem', 'loss', '15%'], stdout=PIPE, stderr=PIPE)
'''


sys.stdout.buffer.write(command.stdout)
sys.stderr.buffer.write(command.stderr)
sys.exit(command.returncode)

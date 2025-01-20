import socket
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from logic.bob import Bob
from logic.food import Food
from logic.item import Item
default_port = 55005

def send_grid(grid):
    """Extraire les déplacements des bobs pour les envoyer

    Args:
        grid (Grid): grille du jeu
    """
    for l in grid.map.keys():
        for b in grid.map[l]:
            if isinstance(b, Bob):
                x1,y1 = [a-b for a,b in zip(l, b.last_move)]
                x2,y2 = l
                if (x1 != x2 or y1 != y2):
                    s = f"DEPLACE|{x1:02},{y1:02}|{x2:02},{y2:02} \0"
                    send_info_to_C(portnum, MSG=s.encode('ascii'))


def send_DPL(pos, bob, portnum=default_port):
    """Extraire le déplacement du bob pour l'envoyer
    Args:
        pos (tuple): tuple des coordonnées du bob
        bob (Bob): bob à envoyer
    """
    x1, y1 = [a-b for a,b in zip(pos, bob.get_last_move())]
    if (x1 != pos[0] or y1 != pos[1]):
        # DPL	id	x1	y1	x2	y2
        s = f"DPL{bob.get_id():15}{x1:4}{y1:4}{pos[0]:4}{pos[1]:4}\0"
        #s = f"DPL{x1:4}{y1:4}{pos[0]:4}{pos[1]:4}" # pour tester
        send_info_to_C(portnum, MSG=s.encode('ascii'))


def send_PLC(pos, thing,portnum=default_port):
    #
    #|      `PLC`    |   id   |    x1   |    y1   |     item    |    E    |    M    |      M      |
    id = thing.get_id()
    energy = 0
    masse = 0
    move = 0
    if isinstance(thing,Bob) : #boborfood is a boolean if true then is bob
        typeitem = 'B' #pas sur qu'on ecrive vraiment comme sa le type TODO
        energy = int(thing.get_E())
        masse =int(thing.get_mass())
        move = int(thing.get_speed())
    else:
        typeitem = 'F'
        energy = int(thing.get_energy())
    
    s = f"PLC{id:15}{pos[0]:4}{pos[1]:4}{typeitem:1}{energy:4}{masse:4}{move:4} \0"
    send_info_to_C(portnum, MSG=s.encode('ascii'))

def send_EAT(pos,bob:Bob,food:Food,portnum):
    idbob = bob.get_id()
    idfood = food.get_id()
    hunger = int(bob.get_Emax() - bob.get_E())
    if hunger > food.get_energy():
        to_eat = int(food.get_energy())
    else:
        to_eat = hunger

    s = f"EAT{idbob:15}{pos[0]:4}{pos[1]:4}{to_eat:4}{idfood:15} \0"
    send_info_to_C(portnum, MSG=s.encode('ascii'))

def send_ATK(atk:Bob,pos,target:Bob,portnum):
    idatk = atk.get_id()
    idtgt = target.get_id()
    s = f"ATK{idatk:15}{pos[0]:4}{pos[1]:4}{idtgt:15}\0"
    send_info_to_C(portnum, MSG=s.encode('ascii'))

def send_DSP(thing:Item,pos,portnum):
    id = thing.get_id()
    s = f"DSP{id:15}{pos[0]:4}{pos[1]:4}\0"
    send_info_to_C(portnum, MSG=s.encode('ascii'))


def send_info_to_C (portnum=default_port, MSG=b'DEPLACE|x1,y1|x2,y2 \0') :
    #print(f'sending on {portnum} port')
    UDP_IP = "127.0.0.1"
    UDP_PORT = portnum
    MESSAGE = MSG
    # print("UDP target IP: %s" % UDP_IP)
    # print("UDP target port: %s" % UDP_PORT)
    # print("message: %s" % MESSAGE)
 
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

def send_ANP(pos,portnum=default_port):
    #Envoie une demande de prop réseau
    #|      `ANP`   |    x1   |    y1   
    s = f"ANP{pos[0]:4}{pos[1]:4}"
    send_info_to_C(portnum, MSG=s.encode('ascii'))

if __name__ =='__main__':
    if sys.argv[1]: portnum = int(sys.argv[1])
    else: portnum = default_port
    send_PLC(True,portnum)

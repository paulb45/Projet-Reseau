import socket
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from logic.bob import Bob

default_port = 55005

def send_grid(grid):
    """Extraire les déplacements des bobs pour les envoyer

    Args:
        grid (Grid): grille du jeu
    """
    for l in grid.map.keys():
        for b in grid.map[l]:
            if isinstance(b, Bob):
                x1,y1 = [a+b for a,b in zip(l, b.last_move)]
                x2,y2 = l
                if (x1 != x2 or y1 != y2):
                    s = f"DEPLACE|{x1:02},{y1:02}|{x2:02},{y2:02} \0"
                    send_info_to_C(portnum, MSG=s.encode('ascii'))


def send_bob(pos, bob, portnum=default_port):
    """Extraire le déplacement du bob pour l'envoyer
    Args:
        pos (tuple): tuple des coordonnées du bob
        bob (Bob): bob à envoyer
    """
    x1, y1 = [a+b for a,b in zip(pos, bob.get_last_move())]
    id = '000000000000000'
    # DPL	id	x1	y1	x2	y2
    s = f"DPL{id}{x1:4}{y1:}{pos[0]:4}{pos[1]:4}"
    #s = f"DPL{x1:4}{y1:4}{pos[0]:4}{pos[1]:4}" # pour tester
    send_info_to_C(portnum, MSG=s.encode('ascii'))

def send_info_to_C (portnum=default_port, MSG=b'DEPLACE|x1,y1|x2,y2 \0') :
    UDP_IP = "127.0.0.1"
    UDP_PORT = portnum
    MESSAGE = MSG
    # print("UDP target IP: %s" % UDP_IP)
    # print("UDP target port: %s" % UDP_PORT)
    # print("message: %s" % MESSAGE)
 
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

if __name__ =='__main__':
    if sys.argv[1]: portnum = int(sys.argv[1])
    else: portnum = default_port
    send_info_to_C(portnum)

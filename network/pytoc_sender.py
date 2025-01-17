import socket
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from logic.bob import Bob

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
                    send_info_to_C(MSG=s.encode('ascii'))


def send_bob(pos, bob):
    """Extraire le déplacement du bob pour l'envoyer
    Args:
        pos (tuple): tuple des coordonnées du bob
        bob (Bob): bob à envoyer
    """
    x1, y1 = [a+b for a,b in zip(pos, bob.get_last_move())]
    id = '0000000000'
    # DPL	id	x1	y1	x2	y2
    # s = f"DPL{id}{x1:5}{y1:5}{pos[0]:5}{pos[1]:5}"
    s = f"DPL{x1:4}{y1:4}{pos[0]:4}{pos[1]:4}" # pour tester
    send_info_to_C(MSG=s.encode('ascii'))


def turnmsg_dpl_tobinary(oldposition, newposition):
    oldx=str(format(oldposition[0],'b'))
    oldy=str(format(oldposition[1],'b'))
    newx=str(format(newposition[0],'b'))
    newy=str(format(newposition[1],'b'))
    msg = oldx+oldy+newx+newy
    return msg

#def turnmsg_plc_tobinary():

#def turnmsg_eat_tobinary():

#def turnmsg_atk_tobinary():

#def turnmsg_dsp_tobinary():

#def turnmsg_new_tobinary():    

    

def send_info_to_C (portnum=55005, MSG=b'DEPLACE|x1,y1|x2,y2 \0') :
    UDP_IP = "127.0.0.1"
    UDP_PORT = portnum
    MESSAGE = MSG
    # print("UDP target IP: %s" % UDP_IP)
    # print("UDP target port: %s" % UDP_PORT)
    # print("message: %s" % MESSAGE)
 
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

if __name__ =='__main__':
    #send_info_to_C(55005,b'DEPLACE|10,10|12,12')
    x=turnmsg_dpl_tobinary((12,13),(14,15))
    print(x)
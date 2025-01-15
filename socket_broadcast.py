import socket
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


def send_info_to_C (portnum=55005, MSG=b'DEPLACE|x1,y1|x2,y2 \0') :
    UDP_IP = "127.0.0.1"
    UDP_PORT = portnum
    MESSAGE = MSG
    print("UDP target IP: %s" % UDP_IP)
    print("UDP target port: %s" % UDP_PORT)
    print("message: %s" % MESSAGE)
 
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

if __name__ =='__main__':
    send_info_to_C(55005,b'DEPLACE|10,10|12,12')
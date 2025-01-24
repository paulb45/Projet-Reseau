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
                    s = f"DEPLACE|{x1:02},{y1:02}|{x2:02},{y2:02}\0"
                    send_info_to_C(55005, MSG=s.encode('ascii'))


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
    
    s = f"PLC{id:15}{pos[0]:4}{pos[1]:4}{typeitem:1}{energy:4}{masse:4}{move:4}\0"
    send_info_to_C(portnum, MSG=s.encode('ascii'))

def send_EAT(pos,bob:Bob,food:Food,portnum):
    idbob = bob.get_id()
    idfood = food.get_id()
    hunger = int(bob.get_Emax() - bob.get_E())
    if hunger > food.get_energy():
        to_eat = int(food.get_energy())
    else:
        to_eat = hunger

    s = f"EAT{idbob:15}{pos[0]:4}{pos[1]:4}{to_eat:4}{idfood:15}\0"
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


def send_info_to_C (portnum:int,MSG:str,socketfd:socket.socket=None) :
    if socketfd != None:
        socketfd.sendto(MSG,("127.0.0.1",portnum))
        #print("sent message")
    else:
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.sendto(MSG,("127.0.0.1",portnum))


    # print("UDP target IP: %s" % UDP_IP)
    # print("UDP target port: %s" % UDP_PORT)
    # print("message: %s" % MESSAGE)
 
    # sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    # sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

def send_ANP(pos,myid, portnum=default_port):
    #Envoie une demande de prop réseau, on précise son id de joueur
    #|      `ANP`   |  myid |  x1   |    y1   
    s = f"ANP{myid:15}{pos[0]:4}{pos[1]:4}\0"
    send_info_to_C(portnum, MSG=s.encode('ascii'))

def send_GNP(pos, grid, idjoueur, portnum=default_port):
    #Réponse a un ANP pour donner la propriété réseau.

    #On indique l'item qui est sur la case (food ou bob), par défaut None.
    #GNP | id | x | y | idbob | M1 | idfood | E2
    #Idjoueur est l'id du joueur à qui on cède la propriété

    #Valeurs pas défaut: 
    print("ENVOIE DE GNP")
    print("POSITION : ", pos)
    items = grid.get_items(pos) #Comment récupérer les items de l'objet grid, sachant que grid n'est pas global ? 
                #Le truc en dessous c'est pour recup l'info de ce qu'il y a sur la case, 
                # et c'est sensé marcher car il y a au + 1 seul bob et une seul food sur une case. 
    bob = None
    food = None
    for el in items :
        if isinstance(el,Bob):
            bob = el
        elif isinstance(el, Food):
            food = el

    bob_id = 0
    bob_masse = 0
    food_id = 0
    food_energy = 0

    if bob is not None:
        bob_id = bob.get_id()
        bob_masse = bob.get_mass()
        print("bob_id = ", bob_id)
    if food is not None :
        food_id = food.get_id()
        food_energy = food.get_energy()
        
    s = f"GNP{idjoueur:15}{pos[0]:4}{pos[1]:4}{bob_id:15}{bob_masse:4}{food_id:15}{food_energy:4}\0"
    send_info_to_C(portnum, MSG=s.encode('ascii'))

def send_RNP(pos, portnum=default_port):
    #Réponse a un ANP pour REFUSER de donner la propriété réseau.

    #GNP | x | y         
    s = f"RNP{pos[0]:4}{pos[1]:4}\0"
    send_info_to_C(portnum, MSG=s.encode('ascii'))

if __name__ =='__main__':
    if sys.argv[1]: portnum = int(sys.argv[1])
    else: portnum = default_port
    bob  = Bob(bob_id=3, mass=10, local=False)
    food = Food(food_id=4, energy = 15, local=False)
    from network_property import Network_property
    # # send_GNP((1,2), 1, bob, food)
    # Network_property.add_appartenance(1,2)
    # print(Network_property.get_np_grid())
    # send_ANP((1,2), 1)
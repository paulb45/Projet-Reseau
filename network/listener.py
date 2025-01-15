import socket
import re

from network.action_buffer  import ActionBuffer

def splitwithpipe(input_str,i):
    #splits text along the pipe use i=0 for first half i=1 for second half
    return input_str.split('|')[i]

def texttotuple(input_str,splitchr):
    #turns text into a tuple useful for getting slime adress in a usable format
    return tuple(map(int, input_str.split(splitchr)))

def checkpattern(stringtocheck,pattern):
    #checks if the string matches the input pattern and returns bool 
    #print(pattern)
    #print(stringtocheck)
    if re.fullmatch(pattern, stringtocheck):
        return True
    else: return False

def readposistionfrombynary(data):
    x=int(data[0:32],2)
    y =int(data[32:64],2)
    return (x,y)

def startlisten(IP="127.0.0.1",port=55005):
    #opens a socket to listen to the C process
    UDP_IP =  IP
    UDP_PORT = port
    #Deplace_pattern = r"^\d+,\d+\|\d+,\d+$"
    #EAT_pattern=r"^\d+\|\d+,\d+\|\d+,\d+$" #TO TEST //////
    sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    boolstop=True
    #the while loop analyses the messages as they arrive if a message matches the protocol adds an acction to the action buffer
    while boolstop:
        #print("inloop")
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        #print(data)
        data=data.decode('ascii')
        #print(data)
        #socket messages arrive encoded in ASCII they are decoded for ease of use
        #check if sender wants to stop probably not useful but I don't like infinite loops
        if data == 'STOP':
            boolstop=False
        #test if the sender wants to perform a DPL action
        elif data.startswith('010001000101000001001100'): #code binaire pour DPL
            #print("startswith works")
            data=data[24:] #degage l'entete action
            #print("received message: %s" % data)
            lastpostion=readposistionfrombynary(data)
            data=data[64:]# degage les données 
            #print(f"lastposition =  {lastpostion}") # might be usefull for further testing
            nextposition=readposistionfrombynary(data)
            data=data[64:]# degage les données
            #print("deplace works") 
            #print(f"nextposition = {nextposition}") # might be usefull for further testing
            ActionBuffer.add_move(lastpostion,nextposition)
            
        elif data.startswith('010100000100110001000011'): # code binaire pour PLC
            data=data[24:] #degage l'entete 
            Position = readposistionfrombynary(data)
            data=data[64:]
            Type = int(data[0:32],2)
            data=data[32:]
            Energie = int(data[0:32],2)
            data=data[32:]
            Masse = int(data[0:32],2)
            data=data[32:]
            Mouvement = int(data[0:32],2)
            #print("place works")
            # Type d'action | Timestamp  | Coord x | Coord y | Type d'item | Energie | Masse | Mouvement |
            #ActionBuffer.add_place(Postion,Type,Energie,Masse, Mouvement) # TO DO after implémentation dans action_buffer
        
        elif data.startswith('010001010100000101010100'): #code bianire pour EAT
            data=data[24:] #degaae l'entente action
            to_eat=int(data[0:32],2)
            data=data[32:]
            position=readposistionfrombynary(data)
            data=data[64:]
            #print("eat works")
            #| Type d'action | Timestamp  | Max to eat | Coord x | Coord y |
            #ActionBuffer.add_eat(to_eat,position)   # TO DO after implémentation dans action_buffer

        elif data.startswith('010000010101010001001011'): #code bianire pour ATK
            data=data[24:] #degaae l'entente action
            position=readposistionfrombynary(data)
            data=data[64:]
            #print("atk works")
            #| Type d'action | Timestamp  | Coord x | Coord y |
            #ActionBuffer.add_eat(position)   # TO DO after implémentation dans action_buffer
        
        elif data.startswith('010001000101001101010000'): #code bianire pour DSP
            data=data[24:] #degaae l'entente action
            position=readposistionfrombynary(data)
            data=data[64:]
            type=int(data[0:32],2)
            data=data[32:]
            #print("dsp works")
            #| Type d'action | Timestamp  | Coord x | Coord y | Type d'item |
            #ActionBuffer.add_eat(position,type)   # TO DO after implémentation dans action_buffer

        elif data.startswith('010011100100010101010111'): #code bianire pour NEW
            data=data[24:] #degaae l'entente action
            masse=int(data[0:32],2)
            data=data[32:]
            statmouvement=int(data[0:32],2)
            data=data[32:]
            #print("new works")
            #| Type d'action | Timestamp  | Masse | Mouvement des Bobs |
            #ActionBuffer.add_eat(masse,statmouvement)   # TO DO after implémentation dans action_buffer
    
    sock.close() # ends the connection
    #print("ended successfuly")
    
if __name__ =='__main__': #allows to run for tests  without breaking everything 
    startlisten()


import socket
from action_buffer  import ActionBuffer

def splitwithpipe(input_str,i):
    #splits text along the pipe use i=0 for first half i=1 for second half
    return input_str.split('|')[i]

def texttotuple(input_str):
    #turns text into a tuple useful for getting slime adress in a usable format
    return tuple(map(int, input_str.split(',')))

def startlisten(IP="127.0.0.1",port=55005):
    UDP_IP =  IP
    UDP_PORT = port

    sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    boolstop=True
    while boolstop:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        data=data.decode('ascii')
        if data == 'STOP':
            boolstop=False
        elif data.startswith('DEPLACE'):
            data=data[8:]
            #print("received message: %s" % data)
            lastpostion=splitwithpipe(data,0)
            #print(lastpostion)
            lastpostion=texttotuple(lastpostion)
            #print(lastpostion)
            nextposition=splitwithpipe(data,1)
            #print(nextposition)
            nextposition=texttotuple(nextposition)
            #print(nextposition)
            ActionBuffer.add_move(lastpostion,nextposition)

    sock.close()
    #print("ended successfuly")
    
startlisten()
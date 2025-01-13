import socket

def splitwithpipe(input_str,i):
    #splits text along the pipe use i=0 for first half i=1 for second half
    return input_str.split('|')[i]

def texttotuple(input_str):
    #turns text into a tuple useful for getting slime adress in a usable format
    return tuple(map(int, input_str.split(',')))

UDP_IP =  "127.0.0.1"
UDP_PORT = 55005


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
        lastpostion=texttotuple(lastpostion)
        #print(lastpostion)
        nextposition=splitwithpipe(data,1)
        nextposition=texttotuple(nextposition)
        #print(nextposition)

sock.close()
print("ended successfuly")
import socket


def send_info_to_C (portnum=55005, MSG=b'DEPLACE|x1,y1|x2,y2 \0') :
    UDP_IP = "127.0.0.1"
    UDP_PORT = portnum
    MESSAGE = MSG
    #print("UDP target IP: %s" % UDP_IP)
    #print("UDP target port: %s" % UDP_PORT)
    #print("message: %s" % MESSAGE)
 
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


send_info_to_C(55005,b'DEPLACE|x1,y1|x2,y2 \0')
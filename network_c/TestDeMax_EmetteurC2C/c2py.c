#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include "network.h"

// ====================================================================================================
//     Programme pour Emmettre un message provenant de C broadcast (d'une autre machine théoriquement)
//                      Emmission du message au receiver en pyhton
// ====================================================================================================
#define DEST_IP "127.0.0.1"  
#define MAX_BUF_SIZE 50

int main(int argc, char *argv[]) {
    int port_python=0;
    int port_broadcast=0;
    setup_ports(argc, argv, &port_python, &port_broadcast);

    int socket_c2py = create_udp_socket();
    struct sockaddr_in py_addr, bind_addr, from_addr;

    // Configuration de l'adresse de Python
    configure_python_addr(&py_addr, port_python, DEST_IP);
    authorized_broadcast(socket_c2py);
    configure_broadcast_addr(&bind_addr, port_broadcast);
    link_socket_to_listen_addr(socket_c2py, &bind_addr);

    char message[MAX_BUF_SIZE];
    socklen_t from_len = sizeof(from_addr);

    while(1){
        listen_socket(socket_c2py, message, MAX_BUF_SIZE, &from_addr, from_len, 0);
        send_message(socket_c2py, message, &py_addr, 0);
        ssize_t sent_bytes = sendto(socket_c2py, message, strlen(message), 0, (struct sockaddr *)&py_addr, sizeof(py_addr));
    }

    close(socket_c2py);

    return 0;
}
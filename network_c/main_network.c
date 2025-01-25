#include <sys/time.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#include "network.h"

// =========================================================================================
//                Programme pour réceptionner un message provenant de python
//     Emmission du message en broadcast au receiver en C (autre machine théoriquement)
// =========================================================================================

int main(int argc, char *argv[]){
    char message[MAX_BUF_SIZE];
    int port_receive_py=0;
    int port_send_broadcast=0;
    int port_send_py=0;
    int port_receive_broadcast=0;
    setup_ports(argc, argv,  &port_receive_py, &port_send_broadcast, &port_send_py, &port_receive_broadcast);

    int socket_c = create_udp_socket();
    authorized_broadcast(socket_c);
    struct sockaddr_in send_addr_c, from_addr_c, rcv_addr_c;
    //Setup de la reception
    configure_broadcast_addr(&from_addr_c, port_receive_broadcast, htonl(INADDR_ANY));
    link_socket_to_listen_addr(socket_c, &from_addr_c);
    //Setup de l'envoi
    configure_broadcast_addr(&send_addr_c, port_send_broadcast, htonl(INADDR_BROADCAST));
    
    setup_udp_buffer(socket_c);


    int socket_py = create_udp_socket();
    struct sockaddr_in send_addr_py, from_addr_py, rcv_addr_py;
    //Setup de la reception
    configure_python_addr(&from_addr_py, port_receive_py, LOCALHOST_ADDRESS);
    link_socket_to_listen_addr(socket_py, &from_addr_py);
    //Setup de l'envoi
    configure_python_addr(&send_addr_py, port_send_py, LOCALHOST_ADDRESS);

    setup_udp_buffer(socket_py);

    fd_set readfds;
    int socket_resolver;

    while(1){
        FD_ZERO(&readfds);
        FD_SET(socket_c, &readfds);
        FD_SET(socket_py, &readfds);
        socket_resolver = select(FD_SETSIZE, &readfds, NULL,NULL,NULL);

        if(socket_resolver > 0){
            if(FD_ISSET(socket_c, &readfds)){
                printf("En attente de message de C\n");
                listen_socket(socket_c, message, MAX_BUF_SIZE, &rcv_addr_c, sizeof(rcv_addr_c), 0);
                printf("Message reçu de C\n");
                send_message(socket_py, message, &send_addr_py, 0);
            }
            if(FD_ISSET(socket_py, &readfds)){
                printf("En attente de message de python\n");
                listen_socket(socket_py, message, MAX_BUF_SIZE, &rcv_addr_py, sizeof(rcv_addr_py), 0);
                printf("Message reçu de python\n");
                send_message(socket_c, message, &send_addr_c, 0);
            }
        }   
    }
    return 0;
}
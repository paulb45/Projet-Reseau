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

// ====================================================================================================
//     Programme pour Emmettre un message provenant de C broadcast (d'une autre machine théoriquement)
//                      Emmission du message au receiver en pyhton
// ====================================================================================================


int main(int argc, char *argv[]){
    char message[MAX_BUF_SIZE];
    int port_receive_py=0;
    int port_send_broadcast=0;
    int port_send_py=0;
    int port_receive_broadcast=0;

    // ensemble de socket
    fd_set socket_set;
    int socket_resolver;

    setup_ports(argc, argv,  &port_receive_py, &port_send_broadcast, &port_send_py, &port_receive_broadcast);

//  creation socket_c2c
    int socket_c2c = create_udp_socket();
    struct sockaddr_in bind_addr_c2c, broadcast_addr, from_addr_c2c;
    socklen_t from_len_c2c = sizeof(from_addr_c2c);

//  creation socket_c2py
    int socket_c2py = create_udp_socket();
    struct sockaddr_in py_addr, bind_addr_c2py, from_addr_c2py;
    socklen_t from_len_c2py = sizeof(from_addr_c2py);

//=================== Config socket ========================
// config bind address socket_c2c
    configure_python_addr(&bind_addr_c2c,  port_receive_py, "NO");
    convert_address(LOCALHOST_ADDRESS, &bind_addr_c2c);
    link_socket_to_listen_addr(socket_c2c, &bind_addr_c2c);
// config bind address socket_c2py
    authorized_broadcast(socket_c2py);
    configure_broadcast_addr(&bind_addr_c2py, port_receive_broadcast);
    link_socket_to_listen_addr(socket_c2py, &bind_addr_c2py);
// config sending address socket_c2c
    authorized_broadcast(socket_c2c);
    configure_broadcast_addr(&broadcast_addr, port_send_broadcast);
    convert_address(BROADCAST_ADDRESS, &broadcast_addr);
// config sending address socket_c2py
    configure_python_addr(&py_addr, port_send_py, LOCALHOST_ADDRESS);

    setup_udp_buffer(socket_c2c);
    setup_udp_buffer(socket_c2py);

    printf("En écoute d'un message python en UDP sur le port %d...\n",  port_receive_py);
    
    //Initialisation du socket_set
    FD_ZERO(&socket_set);
    FD_SET(socket_c2c,&socket_set); //socket_c2c = 3
    FD_SET(socket_c2py, &socket_set); //socket_c2py = 4



    //=================== Reception et envoi des messages ========================
    while (1) {

        socket_resolver = select(5,&socket_set,NULL,NULL,NULL); // 5 car 0,1 et 2 sont réservés
        if(socket_resolver > 0){

            //================ c2c ==============================================
            if(FD_ISSET(socket_c2c,&socket_set)){
                listen_socket(socket_c2c, message, MAX_BUF_SIZE, &from_addr_c2c, from_len_c2c, 0);
                send_message(socket_c2c, message, &broadcast_addr, 0);
            }

            //================ c2py ==============================================
            if(FD_ISSET(socket_c2py,&socket_set)){
                listen_socket(socket_c2py, message, MAX_BUF_SIZE, &from_addr_c2py, from_len_c2py, 0);
                send_message(socket_c2py, message, &py_addr, 0); 
            }
        }   
    }

    close(socket_c2py);
    close(socket_c2c);
    return 0;
}
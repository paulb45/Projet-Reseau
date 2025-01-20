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
    int port_python_c2c=0;
    int port_broadcast=0;
    int port_python_c2py=0;

    setup_ports(argc, argv, &port_python_c2c, &port_broadcast, &port_python_c2py);

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
    configure_sending_addr(&bind_addr_c2c,  port_python_c2c, "NO");
    convert_address(LOCALHOST_ADDRESS, &bind_addr_c2c);
    link_socket_to_listen_addr(socket_c2c, &bind_addr_c2c);
// config bind address socket_c2py
    authorized_broadcast(socket_c2py);
    configure_listening_addr(&bind_addr_c2py, port_broadcast);
    link_socket_to_listen_addr(socket_c2py, &bind_addr_c2py);
// config sending address socket_c2c
    authorized_broadcast(socket_c2c);
    configure_sending_addr(&broadcast_addr, port_broadcast, "NO");
    convert_address(BROADCAST_ADDRESS, &broadcast_addr);
// config sending address socket_c2py
    configure_sending_addr(&py_addr, port_python_c2py, LOCALHOST_ADDRESS);
//=============================================================
    // // PAS TOUCHE !!!
    // //---------------------------------------------------------
    // // Configuration de la taille du buffer de réception
    // int max_buf_size;
    // setsockopt(socket_c2c, SOL_SOCKET, SO_RCVBUF, &max_buf_size, sizeof(int));
    // if (setsockopt(socket_c2c, SOL_SOCKET, SO_RCVBUF, &max_buf_size, sizeof(int)) == -1) {
    //     perror("Problème de configuration de la taille du buffer de réception");
    //     close(socket_c2c);
    //     exit(EXIT_FAILURE);
    // }
    // //SO_SND définit la taille limite d'un datagram
    // //---------------------------------------------------------


    printf("En écoute d'un message python en UDP sur le port %d...\n",  port_python_c2c);
    
    // Boucle pour recevoir et traiter les messages
    while (1) {
        //================ c2c ==============================================
        listen_socket(socket_c2c, message, MAX_BUF_SIZE, &from_addr_c2c, from_len_c2c, 1);
        send_message(socket_c2c, message, &broadcast_addr, 0);
        //================ c2py ==============================================
        listen_socket(socket_c2py, message, MAX_BUF_SIZE, &from_addr_c2py, from_len_c2py, 1);
        send_message(socket_c2py, message, &py_addr, 0);    
    }

    close(socket_c2py);
    close(socket_c2c);
    return 0;
}
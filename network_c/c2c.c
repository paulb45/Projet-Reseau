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
#define LOCALHOST_ADDRESS "127.0.0.1" // addresse de reception du message de python
#define BROADCAST_ADDRESS "255.255.255.255"  // Adresse de broadcast
#define MAX_BUF_SIZE 1024 // Taille du message

int main(int argc, char *argv[]) {
    int port_python=0;
    int port_broadcast=0;
    
    struct sockaddr_in bind_addr, broadcast_addr, from_addr;
    socklen_t from_len = sizeof(from_addr);

    setup_ports(argc, argv, &port_python, &port_broadcast);
    int socket_c2c = create_udp_socket();

    configure_python_addr(&bind_addr, port_python, "NO");
    convert_address(LOCALHOST_ADDRESS, &bind_addr);

    link_socket_to_listen_addr(socket_c2c, &bind_addr);
    authorized_broadcast(socket_c2c);


    configure_broadcast_addr(&broadcast_addr, port_broadcast, "NO");
    convert_address(BROADCAST_ADDRESS, &broadcast_addr);


    // PAS TOUCHE !!!
    //-----------------------------------------------------------------------------------
    // Configuration de la taille du buffer de réception
    int max_buf_size;
    setsockopt(socket_c2c, SOL_SOCKET, SO_RCVBUF, &max_buf_size, sizeof(int));
    if (setsockopt(socket_c2c, SOL_SOCKET, SO_RCVBUF, &max_buf_size, sizeof(int)) == -1) {
        perror("Problème de configuration de la taille du buffer de réception");
        close(socket_c2c);
        exit(EXIT_FAILURE);
    }
    //SO_SND définit la taille limite d'un datagram
    //-----------------------------------------------------------------------------------

    printf("En écoute d'un message python en UDP sur le port %d...\n", port_python);

    // Boucle pour recevoir et traiter les messages
    char message[MAX_BUF_SIZE];
    while (1) {
        listen_socket(socket_c2c, message, MAX_BUF_SIZE, &from_addr, from_len, 0);
        send_message(socket_c2c, message, &broadcast_addr, 0);
    }
    close(socket_c2c);
    return 0;
}
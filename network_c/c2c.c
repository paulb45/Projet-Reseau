#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
<<<<<<< Updated upstream
#include "init_port.h"
=======

#include "network.h"
>>>>>>> Stashed changes
// =========================================================================================
//                Programme pour réceptionner un message provenant de python
//     Emmission du message en broadcast au receiver en C (autre machine théoriquement)
// =========================================================================================
#define LOCALHOST_ADDRESS "127.0.0.1" // addresse de reception du message de python
#define BROADCAST_ADDRESS "255.255.255.255"  // Adresse de broadcast
#define MAX_BUF_SIZE 100  // Taille du message

int main(int argc, char *argv[]) {
<<<<<<< Updated upstream
    // Définit les ports de réception et d'émission
    int port_python=0;
    int port_broadcast=0;
    setup_ports(argc, argv, &port_python, &port_broadcast);
    
    

    //Init du socket de réception et d'émission
    int socket_c2c;
=======
    int port_python=0;
    int port_broadcast=0;
    
>>>>>>> Stashed changes
    struct sockaddr_in bind_addr, broadcast_addr, from_addr;
    socklen_t from_len = sizeof(from_addr);

    setup_ports(argc, argv, &port_python, &port_broadcast);
    int socket_c2c = create_udp_socket();

    configure_sending_addr(&bind_addr, port_python, "NO");
    convert_address(LOCALHOST_ADDRESS, &bind_addr);

<<<<<<< Updated upstream
    // Configuration de l'adresse de connexion du socket (bind)
    memset(&bind_addr, 0, sizeof(bind_addr));  // Initialiser à 0
    bind_addr.sin_family = AF_INET;               // Protocole IPv4
    bind_addr.sin_port = htons(port_python);             // Port d'écoute python
    //bind_addr.sin_addr.s_addr = INADDR_ANY;       // Écoute sur toutes les interfaces réseau
    if (inet_pton(AF_INET, LOCALHOST_ADDRESS, &bind_addr.sin_addr) <= 0) {
        perror("Erreur lors de la conversion de l'adresse IP du socket_send");
        close(socket_c2c);
        exit(EXIT_FAILURE);
    }
=======
    link_socket_to_listen_addr(socket_c2c, &bind_addr);
    authorized_broadcast(socket_c2c);
>>>>>>> Stashed changes


    configure_sending_addr(&broadcast_addr, port_broadcast, "NO");
    convert_address(BROADCAST_ADDRESS, &broadcast_addr);

<<<<<<< Updated upstream
    // Activer l'option  SO_BROADCAST pour le socket
    int broadcast = 1;
    if(setsockopt(socket_c2c,SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast)) < 0) {
        perror("Erreur lors de la configuration de l'option SO_BROADCAST");
        close(socket_c2c);
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse de broadcast pour le socket_c2c
    memset(&broadcast_addr, 0, sizeof(broadcast_addr));
    broadcast_addr.sin_family = AF_INET;
    broadcast_addr.sin_port = htons(port_broadcast);  // Le port de diffusion
    if (inet_pton(AF_INET, BROADCAST_ADDRESS, &broadcast_addr.sin_addr) <= 0) {
        perror("Erreur lors de la conversion de l'adresse IP du socket_send");
        close(socket_c2c);
        exit(EXIT_FAILURE);
    }
=======
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream

        char message[MAX_BUF_SIZE];

        // Réception du message
        ssize_t n = recvfrom(socket_c2c, message, MAX_BUF_SIZE, 0, (struct sockaddr *)&from_addr, &from_len);
        if (n < 0) {
            perror("Erreur de réception");
            close (socket_c2c);
            exit(EXIT_FAILURE);
        }

        message[n] = '\0';

        printf("Message reçu de %s:%d\n", inet_ntoa(from_addr.sin_addr), ntohs(from_addr.sin_port));

        printf("Message: %s\n", message);

        //Envoi du message
        ssize_t bytes_sent = sendto(socket_c2c, message, strlen(message), 0,(struct sockaddr *)&broadcast_addr, sizeof(broadcast_addr));
        if (bytes_sent < 0) {
            perror("Erreur lors de l'envoi du message en broadcast");
            close(socket_c2c);
            exit(EXIT_FAILURE);
        }

        printf("Message envoyé en broadcast %s:%d\n", inet_ntoa(broadcast_addr.sin_addr), ntohs(broadcast_addr.sin_port));



=======
        listen_socket(socket_c2c, message, MAX_BUF_SIZE, &from_addr, from_len, 0);
        send_message(socket_c2c, message, &broadcast_addr, 0);
>>>>>>> Stashed changes
    }
    close(socket_c2c);
    return 0;
}
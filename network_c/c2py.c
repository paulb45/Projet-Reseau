#include <stdio.h>
#include <stdlib.h>
#include <string.h>
<<<<<<< Updated upstream
#include <arpa/inet.h>  // Pour la gestion des adresses réseau
#include <unistd.h>     // Pour la fonction close()
#include "init_port.h"
=======
#include <arpa/inet.h>
#include <unistd.h>
#include "network.h"

>>>>>>> Stashed changes
// ====================================================================================================
//     Programme pour Emmettre un message provenant de C broadcast (d'une autre machine théoriquement)
//                      Emmission du message au receiver en pyhton
// ====================================================================================================
#define DEST_IP "127.0.0.1"  
#define MAX_BUF_SIZE 50

<<<<<<< Updated upstream
int main() {
    // Définit les ports de réception et d'émission
    int port_python=0;
    int port_broadcast=0;
    setup_ports(argc, argv, &port_python, &port_broadcast);
=======
int main(int argc, char *argv[]) {
    int port_python=0;
    int port_broadcast=0;
    setup_ports(argc, argv, &port_python, &port_broadcast);

    int socket_c2py = create_udp_socket();
    struct sockaddr_in py_addr, bind_addr, from_addr;

    // Configuration de l'adresse de Python
    configure_sending_addr(&py_addr, port_python, DEST_IP);
    authorized_broadcast(socket_c2py);
    configure_listening_addr(&bind_addr, port_broadcast);
    link_socket_to_listen_addr(socket_c2py, &bind_addr);
>>>>>>> Stashed changes

    char message[MAX_BUF_SIZE];
    socklen_t from_len = sizeof(from_addr);

<<<<<<< Updated upstream
    // Création du socket UDP 
    socket_c2py = socket(AF_INET, SOCK_DGRAM, 0);
    if (socket_c2py < 0) {
        perror("Erreur de création du socket de transmission à Python");
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse de Python
    memset(&py_addr, 0, sizeof(py_addr));  // Initialiser à 0
    py_addr.sin_family = AF_INET;               // Protocole IPv4
    py_addr.sin_port = htons(port_python);             // Port de destination
    py_addr.sin_addr.s_addr = inet_addr(DEST_IP); // Adresse IP de Python

    // Autoriser la réception des broadcasts
    int broadcast = 1;
    if (setsockopt(socket_c2py, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast)) < 0) {
        perror("Erreur lors de la configuration de l'option SO_BROADCAST");
        close(socket_c2py);
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse d'écoute
    memset(&bind_addr, 0, sizeof(bind_addr));
    bind_addr.sin_family = AF_INET;
    bind_addr.sin_port = htons(port_broadcast); // Port d'écoute BROADCAST_PORT
    bind_addr.sin_addr.s_addr = INADDR_ANY;  

    // Lier le socket à l'adresse et au port spécifiés
    if (bind(socket_c2py, (struct sockaddr *)&bind_addr, sizeof(bind_addr)) < 0) {
        perror("Erreur lors de la liaison du socket de réception");
        close(socket_c2py);
        exit(EXIT_FAILURE);
    }

    printf("En attente de messages broadcast depuis %d...\n", ntohs(bind_addr.sin_port));


    while(1){
        
        // Ecouter les messages broadcast
        ssize_t len = recvfrom(socket_c2py, message, MAX_BUF_SIZE, 0, (struct sockaddr *)&from_addr, &from_len);
        if (len < 0) {
            perror("Erreur lors de la réception des données");
            close(socket_c2py);
            exit(EXIT_FAILURE);
        }
        printf("Message reçu de %s:%d\n", inet_ntoa(from_addr.sin_addr), ntohs(from_addr.sin_port));

        printf("Message: %s\n", message);

        // Envoi du message à Python
        ssize_t sent_bytes = sendto(socket_c2py, message, MAX_BUF_SIZE, 0, (struct sockaddr *)&py_addr, sizeof(py_addr));
        if (sent_bytes == -1) {
            perror("Erreur lors de l'envoi du message");
            close(socket_c2py);
            exit(EXIT_FAILURE);
        }

        printf("Message envoyé à python %s:%d\n", inet_ntoa(py_addr.sin_addr), ntohs(py_addr.sin_port));
=======
    while(1){
        listen_socket(socket_c2py, message, MAX_BUF_SIZE, &from_addr, from_len, 0);
        send_message(socket_c2py, message, &py_addr, 0);
        ssize_t sent_bytes = sendto(socket_c2py, message, strlen(message), 0, (struct sockaddr *)&py_addr, sizeof(py_addr));
>>>>>>> Stashed changes
    }

    close(socket_c2py);

    return 0;
}
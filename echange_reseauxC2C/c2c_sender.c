#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
// =========================================================================================
//                Programme pour réceptionner un message provenant de python
//     Emmission du message en broadcast au receiver en C (autre machine théoriquement)
// =========================================================================================
#define PORT 55005 //Port sur lequel Python envoie les informations
#define BROADCAST_PORT 12345  // Le port sur lequel envoyer les broadcasts
#define BROADCAST_ADDRESS "255.255.255.255"  // Adresse de broadcast
#define MAX_BUF_SIZE 50

int main() {
    //Init du socket de réception
    int entry_socket;
    struct sockaddr_in sender_addr, receptor_addr;
    socklen_t receptor_len = sizeof(receptor_addr);
    

    //Init du socket d'émission
    int socket_send;
    struct sockaddr_in broadcast_addr;

    // Création du socket UDP réception
    entry_socket = socket(AF_INET, SOCK_DGRAM, 0);
    if  (entry_socket < 0) {
        perror("Erreur de création du socket");
        exit(EXIT_FAILURE);
    }

    // Création du socket UDP émission
    socket_send = socket(AF_INET, SOCK_DGRAM, 0);
    if (socket_send < 0) {
        perror("Erreur lors de la création du socket");
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse de réception
    memset(&sender_addr, 0, sizeof(sender_addr));  // Initialiser à 0
    sender_addr.sin_family = AF_INET;               // Protocole IPv4
    sender_addr.sin_port = htons(PORT);             // Port d'écoute
    sender_addr.sin_addr.s_addr = INADDR_ANY;       // Écoute sur toutes les interfaces réseau

    // Lier le socket_entry à l'adresse et au port
    if (bind(entry_socket, (struct sockaddr *)&sender_addr, sizeof(sender_addr)) < 0) {
        perror("Erreur de bind sur le socket_entry");
        close (entry_socket);
        exit(EXIT_FAILURE);
    }

    // Activer l'option SO_BROADCAST pour le socket_send
    int broadcast = 1;
    if (setsockopt(socket_send, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast)) < 0) {
        perror("Erreur lors de la configuration de l'option SO_BROADCAST");
        close(socket_send);
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse de broadcast pour le socket_send
    memset(&broadcast_addr, 0, sizeof(broadcast_addr));
    broadcast_addr.sin_family = AF_INET;
    broadcast_addr.sin_port = htons(BROADCAST_PORT);  // Le port de diffusion
    if (inet_pton(AF_INET, BROADCAST_ADDRESS, &broadcast_addr.sin_addr) <= 0) {
        perror("Erreur lors de la conversion de l'adresse IP du socket_send");
        close(socket_send);
        exit(EXIT_FAILURE);
    }

    printf("Serveur UDP en écoute sur le port %d...\n", PORT);

    // Boucle pour recevoir et traiter les messages
    while (1) {

        char message[MAX_BUF_SIZE];

        // Réception du message
        ssize_t n = recvfrom(entry_socket, message, MAX_BUF_SIZE, 0, (struct sockaddr *)&receptor_addr, &receptor_len);
        if (n < 0) {
            perror("Erreur de réception");
            close (entry_socket);
            exit(EXIT_FAILURE);
        }

        message[n] = '\0';

        printf("Message reçu de %s:%d\n", inet_ntoa(receptor_addr.sin_addr), ntohs(receptor_addr.sin_port));

        printf("Message reçu: %s\n", message);

        //Envoi du message
        ssize_t bytes_sent = sendto(socket_send, message, strlen(message), 0,(struct sockaddr *)&broadcast_addr, sizeof(broadcast_addr));
        if (bytes_sent < 0) {
            perror("Erreur lors de l'envoi du message en broadcast");
            close(socket_send);
            exit(EXIT_FAILURE);
        }

        printf("Message envoyé en broadcast: %s\n", message);



    }

    close(entry_socket);
    close(socket_send);

    return 0;
}
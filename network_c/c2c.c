#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
// =========================================================================================
//                Programme pour réceptionner un message provenant de python
//     Emmission du message en broadcast au receiver en C (autre machine théoriquement)
// =========================================================================================
#define PORT 55006 //Port sur lequel Python envoie les informations, port d'écoute
#define LOCALHOST_ADDRESS "127.0.0.1" // addresse de reception du message de python
#define BROADCAST_PORT 50002  // Le port sur lequel envoyer les broadcasts
#define BROADCAST_ADDRESS "255.255.255.255"  // Adresse de broadcast
#define MAX_BUF_SIZE 50  // Taille du message

int main() {
    //Init du socket de réception et d'émission
    int socket_c2c;
    struct sockaddr_in bind_addr, broadcast_addr, from_addr;
    socklen_t from_len = sizeof(from_addr);


    // Création du socket UDP réception
    socket_c2c = socket(AF_INET, SOCK_DGRAM, 0);
    if  (socket_c2c < 0) {
        perror("Erreur de création du socket");
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse de connexion du socket (bind)
    memset(&bind_addr, 0, sizeof(bind_addr));  // Initialiser à 0
    bind_addr.sin_family = AF_INET;               // Protocole IPv4
    bind_addr.sin_port = htons(PORT);             // Port d'écoute python
    //bind_addr.sin_addr.s_addr = INADDR_ANY;       // Écoute sur toutes les interfaces réseau
    if (inet_pton(AF_INET, LOCALHOST_ADDRESS, &bind_addr.sin_addr) <= 0) {
        perror("Erreur lors de la conversion de l'adresse IP du socket_send");
        close(socket_c2c);
        exit(EXIT_FAILURE);
    }


    // Lier le socket_c2c à l'adresse et au port de reception du python
    if (bind(socket_c2c, (struct sockaddr *)&bind_addr, sizeof(bind_addr)) < 0) {
        perror("Erreur de bind sur le socket_entry");
        close(socket_c2c);
        exit(EXIT_FAILURE);
    }

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
    broadcast_addr.sin_port = htons(BROADCAST_PORT);  // Le port de diffusion
    if (inet_pton(AF_INET, BROADCAST_ADDRESS, &broadcast_addr.sin_addr) <= 0) {
        perror("Erreur lors de la conversion de l'adresse IP du socket_send");
        close(socket_c2c);
        exit(EXIT_FAILURE);
    }

    printf("En écoute d'un message python en UDP sur le port %d...\n", PORT);

    // Boucle pour recevoir et traiter les messages
    while (1) {

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



    }

    close(socket_c2c);
    

    return 0;
}
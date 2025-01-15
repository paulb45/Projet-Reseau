#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>  // Pour la gestion des adresses réseau
#include <unistd.h>     // Pour la fonction close()

// ====================================================================================================
//     Programme pour Emmettre un message provenant de C broadcast (d'une autre machine théoriquement)
//                      Emmission du message au receiver en pyhton
// ====================================================================================================

#define PORT 55006
#define DEST_IP "127.0.0.1"  
#define BROADCAST_PORT 12345  // Le port sur lequel écouter les broadcasts
#define MAX_BUF_SIZE 50

int main() {

    //Init du socket de transmission à Python
    int socket_topy;
    struct sockaddr_in py_addr;

    //Init du socket de réception depuis le broadcast
    int sockfd;
    struct sockaddr_in listen_addr;
    char message[MAX_BUF_SIZE];
    socklen_t listen_addr_len = sizeof(listen_addr);

    // Création du socket UDP de transmission à Python
    socket_topy = socket(AF_INET, SOCK_DGRAM, 0);
    if (socket_topy < 0) {
        perror("Erreur de création du socket de transmission à Python");
        exit(EXIT_FAILURE);
    }

    // Création du socket UDP de réception
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Erreur lors de la création du socket de réception");
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse de Python
    memset(&py_addr, 0, sizeof(py_addr));  // Initialiser à 0
    py_addr.sin_family = AF_INET;               // Protocole IPv4
    py_addr.sin_port = htons(PORT);             // Port de destination
    py_addr.sin_addr.s_addr = inet_addr(DEST_IP); // Adresse IP de Python

     // Autoriser la réception des broadcasts
    int broadcast = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast)) < 0) {
        perror("Erreur lors de la configuration de l'option SO_BROADCAST");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse du socket de réception
    memset(&listen_addr, 0, sizeof(listen_addr));
    listen_addr.sin_family = AF_INET;
    listen_addr.sin_port = htons(BROADCAST_PORT);
    listen_addr.sin_addr.s_addr = INADDR_ANY;  

    // Lier le socket à l'adresse et au port spécifiés
    if (bind(sockfd, (struct sockaddr *)&listen_addr, sizeof(listen_addr)) < 0) {
        perror("Erreur lors de la liaison du socket de réception");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("En attente de messages broadcast sur le port %d...\n", BROADCAST_PORT);


    while(1){
        
        // Ecouter les messages broadcast
        ssize_t len = recvfrom(sockfd, message, MAX_BUF_SIZE, 0, (struct sockaddr *)&listen_addr, &listen_addr_len);
        if (len < 0) {
            perror("Erreur lors de la réception des données");
            close(sockfd);
            exit(EXIT_FAILURE);
        }

        printf("Message reçu: %s\n", message);

        // Envoi du message à Python
        ssize_t sent_bytes = sendto(socket_topy, message, MAX_BUF_SIZE, 0, (struct sockaddr *)&py_addr, sizeof(py_addr));
        if (sent_bytes == -1) {
            perror("Erreur lors de l'envoi du message");
            close(socket_topy);
            exit(EXIT_FAILURE);
        }

        printf("Message envoyé : %s\n", message);
    }

    close(socket_topy);
    close(sockfd);

    return 0;
}

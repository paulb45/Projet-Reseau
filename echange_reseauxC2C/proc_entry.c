#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 55005

int main() {
    int sockfd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[256];

    // Création du socket UDP
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Erreur de création du socket");
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse du serveur
    memset(&server_addr, 0, sizeof(server_addr));  // Initialiser à 0
    server_addr.sin_family = AF_INET;               // Protocole IPv4
    server_addr.sin_port = htons(PORT);             // Port d'écoute
    server_addr.sin_addr.s_addr = INADDR_ANY;       // Écoute sur toutes les interfaces réseau

    // Lier le socket à l'adresse et au port
    if (bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Erreur de bind");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("Serveur UDP en écoute sur le port %d...\n", PORT);

    // Boucle pour recevoir et traiter les messages
    while (1) {
        // Réception du message
        ssize_t n = recvfrom(sockfd, buffer, sizeof(buffer) - 1, 0, (struct sockaddr *)&client_addr, &client_len);
        if (n < 0) {
            perror("Erreur de réception");
            close(sockfd);
            exit(EXIT_FAILURE);
        }

        buffer[n] = '\0';

        printf("Message reçu de %s:%d\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));

        printf("Message reçu: %s\n", buffer);

    }

    close(sockfd);

    return 0;
}
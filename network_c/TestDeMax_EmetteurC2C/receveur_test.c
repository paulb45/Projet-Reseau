#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define BROADCAST_PORT 12345  // Le port sur lequel écouter les broadcasts
#define MAX_BUF_SIZE 50

int main() {
    int sockfd;
    struct sockaddr_in addr;
    char buffer[MAX_BUF_SIZE];
    socklen_t addr_len = sizeof(addr);

    // Création du socket UDP
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Erreur lors de la création du socket");
        exit(EXIT_FAILURE);
    }

    // Autoriser la réception des broadcasts
    int broadcast = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast)) < 0) {
        perror("Erreur lors de la configuration de l'option SO_BROADCAST");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse du socket
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(BROADCAST_PORT);
    addr.sin_addr.s_addr = INADDR_ANY;  // Accepter les messages sur toutes les interfaces réseau

    // Lier le socket à l'adresse et au port spécifiés
    if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("Erreur lors de la liaison du socket");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("En attente de messages broadcast sur le port %d...\n", BROADCAST_PORT);

    // Écouter les messages broadcast
    while (1) {
        ssize_t len = recvfrom(sockfd, buffer, MAX_BUF_SIZE, 0, (struct sockaddr *)&addr, &addr_len);
        if (len < 0) {
            perror("Erreur lors de la réception des données");
            close(sockfd);
            exit(EXIT_FAILURE);
        }

        buffer[len] = '\0';  // Terminer la chaîne
        printf("Message reçu: %s\n", buffer);
    }

    close(sockfd);
    return 0;
}

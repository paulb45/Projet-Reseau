#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define BROADCAST_PORT 12345  // Le port sur lequel envoyer les broadcasts
#define BROADCAST_ADDRESS "255.255.255.255"  // Adresse de broadcast
#define MAX_BUF_SIZE 1024

int main(int ac, char **av) {
    int sockfd;
    char* message;
    struct sockaddr_in broadcast_addr;
    if(ac != 2){
        perror("Erreur lors du renseignement du message");
    }
    
    // Création du socket UDP
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Erreur lors de la création du socket");
        exit(EXIT_FAILURE);
    }

    // Activer l'option SO_BROADCAST pour permettre l'envoi en broadcast
    int broadcast = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast)) < 0) {
        perror("Erreur lors de la configuration de l'option SO_BROADCAST");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse de broadcast
    memset(&broadcast_addr, 0, sizeof(broadcast_addr));
    broadcast_addr.sin_family = AF_INET;
    broadcast_addr.sin_port = htons(BROADCAST_PORT);  // Le port de diffusion
    if (inet_pton(AF_INET, BROADCAST_ADDRESS, &broadcast_addr.sin_addr) <= 0) {
        perror("Erreur lors de la conversion de l'adresse IP");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Envoyer le message en broadcast
    message = av[1];
    ssize_t bytes_sent = sendto(sockfd, message, strlen(message), 0,(struct sockaddr *)&broadcast_addr, sizeof(broadcast_addr));
    if (bytes_sent < 0) {
        perror("Erreur lors de l'envoi du message");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("Message envoyé en broadcast: %s\n", message);

    // Fermer le socket
    close(sockfd);

    return 0;
}

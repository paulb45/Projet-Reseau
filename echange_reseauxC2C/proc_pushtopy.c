#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>  // Pour la gestion des adresses réseau
#include <unistd.h>     // Pour la fonction close()

#define PORT 55005
#define DEST_IP "127.0.0.1"  

int main() {
    int sockfd;
    struct sockaddr_in server_addr;
    char buffer[256];  // Buffer pour recevoir le message

    // Création du socket UDP
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Erreur de création du socket");
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse du serveur
    memset(&server_addr, 0, sizeof(server_addr));  // Initialiser à 0
    server_addr.sin_family = AF_INET;               // Protocole IPv4
    server_addr.sin_port = htons(PORT);             // Port de destination
    server_addr.sin_addr.s_addr = inet_addr(DEST_IP); // Adresse IP du serveur

    while(1){
        printf("Entrez le message à envoyer : ");
        if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
            perror("Erreur de lecture depuis stdin");
            close(sockfd);
            exit(EXIT_FAILURE);
        }
        
        buffer[strcspn(buffer, "\n")] = '\0';

        // Envoi du message à Python
        ssize_t sent_bytes = sendto(sockfd, buffer, strlen(buffer), 0, (struct sockaddr *)&server_addr, sizeof(server_addr));
        if (sent_bytes == -1) {
            perror("Erreur lors de l'envoi du message");
            close(sockfd);
            exit(EXIT_FAILURE);
        }

        printf("Message envoyé : %s\n", buffer);
    }

    close(sockfd);

    return 0;
}

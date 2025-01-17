#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>  // Pour la gestion des adresses réseau
#include <unistd.h>     // Pour la fonction close()

// ====================================================================================================
//     Programme pour Emmettre un message provenant de C broadcast (d'une autre machine théoriquement)
//                      Emmission du message au receiver en pyhton
// ====================================================================================================

#define PORT 55005 // Port sur lequel python écoute
#define DEST_IP "127.0.0.1"  
#define BROADCAST_PORT 50002  // Le port sur lequel écouter les broadcasts
#define MAX_BUF_SIZE 50

int main() {

    //Init du socket 
    int socket_c2py;
    struct sockaddr_in py_addr,bind_addr,from_addr;
    char message[MAX_BUF_SIZE];
    socklen_t from_len = sizeof(from_addr);

    // Création du socket UDP 
    socket_c2py = socket(AF_INET, SOCK_DGRAM, 0);
    if (socket_c2py < 0) {
        perror("Erreur de création du socket de transmission à Python");
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse de Python
    memset(&py_addr, 0, sizeof(py_addr));  // Initialiser à 0
    py_addr.sin_family = AF_INET;               // Protocole IPv4
    py_addr.sin_port = htons(PORT);             // Port de destination
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
    bind_addr.sin_port = htons(BROADCAST_PORT); // Port d'écoute BROADCAST_PORT
    bind_addr.sin_addr.s_addr = INADDR_ANY;  

    // Lier le socket à l'adresse et au port spécifiés
    if (bind(socket_c2py, (struct sockaddr *)&bind_addr, sizeof(bind_addr)) < 0) {
        perror("Erreur lors de la liaison du socket de réception");
        close(socket_c2py);
        exit(EXIT_FAILURE);
    }

    //printf("En attente de messages broadcast depuis %d...\n", ntohs(bind_addr.sin_port));


    while(1){
        
        // Ecouter les messages broadcast
        ssize_t n = recvfrom(socket_c2py, message, MAX_BUF_SIZE, 0, (struct sockaddr *)&from_addr, &from_len);
        if (n < 0) {
            perror("Erreur lors de la réception des données");
            close(socket_c2py);
            exit(EXIT_FAILURE);
        }
        //printf("Message reçu de %s:%d\n", inet_ntoa(from_addr.sin_addr), ntohs(from_addr.sin_port));

        //printf("Message: %s\n", message);

        // Envoi du message à Python
        ssize_t sent_bytes = sendto(socket_c2py, message, strlen(message), 0, (struct sockaddr *)&py_addr, sizeof(py_addr));
        if (sent_bytes == -1) {
            perror("Erreur lors de l'envoi du message");
            close(socket_c2py);
            exit(EXIT_FAILURE);
        }

        //printf("Message envoyé à python %s:%d\n", inet_ntoa(py_addr.sin_addr), ntohs(py_addr.sin_port));
    }

    close(socket_c2py);

    return 0;
}

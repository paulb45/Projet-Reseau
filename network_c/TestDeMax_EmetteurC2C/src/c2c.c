#include "../include/c2c.h"

// =========================================================================================
//                Programme pour réceptionner un message provenant de python
//     Emmission du message en broadcast au receiver en C (autre machine théoriquement)
// =========================================================================================


// Initialise et renvoie une socket UDP en IPv4
int init_sck_c2c(){
    int sckfd = socket(AF_INET, SOCK_DGRAM, 0);
    if  (sckfd < 0) {
        perror("Erreur de création du socket");
        close(sckfd);
        exit(EXIT_FAILURE);
    }
    return sckfd;
}

// Configuration de la connexion du socket (bind)
void init_bind_addr(int sckfd, struct sockaddr_in *bind_addr){
    memset(bind_addr, 0, sizeof(*bind_addr));  // Initialiser à 0
    bind_addr->sin_family = AF_INET;               // Protocole IPv4
    bind_addr->sin_port = htons(PORT);             // Port d'écoute python
    //bind_addr.sin_addr.s_addr = INADDR_ANY;       // Écoute sur toutes les interfaces réseau
    if (inet_pton(AF_INET, LOCALHOST_ADDRESS, &(bind_addr->sin_addr)) <= 0) {
        perror("Erreur lors de la conversion de l'adresse IP du socket_send");
        close(sckfd);
        exit(EXIT_FAILURE);
    }
    // Lier le socket_c2c à l'adresse et au port de reception du python

    if (bind(sckfd, (struct sockaddr *)bind_addr, sizeof(*bind_addr)) < 0) {
        perror("Erreur de bind sur le socket_entry");
        exit(EXIT_FAILURE);
    }
}

// Activer l'option  SO_BROADCAST pour le socket
void init_brd_sck(int sckfd){
    int broadcast = 1;
    if(setsockopt(sckfd,SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast)) < 0) {
        perror("Erreur lors de la configuration de l'option SO_BROADCAST");
        close(sckfd);
        exit(EXIT_FAILURE);
    }

}
// Configuration de l'adresse de broadcast pour le socket
void init_brd_addr(int sckfd, struct sockaddr_in *brd_addr){
    memset(brd_addr, 0, sizeof(*brd_addr));
    brd_addr->sin_family = AF_INET;
    brd_addr->sin_port = htons(BROADCAST_PORT);  // Le port de diffusion
    if (inet_pton(AF_INET, BROADCAST_ADDRESS, &(brd_addr->sin_addr)) <= 0) {
        perror("Erreur lors de la conversion de l'adresse IP");
        close(sckfd);
        exit(EXIT_FAILURE);
    }
}
// Configuration de la taille du buffer de réception
void init_buf_size(int sckfd){
    int max_buf_size;
    if (setsockopt(sckfd, SOL_SOCKET, SO_RCVBUF, &max_buf_size, sizeof(int)) == -1) {
        perror("Problème de configuration de la taille du buffer de réception");
        close(sckfd);
        exit(EXIT_FAILURE);
    }
    //SO_SND définit la taille limite d'un datagram
}

// Réception du message
char* msg_receive(int sckfd, struct sockaddr_in *from_addr, socklen_t from_len){
    char message[MAX_BUF_SIZE];
    ssize_t n = recvfrom(sckfd, message, MAX_BUF_SIZE, 0, (struct sockaddr *)from_addr, &from_len);
    if (n < 0) {
        perror("Erreur de réception");
        close (sckfd);
        exit(EXIT_FAILURE);
    }
    return message;
}
//Envoi du message
void send_msg(int sckfd, char* message, struct sockaddr_in *brd_addr){
    ssize_t bytes_sent = sendto(sckfd, message, strlen(message), 0,(struct sockaddr *)brd_addr, sizeof(*brd_addr));
    if (bytes_sent < 0) {
        perror("Erreur lors de l'envoi du message en broadcast");
        close(sckfd);
        exit(EXIT_FAILURE);
    }
}

#ifndef C2C_H_INCLUDED
#define C2C_H_INCLUDED

#define PORT 55006 //Port sur lequel Python envoie les informations, port d'écoute
#define LOCALHOST_ADDRESS "127.0.0.1" // addresse de reception du message de python
#define BROADCAST_PORT 50002  // Le port sur lequel envoyer les broadcasts
#define BROADCAST_ADDRESS "255.255.255.255"  // Adresse de broadcast
#define MAX_BUF_SIZE 100  // Taille du message

// Initialise et renvoie une socket UDP en IPv4
int init_sck_c2c();

// Configuration de la connexion du socket (bind)
void init_bind_addr(int sckfd, struct sockaddr_in *bind_addr);

// Activer l'option  SO_BROADCAST pour le socket
void init_brd_sck(int sckfd);

// Configuration de l'adresse de broadcast pour le socket
void init_brd_addr(int sckfd, struct sockaddr_in *brd_addr);

// Configuration de la taille du buffer de réception
void init_buf_size(int sckfd);

// Réception du message
char* msg_receive(int sckfd, struct sockaddr_in *from_addr, socklen_t from_len);

//Envoi du message
void send_msg(int sckfd, char* message, struct sockaddr_in *brd_addr);

#endif 
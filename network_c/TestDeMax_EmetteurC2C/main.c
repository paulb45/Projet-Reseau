#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>  // Pour la gestion des adresses réseau
#include <unistd.h>     // Pour la fonction close()

#include "c2c.h"
#include "c2py.h"

int main()
{
//============= INIT DU SOCKET_C2C ===============
    //Init du socket de réception et d'émission c2c
    int socket_c2c;
    struct sockaddr_in bind_addr, broadcast_addr, from_addr;
    socklen_t from_len = sizeof(from_addr);

    // Création du socket UDP réception c2c
    socket_c2c = init_sck_c2c();
    // Configuration de la connexion du socket (bind)
    init_bind_addr(socket_c2c, &bind_addr);
    // Activer l'option  SO_BROADCAST pour le socket
    init_brd_sck(socket_c2c);
    // Configuration de l'adresse de broadcast pour le socket
    init_brd_addr(socket_c2c, &broadcast_addr);
    // Configuration de la taille du buffer de réception
    init_buf_size(socket_c2c);
//================================================

    while(1){
        // Réception du message (c2c)
        printf("En écoute d'un message python en UDP sur le port %d...\n", PORT);
        char message[MAX_BUF_SIZE] = msg_receive(socket_c2c, &from_addr, from_len);
        //Envoi du message (c2c)
        send_msg(socket_c2c, message, &broadcast_addr);
        printf("(c2c) Message envoyé en Broadcast !");
    }






    close(socket_c2c);
    return 0;
}
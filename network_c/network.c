#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include "network.h"

void setup_ports(int argc, char *argv[], int *port_rcv_py, int *port_send_broadcast, int *port_send_py, int *port_rcv_boadcast){
    if (argc == 5) {
        *port_rcv_py = atoi(argv[1]);
        *port_send_broadcast = atoi(argv[2]);
        *port_send_py = atoi(argv[3]);
        *port_rcv_boadcast = atoi(argv[4]);

    }
    else{
        *port_rcv_py = 50000;
        *port_send_broadcast = 60000;
        *port_send_py = 55005;
        *port_rcv_boadcast = 50001;
    }
}

int create_udp_socket(){
    int so = socket(AF_INET, SOCK_DGRAM, 0);
    if (so < 0) {
        return -1;
        perror("Erreur de création du socket de transmission à Python");
        exit(EXIT_FAILURE);
    }
    return so;
}
void test_print(){
    printf("Test\n");
}

void configure_python_addr(struct sockaddr_in* addr, int port, const char* send_ip){
    memset(addr, 0, sizeof(*addr));
    addr->sin_family = AF_INET;
    addr->sin_port = htons(port);
    if(strcmp(send_ip, "NO") == 0){
        return;
    }
    addr->sin_addr.s_addr = inet_addr(send_ip);
}

void authorized_broadcast(int socket){
    int broadcast = 1;
    if (setsockopt(socket, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast)) < 0) {
        perror("Erreur lors de la configuration de l'option SO_BROADCAST");
        close(socket);
        exit(EXIT_FAILURE);
    }
}

void configure_broadcast_addr(struct sockaddr_in* addr, int port, char *send_or_recv){
    memset(addr, 0, sizeof(*addr));
    addr->sin_family = AF_INET;
    addr->sin_port = htons(port);
    if (strcmp(send_or_recv,"SEND")== 0){
        addr->sin_addr.s_addr = INADDR_BROADCAST;
    }
    else{
        addr->sin_addr.s_addr = INADDR_ANY;

    }
}

void link_socket_to_listen_addr(int socket, struct sockaddr_in* addr){
    if (bind(socket, (struct sockaddr *)addr, sizeof(*addr)) < 0) {
        perror("Erreur lors de la liaison du socket de réception");
        close(socket);
        exit(EXIT_FAILURE);
    }
}

void convert_address(char* ip, struct sockaddr_in* addr){
    if (inet_pton(AF_INET, ip, &addr->sin_addr) <= 0) {
        perror("Erreur lors de la conversion de l'adresse IP");
        exit(EXIT_FAILURE);
    }

    
}

void listen_socket(int socket, char* message, int max_size, struct sockaddr_in* from_addr, socklen_t from_len, int debug){
    ssize_t n = recvfrom(socket, message, max_size, 0, (struct sockaddr *)from_addr, &from_len);
    if (n < 0) {
        perror("Erreur lors de la réception des données");
        close(socket);
        exit(EXIT_FAILURE);
    }
    if (debug){
        printf("Message reçu de %s:%d\n", inet_ntoa(from_addr->sin_addr), ntohs(from_addr->sin_port));
        // printf("Message: %s\n", message);
    }
}

void send_message(int socket, char* message, struct sockaddr_in* addr, int debug){
    ssize_t sent_bytes = sendto(socket, message, strlen(message), 0, (struct sockaddr *)addr, sizeof(*addr));
    if (sent_bytes == -1) {
        perror("Erreur lors de l'envoi du message");
        close(socket);
        exit(EXIT_FAILURE);
    }
    if(debug){
        printf("Message envoyé %s:%d\n", inet_ntoa(addr->sin_addr), ntohs(addr->sin_port));
    }
}

void setup_udp_buffer(int socket){
    int max_buf_size = 4*16 + 54*8 + 500 + 10000; // Entete UDP + Max protocole + marge
    setsockopt(socket, SOL_SOCKET, SO_RCVBUF, &max_buf_size, sizeof(int));
    if (setsockopt(socket, SOL_SOCKET, SO_RCVBUF, &max_buf_size, sizeof(int)) == -1) {
        perror("Problème de configuration de la taille du buffer de réception");
        close(socket);
        exit(EXIT_FAILURE);
    }
    setsockopt(socket, SOL_SOCKET, SO_SNDBUF, &max_buf_size, sizeof(int));
    if (setsockopt(socket, SOL_SOCKET, SO_RCVBUF, &max_buf_size, sizeof(int)) == -1) {
        perror("Problème de configuration de la taille du buffer d'envoi");
        close(socket);
        exit(EXIT_FAILURE);
    }
}
#ifndef NETWORK_H
#define NETWORK_H


#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <sys/socket.h>

#define LOCALHOST_ADDRESS "127.0.0.1" // addresse de reception du message de python
#define BROADCAST_ADDRESS "255.255.255.255"  // Adresse de broadcast
#define MAX_BUF_SIZE 1024 // Taille du message

void setup_ports(int argc, char *argv[], int *port_python_c2c, int *port_broadcast, int *port_python_c2py);

int create_udp_socket();

void configure_sending_addr(struct sockaddr_in* addr, int port, const char* ip);

void authorized_broadcast(int socket);
void configure_listening_addr(struct sockaddr_in* addr, int port);

void link_socket_to_listen_addr(int socket, struct sockaddr_in* addr);

void convert_address(char* ip, struct sockaddr_in* addr);

void listen_socket(int socket, char* message, int max_size, struct sockaddr_in* from_addr, socklen_t from_len, int debug);

void send_message(int socket, char* message, struct sockaddr_in* addr, int debug);

#endif
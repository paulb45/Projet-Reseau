#ifndef NETWORK_H
#define NETWORK_H


#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <sys/socket.h>


void setup_ports(int argc, char *argv[], int *port_python, int *port_broadcast);

int create_udp_socket();

void configure_sending_addr(struct sockaddr_in* addr, int port, const char* ip);

void authorized_broadcast(int socket);
void configure_listening_addr(struct sockaddr_in* addr, int port);

void link_socket_to_listen_addr(int socket, struct sockaddr_in* addr);

void convert_address(char* ip, struct sockaddr_in* addr);

void listen_socket(int socket, char* message, int max_size, struct sockaddr_in* from_addr, socklen_t from_len, int debug);

void send_message(int socket, char* message, struct sockaddr_in* addr, int debug);

#endif
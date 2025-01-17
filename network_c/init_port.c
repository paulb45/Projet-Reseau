#include <stdlib.h>
void setup_ports(int argc, char *argv[], int *port_python, int *port_broadcast){
    if (argc == 3) {
        *port_python = atoi(argv[1]);
        *port_broadcast = atoi(argv[2]);
    }
    else{
        *port_python = 50000;
        *port_broadcast = 60000;
    }
}

int main(){return 0;}
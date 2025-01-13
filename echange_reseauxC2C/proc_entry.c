#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void traiter_message(const char *message) {
    int x_source, y_source, x_dest, y_dest;
    
    // Extraire les coordonnées du message
    if(sscanf(message, "DEPLACE|%d,%d|%d,%d", &x_source, &y_source, &x_dest, &y_dest)){
        printf("Déplacement demandé: Source(%d, %d) -> Destination(%d, %d)\n", x_source, y_source, x_dest, y_dest);
    } else {
        fprintf(stderr, "Erreur: format du message invalide.\n");
    }

}

int main() {
    char buffer[256];

    // Lire les messages
    while (fgets(buffer, sizeof(buffer), stdin) != NULL) {
        buffer[strcspn(buffer, "\n")] = '\0';

        printf("Message reçu: %s\n", buffer);

        traiter_message(buffer);
    }

    return 0;
}
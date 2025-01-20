CC = gcc
CFLAGS = -Wall -Wextra -g

# Noms des programmes
EXEC1 = c2c
EXEC2 = c2py
INCL = init_port

<<<<<<< Updated upstream
# Compilation des programmes
$(INCL): init_port.c
	$(CC) $(CFLAGS) -o $(INCL) init_port.c

$(EXEC1): c2c.c
	$(CC) $(CFLAGS) -o $(EXEC1) c2c.c
=======
# Cible par défaut : compiler les deux programmes
all: $(EXEC1) $(EXEC2)
>>>>>>> Stashed changes

# Compilation des programmes
$(EXEC1): c2c.c network.c
	$(CC) $(CFLAGS) -o $(EXEC1) c2c.c network.c

$(EXEC2): c2py.c network.c
	$(CC) $(CFLAGS) -o $(EXEC2) c2py.c network.c

# Kill des processus
kill_processes:
	@pgrep -fl $(EXEC1) | grep -v "sh" | awk '{print $$1}' | xargs -r kill || echo "No process found for $(EXEC1)"
	@pgrep -fl $(EXEC2) | grep -v "sh" | awk '{print $$1}' | xargs -r kill || echo "No process found for $(EXEC2)"
	@echo "\nProcessus tués avec succès\n"

# Exécution des programmes
run: $(EXEC1) $(EXEC2) kill_processes
	@echo "\nExécuter les programmes en arrière-plan"
	./$(EXEC1) & 
	./$(EXEC2) &
	wait

# Nettoyage des fichiers compilés
clean: kill_processes
	rm -f $(EXEC1) $(EXEC2) network



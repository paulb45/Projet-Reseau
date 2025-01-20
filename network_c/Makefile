CC = gcc
CFLAGS = -Wall -Wextra -g

# Noms des programmes
EXEC1 = main_network

# Compilation des programmes
$(EXEC1): main_network.c
	$(CC) $(CFLAGS) -o $(EXEC1) main_network.c network.c

# Kill des processus
kill_processes:
	@pgrep -fl $(EXEC1) | grep -v "sh" | awk '{print $$1}' | xargs -r kill || echo "No process found for $(EXEC1)"
	@echo "\nProcessus tués avec succès\n"

# Exécution des programmes
run: $(EXEC1) kill_processes
	@echo "\nExécuter les programmes en arrière-plan"
	./$(EXEC1) &
	wait

# Nettoyage des fichiers compilés
clean: kill_processes
	rm -f $(EXEC1) network

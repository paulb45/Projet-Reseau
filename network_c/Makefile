CC = gcc
CFLAGS = -Wall -Wextra -g

# Nom des programmes
EXEC1 = c2c
EXEC2 = c2py

# Compilation des programmes
$(EXEC1): c2c.c
	$(CC) $(CFLAGS) -o $(EXEC1) c2c.c

$(EXEC2): c2py.c
	$(CC) $(CFLAGS) -o $(EXEC2) c2py.c

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
	rm -f $(EXEC1) $(EXEC2)



#!/bin/bash
# Définit le répertoire du script
script_dir=$(dirname $0)

bash -c "
source $script_dir/venv/bin/activate;
python3 $script_dir/main.py 10000 10001 &
wait" &

# Start dans une deuxième console
bash -c "
source $script_dir/venv/bin/activate;
python3 $script_dir/main.py 10001 10000 &
wait" &

# Attend la fin des deux processus
wait

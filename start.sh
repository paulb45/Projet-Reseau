#!/bin/bash
# Définit le répertoire du script
script_dir=$(dirname $0)

bash $script_dir/network_c/kill_process.sh
bash -c "make -C $script_dir/network_c"

# Start dans une première console
bash -c "
source $script_dir/venv/bin/activate;
./$script_dir/network_c/main_network 55001 30001 55005 30002 &
python3 $script_dir/main.py 55005 55001 &
wait" &

# Start dans une deuxième console
bash -c "
source $script_dir/venv/bin/activate;
./$script_dir/network_c/main_network 55002 30002 55006 30001 &
python3 $script_dir/main.py 55006 55002 &
wait" &

# Attend la fin des deux processus
wait

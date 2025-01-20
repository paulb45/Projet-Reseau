#!/bin/bash
# Définit le répertoire du script
script_dir=$(dirname $0)

bash $script_dir/network_c/kill_process.sh
bash -c "make -C $script_dir/network_c"

# Start dans une première console
bash -c "
source $script_dir/venv/bin/activate;
./$script_dir/network_c/c2c 30000 30001 &
./$script_dir/network_c/c2py 30005 30004 &
python3 $script_dir/main.py 30005 30000 &
wait" &

# Start dans une deuxième console
bash -c "
source $script_dir/venv/bin/activate;
./$script_dir/network_c/c2c 30003 30004 &
./$script_dir/network_c/c2py 30002 30001 &
python3 $script_dir/main.py 30002 30003 &
wait" &

# Attend la fin des deux processus
wait
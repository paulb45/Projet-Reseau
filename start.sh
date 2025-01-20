#!/bin/bash
<<<<<<< Updated upstream
script_dir=$(dirname $0)
cd network_c; make; cd ..

# Start in a first console
bash -c "
./network_c/c2c 30001 40000;
./network_c/c2py 20000 40001;
python3 network/listener.py 20001;
python3 network/pytoc_sender.py 30000;
python3 main.py" &

# Start in a second console
bash -c "
./network_c/c2c 3001 4000;
./network_c/c2py 2000 4001;
python3 network/listener.py 2001;
python3 network/pytoc_sender.py 3000;
python3 main.py" &

=======
# Définit le répertoire du script
script_dir=$(dirname $0)

bash $script_dir/network_c/kill_process.sh
bash -c "make -C $script_dir/network_c"

# Start dans une première console
bash -c "
source $script_dir/venv/bin/activate;
./$script_dir/network_c/c2c 30001 40000 &
./$script_dir/network_c/c2py 20000 40001 &
python3 $script_dir/network/listener.py 20001 &
python3 $script_dir/network/pytoc_sender.py 30000 &
python3 $script_dir/main.py &
wait" &

# Start dans une deuxième console
bash -c "
source $script_dir/venv/bin/activate;
./$script_dir/network_c/c2c 3001 4000 &
./$script_dir/network_c/c2py 2000 4001 &
python3 $script_dir/network/listener.py 2001 &
python3 $script_dir/network/pytoc_sender.py 3000 &
python3 $script_dir/main.py &
wait" &

# Attend la fin des deux processus
>>>>>>> Stashed changes
wait
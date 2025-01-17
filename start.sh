#!/bin/bash
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

wait
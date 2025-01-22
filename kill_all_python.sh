#!/bin/bash

#Petit script pour tuer tout les process python3, parce que avec les script start.sh
# et start_py.sh ils se retrouve en arrière plan et sont impossible à tuer si ils freeze

for pid in $(pgrep -f python3); do kill -9 $pid; done

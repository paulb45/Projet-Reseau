import numpy as np

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

"""
    Implémente la gestion des changements de coordonnées
"""

transfer_cart_to_iso = np.array([
        [0.5, -0.5],
        [0.25, 0.25]
    ]) * tile_size

transfer_iso_to_cart = np.linalg.inv(transfer_cart_to_iso)

def cart_to_iso(pos: tuple) -> list:
    return (transfer_cart_to_iso @ pos) + (Config.interface_x_offset, Config.interface_y_offset)

def iso_to_cart(pos: tuple) -> list:
    return transfer_iso_to_cart @ (pos - (Config.interface_x_offset, Config.interface_y_offset))

def iso_to_print(pos: tuple) -> tuple:
    return pos + (Config.height_map*tile_size/2, 0)
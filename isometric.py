import numpy as np

class Isometric():
    transfer_cart_to_iso = np.array([
            [0.5, -0.5],
            [0.25, 0.25]
        ])
    
    transfer_iso_to_cart = np.linalg.inv(transfer_cart_to_iso)

    @staticmethod
    def cart_to_iso(pos: tuple) -> list:
        return Isometric.transfer_cart_to_iso @ pos
    
    @staticmethod
    def iso_to_cart(pos: tuple) -> list:
        return Isometric.transfer_iso_to_cart @ pos

if __name__ == '__main__':
    # !!! En faisant la convertion on perd une très légère précision !!!
    assert all(  np.allclose([i,j], Isometric.cart_to_iso(Isometric.iso_to_cart((i,j)))) for i, j in np.random.rand(100,2) )
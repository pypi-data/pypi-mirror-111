import numpy as np
import copy

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

class CANBase():
    def __init__(self, Pbits = None, liste_umin_umax = None, NXe = None, test_ech = None):
        self.Pbits = Pbits
        self.liste_umin_umax = liste_umin_umax
        self.NXe = NXe
        self.test_ech = test_ech

if __name__ == "__main__":
    pass

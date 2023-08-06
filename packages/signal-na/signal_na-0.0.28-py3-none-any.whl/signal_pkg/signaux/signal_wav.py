#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:43:58 2019

@author: nicolas
"""

import os, sys
import scipy.io.wavfile as wave

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from base.axe_x_base import AxeXBase
from signaux.signal_complet import SignalComplet
import base.constantes_base as cst
from plot.plot_base import tracer
__all__ = ["SignalWav"]

class SignalWav(SignalComplet):
    def __init__(self, nom_fichier_wav, liste_umin_umax = cst.liste_umin_umax, nom = ""):

        Pbits = cst.Pbits
        
        Fe_originale, data = wave.read(nom_fichier_wav)
        Xe_original = 1/Fe_originale
        N = len(data)

        axe_x_base_original = AxeXBase([0, Xe_original], Xe_original)        
        Xe = axe_x_base_original.lire_Xe()

        SignalComplet.__init__(self, AxeXBase([0, N*Xe], Xe), data, nom)
        nom = self.lire_nom()
        can_base = self._Signal4TNS__lire_can_base()
        can_base.Pbits = Pbits
        can_base.liste_umin_umax = liste_umin_umax

        self._Signal1Base__vecteur_y = self._Signal4TNS__convertir_vecteur_numerique_vers_analogique()

if __name__ == "__main__":
    s1 = SignalWav('/Users/nicolas/tmp/A3.wav', [-10, 10])
    
    can_base = s1._Signal4TNS__lire_can_base()
    print(can_base.Pbits)
    print(can_base.liste_umin_umax)
    # s1.enregistrer_wav('/Users/nicolas/tmp/A3bis.wav')
    s2 = s1.quantifier(10)
    tracer(s1, s2)

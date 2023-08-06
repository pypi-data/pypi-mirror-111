#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:43:58 2019

@author: nicolas
"""
import time

import os, sys
import numpy as np
import matplotlib.pyplot as plt


sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from base.axe_x_base import AxeXBase
from signaux.signal_7_filtre import Signal7Filtre
from base.filtrage_base import calculer_sortie_filtre
from plot.plot_base import tracer
 
__all__ = ["SignalSysam"]



class Signal8Tronque(Signal7Filtre):
    def tronquer(self, liste_xmin_xmax):

        axe_x_base_initial = self._PlotBase__lire_axe_x_base()
        axe_x_base_final = AxeXBase(liste_xmin_xmax, axe_x_base_initial.lire_Xe())
        assert axe_x_base_final.iemin >= axe_x_base_initial.iemin, "tronquer: on ne peut pas ajouter des valeurs inconnues"
        assert axe_x_base_final.iemax <= axe_x_base_initial.iemax, "tronquer: on ne peut pas ajouter des valeurs inconnues"
        
        sortie = self.copier()

        sortie._PlotBase__axe_x_base = axe_x_base_final

        vecteur_x_final = sortie.lire_vecteur_x()
        vecteur_ia_final = axe_x_base_initial.convertir_x_vers_ia(vecteur_x_final)
        vecteur_i_final = axe_x_base_initial.convertir_ia_vers_i(vecteur_ia_final)
        vecteur_y = self.lire_vecteur_y()[vecteur_i_final]
        sortie._Signal1Base__vecteur_y = vecteur_y
        
        return sortie

if __name__ == "__main__":
    bdt = AxeXBase([0, 1], 1e-6)
    vt = bdt.lire_vecteur_x()
    ve = np.sin(2*np.pi*1e2*vt)
    e = Signal8Tronque(bdt, ve)
    s = e.tronquer([-1,1])

    tracer(e, s, superposition = False)
    
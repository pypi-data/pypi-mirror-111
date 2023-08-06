# -*- coding: utf-8 -*-
r"""
Utilities for lattice operations
"""
import numpy as np


def theta(r: np.ndarray, c: float, w: float) -> np.ndarray:
    r"""
    Theta function for example needed to create skyrmion
    """
    comp1 = np.arcsin(np.tanh((-r - c) * 2 / w))
    comp2 = np.arcsin(np.tanh((-r + c) * 2 / w))
    return np.pi + comp1 + comp2


def phi(p: np.ndarray, vorticity: float, helicity: float) -> np.ndarray:
    r"""
    Theta function for example needed to create skyrmion
    """
    return vorticity * p + helicity

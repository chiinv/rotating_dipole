"""Shared physics routines for rotating magnetic dipole
---------------------------------------------------------
SI units; the dipole rotates in the xy‑plane with angular frequency ω=1 rad/s
(only the phase matters for shape → hard‑code ω=1).
"""
import numpy as np

MU0 = 4 * np.pi * 1e-7                     # vacuum permeability [H m⁻¹]
ANGLES_DEG = np.arange(0, 361, 10)         # 0° … 360° (10° step)
ANGLES_RAD = np.deg2rad(ANGLES_DEG)


def b_field(point: tuple[float, float, float], ang: float) -> tuple[float, float, float]:
    """Return (Bx, By, Bz) at *point* when dipole phase is *ang* [rad]."""
    x, y, z = point
    r2 = x * x + y * y + z * z or 1e-30      # avoid div/0 at origin
    px, py = np.cos(ang), np.sin(ang)         # rotating dipole moment (pz=0)
    pr = px * x + py * y
    coeff = MU0 / (4 * np.pi) / r2 ** 2.5     # 1 / r^5
    bx = coeff * (3 * pr * x - r2 * px)
    by = coeff * (3 * pr * y - r2 * py)
    bz = coeff * (3 * pr * z)
    return bx, by, bz


def compute_series(point: tuple[float, float, float]):
    """Return numpy arrays (Bx, By, Bz) for all sample angles."""
    b = np.array([b_field(point, a) for a in ANGLES_RAD])
    return b[:, 0], b[:, 1], b[:, 2]
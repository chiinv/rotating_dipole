import numpy as np
MU0 = 4 * np.pi * 1e-7
ANGLES_DEG = np.arange(0, 361, 10)
ANGLES_RAD = np.deg2rad(ANGLES_DEG)

def b_field(point, ang):
    x, y, z = point
    r2 = x*x + y*y + z*z or 1e-30
    px, py = np.cos(ang), np.sin(ang)
    pr = px*x + py*y
    coeff = MU0/(4*np.pi)/r2**2.5
    bx = coeff*(3*pr*x - r2*px)
    by = coeff*(3*pr*y - r2*py)
    bz = coeff*(3*pr*z)
    return bx, by, bz

def compute_series(point):
    out = np.array([b_field(point, a) for a in ANGLES_RAD])
    return out[:,0], out[:,1], out[:,2]
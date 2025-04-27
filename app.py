import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from dipole import compute_series, ANGLES_DEG

st.set_page_config(layout="wide")

# --- Sidebar sliders (range -5..5 step 0.1) ---
x = st.sidebar.slider("x [m]",  -5.0, 5.0, 0.0, 0.1)
y = st.sidebar.slider("y [m]",  -5.0, 5.0, 0.0, 0.1)
z = st.sidebar.slider("z [m]",  -5.0, 5.0, 0.5, 0.1)

bx, by, bz = compute_series((x, y, z))

# --- 2×2 layout ---
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# 1. Time series
fig1, ax1 = plt.subplots()
ax1.plot(ANGLES_DEG, bx, label="Bx")
ax1.plot(ANGLES_DEG, by, label="By")
ax1.plot(ANGLES_DEG, bz, label="Bz")
ax1.set_xlabel("ωt [deg]"); ax1.set_ylabel("B [T]"); ax1.legend()
col1.pyplot(fig1)

# 2. Lissajous Bx-By
lim = np.max(np.abs(np.concatenate([bx, by])))
fig2, ax2 = plt.subplots()
ax2.plot(bx, by, marker="o")
ax2.set_xlabel("Bx [T]"); ax2.set_ylabel("By [T]")
ax2.set_xlim(-lim, lim); ax2.set_ylim(-lim, lim); ax2.set_aspect("equal")
col2.pyplot(fig2)

# 3. 3-D Trajectory
from mpl_toolkits.mplot3d import Axes3D  # noqa
fig3 = plt.figure()
ax3 = fig3.add_subplot(111, projection='3d')
ax3.plot(bx, by, bz, marker='o')
lim3 = np.max(np.abs(np.concatenate([bx, by, bz])))
ax3.set_xlim(-lim3, lim3); ax3.set_ylim(-lim3, lim3); ax3.set_zlim(-lim3, lim3)
ax3.set_xlabel("Bx [T]"); ax3.set_ylabel("By [T]"); ax3.set_zlabel("Bz [T]")
col3.pyplot(fig3)

# 4. Observation point map
fig4, ax4 = plt.subplots()
ax4.plot([x], [y], "ro")
ax4.set_xlim(-5, 5); ax4.set_ylim(-5, 5); ax4.set_aspect("equal")
ax4.grid(True, ls="--", lw=0.5); ax4.set_xlabel("x [m]"); ax4.set_ylabel("y [m]")
col4.pyplot(fig4)
"""Interactive web app using Streamlit + Plotly.
Run:
    streamlit run app.py
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from dipole import compute_series, ANGLES_DEG

st.set_page_config(page_title="Rotating Dipole Field", layout="wide")

st.title("Rotating Magnetic Dipole – Interactive Visualiser")

# Sidebar sliders (−5 … 5, 0.1 step)
x = st.sidebar.slider("x [m]", -5.0, 5.0, 0.0, 0.1)
y = st.sidebar.slider("y [m]", -5.0, 5.0, 0.0, 0.1)
z = st.sidebar.slider("z [m]", -5.0, 5.0, 0.5, 0.1)
point = (x, y, z)

# Compute field series
bx, by, bz = compute_series(point)

# Create four Plotly figures -------------------------------------------------

# 1. Time‑series
fig_ts = go.Figure()
fig_ts.add_trace(go.Scatter(x=ANGLES_DEG, y=bx, mode="lines", name="Bx"))
fig_ts.add_trace(go.Scatter(x=ANGLES_DEG, y=by, mode="lines", name="By"))
fig_ts.add_trace(go.Scatter(x=ANGLES_DEG, y=bz, mode="lines", name="Bz"))
fig_ts.update_layout(xaxis_title="ωt [deg]", yaxis_title="B [T]", margin=dict(l=0,r=0,t=20,b=0))

# 2. Lissajous Bx–By
lim2 = np.max(np.abs(np.concatenate([bx, by])))
fig_lis = go.Figure(go.Scatter(x=bx, y=by, mode="markers+lines"))
fig_lis.update_layout(xaxis_range=[-lim2, lim2], yaxis_range=[-lim2, lim2],
                      xaxis_title="Bx [T]", yaxis_title="By [T]", margin=dict(l=0,r=0,t=20,b=0),
                      yaxis_scaleanchor="x", yaxis_scaleratio=1)

# 3. 3‑D trajectory
lim3 = np.max(np.abs(np.concatenate([bx, by, bz])))
fig_3d = go.Figure(go.Scatter3d(x=bx, y=by, z=bz, mode="lines+markers"))
fig_3d.update_layout(scene=dict(xaxis_title="Bx [T]", yaxis_title="By [T]", zaxis_title="Bz [T]",
                                xaxis_range=[-lim3, lim3], yaxis_range=[-lim3, lim3], zaxis_range=[-lim3, lim3]),
                     margin=dict(l=0,r=0,t=20,b=0))

# 4. Observation point map (x‑y)
fig_xy = go.Figure(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(size=10, color="red")))
fig_xy.update_layout(xaxis_range=[-5, 5], yaxis_range=[-5, 5],
                     xaxis_title="x [m]", yaxis_title="y [m]", margin=dict(l=0,r=0,t=20,b=0),
                     yaxis_scaleanchor="x", yaxis_scaleratio=1)

# Layout: 2 × 2 grid ---------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_ts, use_container_width=True)
with col2:
    st.plotly_chart(fig_lis, use_container_width=True)
col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig_3d, use_container_width=True)
with col4:
    st.plotly_chart(fig_xy, use_container_width=True)

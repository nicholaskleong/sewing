import streamlit as st
from datetime import datetime
import boto3
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle
import plotly.graph_objects as go
import math
from cylinder import cylinder, boundary_circle

st.set_page_config(initial_sidebar_state='collapsed')

st.title('Cylinder Bag Calculator')

diameter= st.number_input('Diameter (mm)',value = 130,step=1,)
height = st.number_input('Height (mm)',value = 280,step=1)

with st.expander('Further config'):
    SEAM = st.number_input('Seam Allowance',value=10,step=1)
    TAPE = 20
    roll = st.number_input('Width of roll top (3 rolls)', value = 3*TAPE, step=1)
    stiffener = st.number_input('Width for stiffener wrap (2* tape)',value = 2*TAPE,step=1)
cut_diameter = diameter + SEAM * 2
body_width = math.pi * diameter + 2* SEAM
body_height = height + SEAM + roll + stiffener

volume = math.pi*(diameter/2)** 2 * height

st.write(f'Base (incl seam) : {cut_diameter:.0f}mm')
st.write(f'Body (incl seam): {body_width:.0f} x {body_height:.0f}mm')
st.write(f'Approx Volume: {volume/1000000:0.2f}L')


fig,ax = plt.subplots(figsize=(8,6))
circle = Circle((cut_diameter/2,cut_diameter/2),cut_diameter/2,edgecolor='black',fill=False)
rect = Rectangle((cut_diameter + 20,0),body_width,body_height,edgecolor='black',fill=False)
ax.add_patch(circle)
ax.text(cut_diameter/2,cut_diameter/2,s=f'{cut_diameter}mm (dia.)',horizontalalignment='center')
ax.add_patch(rect)
ax.text(cut_diameter + 20+body_width/2,5,f'{body_width:.0f}mm')
ax.text(cut_diameter + 20+5,body_height/2,f'{body_height:.0f}mm')
ax.set_xlim(-20,800)
ax.set_ylim(-20,600)
ax.axis('off')
st.pyplot(fig)

x1, y1, z1 = cylinder(diameter/2, height, a=0)
colorscale = [[0, 'blue'],
             [1, 'blue']]
cyl1 = go.Surface(x=x1, y=y1, z=z1,
                 colorscale = colorscale,
                 showscale=False,
                 opacity=0.5)
xb_low, yb_low, zb_low = boundary_circle(diameter/2, h=height)
xb_up, yb_up, zb_up = boundary_circle(diameter/2, h=0+height)

bcircles1 =go.Scatter3d(x = xb_low.tolist()+[None]+xb_up.tolist(),
                        y = yb_low.tolist()+[None]+yb_up.tolist(),
                        z = zb_low.tolist()+[None]+zb_up.tolist(),
                        mode ='lines',
                        line = dict(color='blue', width=2),
                        opacity =0.55, showlegend=False)

layout = go.Layout(scene_xaxis_visible=False, scene_yaxis_visible=False, scene_zaxis_visible=False)
fig =  go.Figure(data=[cyl1,bcircles1], layout=layout)
fig.update_layout(scene_camera_eye_z= 3)
# fig.layout.scene.camera.projection.type = "orthographic" #commenting this line you get a fig with perspective proj

st.plotly_chart(fig)

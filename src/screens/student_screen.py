import streamlit as st
import numpy as np
from src.ui.base_layout import style_background_dashboard
from src.ui.base_layout import style_base_layout
from src.components.header import header_dashboard
from PIL import Image
def student_screen():
    style_background_dashboard()
    style_base_layout()
    
    c1,c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    
    with c1:
      header_dashboard()
    with c2:
        st.button("← Back to Home",type='secondary',key='loginbackbtn',shortcut="control+backspace" ,on_click=lambda: st.session_state.update({'login_type': None}))
        
    
    st.space()
    st.header("Login Using Face Id",text_alignment='center')
    st.space()
    photo_source = st.camera_input("Position your face in the center")
    
    if photo_source:
        np.array(Image.open(photo_source))
        

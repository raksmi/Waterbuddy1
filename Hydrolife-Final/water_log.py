"""
Water logging page
"""

import streamlit as st
from datetime import datetime
from database import update_water_data

def show_water_log():
    """Water logging page"""
    st.markdown('<h1 style="text-align: center; color: white;">Log Water Intake</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: white; padding: 40px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); text-align: center;">
            <div style="font-size: 60px; margin-bottom: 16px;">💧</div>
            <h3 style="color: black;">Log Water Intake</h3>
            <p style="color: #666; margin-bottom: 24px;">Enter the amount in milliliters</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        amount = st.number_input("Amount (ml)", min_value=1, max_value=2000, value=500, step=50, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        
        col1, col2, col3, col4 = st.columns(4)
        presets = [250, 500, 750, 1000]
        for i, preset in enumerate(presets):
            with [col1, col2, col3, col4][i]:
                if st.button(str(preset), use_container_width=True, key=f"preset_{preset}"):
                    amount = preset
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        col_cancel, col_log = st.columns(2)
        with col_cancel:
            if st.button("Cancel", use_container_width=True):
                st.session_state.current_page = 'dashboard'
                st.rerun()
        with col_log:
            if st.button("Log Water", use_container_width=True, type="primary"):
                
                st.session_state.water_data['today_intake'] += amount
                st.session_state.water_data['total_sips'] += 1
                
                
                today_name = datetime.now().strftime('%a')
                for day in st.session_state.water_data['weekly_data']:
                    if day['day'] == today_name:
                        day['water'] = st.session_state.water_data['today_intake']
                
                
                update_water_data(st.session_state.user_id, st.session_state.water_data)
                
                st.success(f"Added {amount}ml! 💧")
                st.session_state.current_page = 'dashboard'
                st.rerun()

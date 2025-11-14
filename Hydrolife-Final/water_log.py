"""
Water logging page
"""

import streamlit as st
from datetime import datetime
from database import update_water_data

def show_water_log():
    """Water logging page with unit converter for cups ↔ ml and sidebar tips."""

    st.markdown('<h1 style="text-align: center; color: white;">Log Water Intake</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: white; padding: 40px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); text-align: center;">
            <div style="font-size: 60px; margin-bottom: 16px;">💧</div>
            <h3 style="color: black;">Log Water Intake</h3>
            <p style="color: #666; margin-bottom: 24px;">Enter the amount</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        
        unit = st.radio("Select unit", options=["ml", "cups"], horizontal=True)

        
        ML_IN_A_CUP = 240

        
        if unit == "ml":
            amount = st.number_input("Amount (ml)", min_value=1, max_value=2000, value=500, step=50, label_visibility="collapsed")
            presets = [250, 500, 750, 1000]
        else:
            amount_cups = st.number_input("Amount (cups)", min_value=0.1, max_value=8.0, value=2.0, step=0.2, format="%.2f", label_visibility="collapsed")
            amount = int(amount_cups * ML_IN_A_CUP)
            presets_cups = [1, 2, 3, 4]
            presets = [int(cup * ML_IN_A_CUP) for cup in presets_cups]
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        for i, preset_ml in enumerate(presets):
            with [col1, col2, col3, col4][i]:
                preset_display = preset_ml if unit == "ml" else round(preset_ml / ML_IN_A_CUP, 2)
                if st.button(str(preset_display), use_container_width=True, key=f"preset_{preset_display}"):
                    amount = preset_ml
        
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

        st.markdown("<br>", unsafe_allow_html=True)

        
        if 'user_data' in st.session_state:
            daily_goal = st.session_state.user_data.get('daily_goal', 2000)
            today_intake = st.session_state.water_data.get('today_intake', 0)
            remaining_water = max(0, daily_goal - today_intake)
            progress_percent = (today_intake / daily_goal) * 100 if daily_goal > 0 else 0
            remaining_percent = 100 - progress_percent
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(0, 212, 255, 0.1)); 
                border-radius: 12px; padding: 16px; text-align: center; 
                border: 2px solid rgba(102, 126, 234, 0.3);">
        <p style="color: #FFFFFF; font-size: 16px; font-weight: 600; margin: 0;">
            💧 {progress_percent:.1f}% achieved!
        </p>
    </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Show daily tip"):
            show_tip()

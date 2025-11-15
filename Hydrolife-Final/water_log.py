"""
Water Logging Page
"""

import streamlit as st
from datetime import datetime
from database import update_water_intake


def play_drink_sound():
    try:
        audio_file = open("drink.mp3", "rb").read()
        st.audio(audio_file, format="audio/mp3", start_time=0)
    except:
        pass 


def daily_tip():
    tips_list = [
        "Drinking water can boost your metabolism by up to 30%.",
        "A glass of water before meals can help with digestion.",
        "Staying hydrated improves concentration and mood.",
        "Dehydration can cause headaches—drink up regularly!",
        "Aim to drink at least 8 cups (about 2 liters) of water a day.",
        "Carry a reusable water bottle to make tracking your intake easy."
    ]

    import random
    tip = random.choice(tips_list)

    st.markdown(f"""
        <div style="background: white; border-radius: 16px; padding: 24px; 
        box-shadow: 0 6px 18px rgba(102,126,234,0.12); text-align: center;">
            <h3 style="color: #667eea;">💡 Daily Hydration Tip</h3>
            <p style="color: #222; font-size: 16px; font-weight: 500;">{tip}</p>
        </div>
    """, unsafe_allow_html=True)



def water_log():
    """Water logging page with ml ↔ cups converter & hydration tips."""

    st.markdown('<h1 style="text-align: center; color: white;">Log Water Intake</h1>',
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
   
        st.markdown("""
        <div style="background: white; padding: 40px; border-radius: 24px; 
        box-shadow: 0 10px 40px rgba(0,0,0,0.15); text-align: center;">
            <div style="font-size: 60px; margin-bottom: 16px;">💧</div>
            <h3 style="color: black;">Log Water Intake</h3>
            <p style="color: #666; margin-bottom: 24px;">Enter the user_amount</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

     
        units = st.radio("Select units", ["ml", "cups"], horizontal=True)
        ML_IN_A_CUP = 240

 
        if units == "ml":
            user_amount = st.number_input(
                "user_amount (ml)",
                min_value=1,
                max_value=2000,
                value=500,
                step=50,
                label_visibility="collapsed"
            )
        else:
       
            cups = st.number_input(
                "user_amount (cups)",
                min_value=0.1,
                max_value=8.0,
                value=2.0,
                step=0.2,
                format="%.2f",
                label_visibility="collapsed"
            )
            user_amount = int(cups * ML_IN_A_CUP)

        st.markdown("<br><br>", unsafe_allow_html=True)

   
        col_cancel, col_log = st.columns(2)

        
        with col_cancel:
            if st.button("Cancel", use_container_width=True):
                st.session_state.current_page = "dashboard"
                st.rerun()

   
        with col_log:
            if st.button("Log Water", use_container_width=True, type="primary"):

             
                st.session_state.water_data['water_intake'] += user_amount
                st.session_state.water_data['whole_sips'] += 1

                
                today = datetime.now().strftime("%a")
                for day in st.session_state.water_data['weekly_hist']:
                    if day["day"] == today:
                        day["water"] = st.session_state.water_data['water_intake']

                update_water_intake(st.session_state.id_user, st.session_state.water_data)

                st.success(f"Added {user_amount} ml! 💧")

              
                play_drink_sound()

             
                st.session_state.current_page = "dashboard"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if "user_data" in st.session_state:
            water_goal = st.session_state.user_data.get("water_goal", 2000)
            water_intake = st.session_state.water_data.get("water_intake", 0)

            progress_percent = (water_intake / water_goal) * 100

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(102,126,234,0.1), 
                rgba(0,212,255,0.1)); border-radius: 12px; padding: 16px; 
                text-align: center; border: 2px solid rgba(102,126,234,0.3);">
                <p style="color: white; font-size: 16px; font-weight: 600; margin: 0;">
                    💧 {progress_percent:.1f}% of your goal achieved!
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        
        if st.button("Show daily tips"):
            daily_tip()

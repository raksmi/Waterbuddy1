"""
Settings page
"""
import streamlit as st
from database import update_water_settings, update_remainder, reset_water_intake, update_water_intake
from datetime import datetime


def settings():
    """Settings page"""
    st.markdown('<h1 style="text-align: center; color: white;">Settings</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        
        st.markdown("""
        <div style="background: white; padding: 14px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                    👤
                </div>
                <h3 style="margin: 0;color: black;">Profile Information</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        name = st.text_input("Full Name", value=st.session_state.user_data['name'])
        age = st.number_input("Age", min_value=1, max_value=150, value=int(st.session_state.user_data['age']))
        
        if st.button("Save Changes", use_container_width=True, type="primary"):
            st.session_state.user_data['name'] = name
            st.session_state.user_data['age'] = str(age)
            update_water_settings(st.session_state.id_user, name, age, st.session_state.user_data['water_goal'])
            st.success("Profile updated! ✓")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        
        st.markdown("""
        <div style="background: white; padding: 14px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #00d4ff, #667eea); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                    🎯
                </div>
                <h3 style="margin: 0;color: black;">Daily Water Goal</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        water_goal = st.number_input(
            "Target (ml)", 
            min_value=1000, 
            max_value=5000, 
            value=st.session_state.user_data['water_goal'],
            step=100
        )
        
        st.info(f"💡 Recommended: {st.session_state.user_data['water_goal']}ml per day")
        
        if st.button("Update Goal", use_container_width=True):
            st.session_state.user_data['water_goal'] = water_goal
            update_water_settings(st.session_state.id_user, st.session_state.user_data['name'], 
                              int(st.session_state.user_data['age']), water_goal)
            st.success("Daily goal updated! ✓")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        
        st.markdown("""
        <div style="background: white; padding: 14px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #10b981, #34d399); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                    🔔
                </div>
                <h3 style="margin: 0;color: black;">notification</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        notification = st.checkbox(
            "Enable notification",
            value=st.session_state.settings['notification']
        )
        
        if notification:
            reminder_interval_user = st.selectbox(
                "Reminder Interval",
                options=[30, 60, 90, 120, 180],
                format_func=lambda x: f"Every {x} minutes" if x < 60 else f"Every {x//60} hour{'s' if x > 60 else ''}",
                index=[30, 60, 90, 120, 180].index(st.session_state.settings['reminder_interval_user'])
            )
            
            st.session_state.settings['notification'] = notification
            st.session_state.settings['reminder_interval_user'] = reminder_interval_user
            update_remainder(st.session_state.id_user, st.session_state.settings)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        
        st.markdown("""
        <div style="background: white; padding: 14px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">
            <h3 style="margin-bottom: 16px;color: black;">Account</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚪 Log Out", use_container_width=True, type="secondary"):
            
            st.session_state.logged_in = False
            st.session_state.id_user = None
            st.session_state.username = None
            if 'user_data' in st.session_state:
                del st.session_state.user_data
            if 'water_data' in st.session_state:
                del st.session_state.water_data
            if 'settings' in st.session_state:
                del st.session_state.settings
            
            st.success("Logged out successfully!")
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 14px; margin: 24px 0;">
            <p>HydroLife v1.0.0</p>
            <p>Your personal hydration companion 💧</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Reset Today's Water Intake", use_container_width=True, type="secondary"):
            reset_water_intake(st.session_state.id_user)
            st.session_state.water_data['water_intake'] = 0
            today = datetime.now().strftime('%a')  # 'Mon', 'Tue', etc.
            for day in st.session_state.water_data['weekly_hist']:
                if day['day'] == today:
                    day['water'] = 0
            update_water_intake(st.session_state.id_user, st.session_state.water_data)
            st.success("Today's water intake has been cleared! 💧")
            st.rerun()

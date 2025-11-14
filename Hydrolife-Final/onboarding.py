"""
Onboarding flow for new users
"""

import streamlit as st
from database import create_user
from helpers import calculate_daily_goal
from reminder_page import start_reminder 

def show_onboarding():
    """Complete onboarding flow for new users"""

    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 1

    if 'onboarding_data' not in st.session_state:
        st.session_state.onboarding_data = {
            'name': '',
            'age': 25,
            'health_conditions': [],
            'reminder_interval': 60
        }

    step = st.session_state.onboarding_step

    if step == 1:
        show_name_step()
    elif step == 2:
        show_age_step()
    elif step == 3:
        show_health_step()
    elif step == 4:
        show_reminder_step()


def show_name_step():
    """Step 1: Name"""
    st.markdown('<div style="text-align: right; color: rgba(255,255,255,0.7); margin-bottom: 16px;">Step 1 of 4</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align: center; color: white;">What\'s your name?</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: white; padding: 40px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); text-align: center;">
            <div style="font-size: 60px; margin-bottom: 16px;">👤</div>
            <h3 style="color:black;">What's your name?</h3>
            <p style="color: #666; margin-bottom: 24px;">Help us personalize your experience</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        name = st.text_input("Full Name", placeholder="Enter your full name", label_visibility="collapsed", value=st.session_state.onboarding_data.get('name', ''))

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Continue →", use_container_width=True, type="primary", disabled=not name):
            st.session_state.onboarding_data['name'] = name
            st.session_state.onboarding_step = 2
            st.rerun()


def show_age_step():
    """Step 2: Age"""
    st.markdown('<div style="text-align: right; color: rgba(255,255,255,0.7); margin-bottom: 16px;">Step 2 of 4</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align: center; color: white;">How old are you?</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: white; padding: 40px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); text-align: center;">
            <div style="font-size: 60px; margin-bottom: 16px;">📅</div>
            <h3 style="color:black;">Select your age range</h3>
            <p style="color: #666; margin-bottom: 24px;">We'll use this to calculate your ideal water goal</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Dropdown age ranges
        age_range = st.selectbox(
            "",
            ["Under 18", "18–29", "30–49", "50–64", "65+"],
            index=0
        )

        st.info("💡 Based on your age group, we'll suggest a personalized daily water goal.(You can change your water goal anytime in setting)")

        st.markdown("<br>", unsafe_allow_html=True)

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("← Back", use_container_width=True):
                st.session_state.onboarding_step = 1
                st.rerun()

        with col_next:
            if st.button("Continue →", use_container_width=True, type="primary"):
                st.session_state.onboarding_data['age_range'] = age_range
                st.session_state.onboarding_step = 3
                st.rerun()


def show_health_step():
    """Step 3: Health conditions"""
    st.markdown('<div style="text-align: right; color: rgba(255,255,255,0.7); margin-bottom: 16px;">Step 3 of 4</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align: center; color: white;">Health Considerations</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: white; padding: 40px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); text-align: center;">
            <div style="font-size: 60px; margin-bottom: 16px;">❤️</div>
            <h3 style="color:black;">Health Considerations</h3>
            <p style="color: #666; margin-bottom: 8px;">Help us personalize your hydration goals (optional)</p>
            <p style="color: #999; font-size: 14px;">Select any that apply:</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        health_options = {
            'diabetes': '🩸 Diabetes',
            'kidney': '🫘 Kidney Issues',
            'heart': '❤ Heart Condition',
            'athletic': '💪 Athletic/Active',
            'pregnant': '🤰 Pregnant',
            'none': '✅ None'
        }
        selected = []
        for key, label in health_options.items():
            if st.checkbox(label, key=f"health_{key}"):
                if key == 'none':
                    selected = ['none']
                    break
                selected.append(key)
        st.info("💡 We'll adjust your daily water goal based on your selections (You can change your water goal anytime in setting)")
        st.markdown("<br>", unsafe_allow_html=True)

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("← Back", use_container_width=True):
                st.session_state.onboarding_step = 2
                st.rerun()
        with col_next:
            if st.button("Continue →", use_container_width=True, type="primary"):
                st.session_state.onboarding_data['health_conditions'] = selected
                st.session_state.onboarding_step = 4
                st.rerun()


def show_reminder_step():
    """Step 4: Reminders"""
    st.markdown('<div style="text-align: right; color: rgba(255,255,255,0.7); margin-bottom: 16px;">Final Step</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align: center; color: white;">Set Your Reminders</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: white; padding: 40px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); text-align: center;">
            <div style="font-size: 60px; margin-bottom: 16px;" class="pulse-animation">🔔</div>
            <h3 style="color:black;">Set Your Reminders</h3>
            <p style="color: #666; margin-bottom: 24px;">We'll remind you to stay hydrated throughout the day!</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        reminder_options = {
            0: '🔕 No Reminders',
            30: '⏰ Every 30 minutes',
            60: '⏰ Every 1 hour',
            90: '⏰ Every 1.5 hours',
            120:'⏰ Every 2 hours',
            180:'⏰ Every 3 hours'
        }
        selected_interval = st.radio(
            "Select reminder frequency:",
            options=list(reminder_options.keys()),
            format_func=lambda x: reminder_options[x],
            index=2  
        )
        st.info("💡 You can change this anytime in Settings. IMP: Don't forget to update the same interval in the setting page")
        st.markdown("<br>", unsafe_allow_html=True)

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("Back", use_container_width=True):
                st.session_state.onboarding_step = 3
                st.rerun()
        with col_next:
            if st.button("How about we start with a sip?🎉", use_container_width=True, type="primary"):

                username = st.session_state.signup_username
                password = st.session_state.signup_password
                name = st.session_state.onboarding_data['name']
                age = st.session_state.onboarding_data['age']
                health_conditions = st.session_state.onboarding_data['health_conditions']
                daily_goal = calculate_daily_goal(str(age), health_conditions)
                reminder_interval = selected_interval
                st.session_state.onboarding_data['reminder_interval'] = reminder_interval

                success, result = create_user(username, password, name, age, health_conditions, daily_goal)

                if success:
                    user_id = result
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.session_state.show_onboarding = False
                    st.session_state.current_page = 'dashboard'

                    
                    if reminder_interval > 0:
                        start_reminder(reminder_interval)

                    
                    del st.session_state.onboarding_step
                    del st.session_state.onboarding_data
                    del st.session_state.signup_username
                    del st.session_state.signup_password

                    st.success(f"Welcome to HydroLife, {name}! 💧")
                    st.rerun()
                else:
                    st.error(f"Error creating account: {result}")



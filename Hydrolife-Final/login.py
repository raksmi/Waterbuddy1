"""
Login/Signup page for HydroLife
"""

import streamlit as st
from database import user_exists, verify_user, get_all_usernames

def show_login():
    """Show login/signup page"""
    st.markdown("""
    <div style="text-align: center; padding: 25px 0;">
        <div style="font-size: 80px; margin-bottom: 4px;">💧</div>
        <h1 style="color: white; font-family: Arial, sans-serif; margin-bottom: 4px;style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;">
            Welcome to HydroLife
        </h1>
        <p style="color: black; font-size: 18px;">Your personal hydration companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        usernames = get_all_usernames()
        
        if usernames:
            st.markdown("""
            <div style="background: #001F3F; padding: 32px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); color: white;">
            <h3 style="text-align: center; margin-bottom: 24px;">Are you a returning user?</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            user_type = st.radio(
                "Select an option:",
                ["Existing User", "New User"],
                horizontal=True,
                label_visibility="collapsed"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if user_type == "Existing User":
                show_existing_user_login(usernames)
            else:
                show_new_user_signup()
        else:
            st.markdown("""
            <div style="background: white; padding: 32px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
                <h3 style="text-align: center; margin-bottom: 8px;">Create Your Account</h3>
                <p style="text-align: center; color: black; font-size: 14px;">Start your hydration journey today!</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            show_new_user_signup()

def show_existing_user_login(usernames):
    """Show login form for existing users"""
    st.markdown("""
 <div style="background: white; padding: 32px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
    <div style="text-align: center; margin-bottom: 24px;">
        <div style="font-size: 48px; margin-bottom: 8px;">🔐</div>
        <h3 style="color: black;">Welcome Back!</h3>
    </div>
</div>

    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    username = st.selectbox(
        "Select your username:",
        options=usernames,
        index=0
    )
    
    password = st.text_input(
        "Enter your password:",
        type="password",
        placeholder="Your password"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("Login →", use_container_width=True, type="primary"):
            if not password:
                st.error("Please enter your password")
            else:
                user_id = verify_user(username, password)
                if user_id:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.session_state.current_page = 'dashboard'
                    st.success(f"Welcome back, {username}! 💧")
                    st.rerun()
                else:
                    st.error("Invalid password. Please try again.")

def show_new_user_signup():
    """Show signup form for new users"""
    st.markdown("""
    <div style="background: white; padding: 32px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
        <div style="background: white; padding: 32px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
        <h3 style="text-align: center; margin-bottom: 8px; color: black;">Create Your Account</h3>
        <p style="text-align: center; color: blue; font-size: 14px;">Start your hydration journey today!</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    username = st.text_input(
        "Choose a username:",
        placeholder="Enter a unique username",
        max_chars=50
    )

    password = st.text_input(
        "Create a password:",
        type="password",
        placeholder="At least 4 characters",
        max_chars=100
    )

    confirm_password = st.text_input(
        "Confirm password:",
        type="password",
        placeholder="Re-enter your password",
        max_chars=100
    )
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.info("💡 You'll complete your profile setup after creating your account")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Continue to Profile Setup →", use_container_width=True, type="primary"):
       
        if not username or not password:
            st.error("Please fill in all fields")
        elif len(password) < 4:
            st.error("Password must be at least 4 characters long")
        elif password != confirm_password:
            st.error("Passwords do not match")
        elif user_exists(username):
            st.error("Username already exists. Please choose a different username.")
        else:
        
            st.session_state.signup_username = username
            st.session_state.signup_password = password
            st.session_state.show_onboarding = True
            st.success("Great! Let's set up your profile...")
            st.rerun()

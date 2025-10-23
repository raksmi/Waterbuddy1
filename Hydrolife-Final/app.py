import streamlit as st

from login import show_login
from onboarding import show_onboarding
from dashboard import show_dashboard
from water_log import show_water_log
from progress import show_progress
from games import show_games
from settings import show_settings

from database import init_database, get_user_data, update_water_data
from helpers import check_and_reset_daily

st.set_page_config(
    page_title="HydroLife",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main {
        padding: 0 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    }
    
    .stButton > button {
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 12px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .nav-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-top: 1px solid rgba(0, 0, 0, 0.1);
        padding: 16px;
        z-index: 1000;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .stDeployButton {display: none;}
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .pulse-animation {
        animation: pulse 2s ease-in-out infinite;
    }
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    
    if 'show_onboarding' not in st.session_state:
        st.session_state.show_onboarding = False
    
    if 'signup_username' not in st.session_state:
        st.session_state.signup_username = None
    
    if 'signup_password' not in st.session_state:
        st.session_state.signup_password = None
   
    if st.session_state.logged_in and st.session_state.user_id:
        if 'user_data' not in st.session_state:
            data = get_user_data(st.session_state.user_id)
            if data:
                
                data['water_data'] = check_and_reset_daily(data['water_data'])
                update_water_data(st.session_state.user_id, data['water_data'])
                
                st.session_state.user_data = data['user_data']
                st.session_state.water_data = data['water_data']
                st.session_state.settings = data['settings']

def show_navigation():
    """Bottom navigation bar"""
    if not st.session_state.logged_in:
        return
    
    pages = [
        {'id': 'dashboard', 'icon': '🏠', 'label': 'Home'},
        {'id': 'log', 'icon': '💧', 'label': 'Sips'},
        {'id': 'progress', 'icon': '📊', 'label': 'Stats'},
        {'id': 'games', 'icon': '🎮', 'label': 'Games'},
        {'id': 'settings', 'icon': '⚙️', 'label': 'Settings'},
    ]
    
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    cols = st.columns(5)
    
    for i, page in enumerate(pages):
        with cols[i]:
            is_active = st.session_state.current_page == page['id']
            
            if st.button(
                f"{page['icon']}\n{page['label']}", 
                use_container_width=True, 
                key=f"nav_{page['id']}",
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_page = page['id']
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

def main():
    """Main application entry point"""
    load_css()
    init_session_state()
    init_database()
    
    
    if st.session_state.show_onboarding:
        show_onboarding()
        return
    
    
    if not st.session_state.logged_in:
        show_login()
        return
    
    if st.session_state.current_page == 'dashboard':
        show_dashboard()
    elif st.session_state.current_page == 'log':
        show_water_log()
    elif st.session_state.current_page == 'progress':
        show_progress()
    elif st.session_state.current_page == 'games':
        show_games()
    elif st.session_state.current_page == 'settings':
        show_settings()
    
    show_navigation()

if __name__ == "__main__":
    main()

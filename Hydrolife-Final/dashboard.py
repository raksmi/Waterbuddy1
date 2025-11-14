import streamlit as st
from datetime import datetime
from database import update_water_data, get_user_data
from helpers import get_avatar, get_level, check_and_reset_daily


def show_dashboard():
    st.session_state.water_data = check_and_reset_daily(st.session_state.water_data)
    update_water_data(st.session_state.user_id, st.session_state.water_data)
    
    
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); padding: 24px; border-bottom: 1px solid rgba(255, 255, 255, 0.2); margin-bottom: 24px;">
        <h2 style="color: black; margin: 0;">Hi, {st.session_state.user_data['name']}! </h2>
        <p style="color: rgba(255, 255, 255, 0.8); margin: 4px 0 0 0;">How about a sip?!!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        
        today_intake = st.session_state.water_data['today_intake']
        daily_goal = st.session_state.user_data['daily_goal']
        progress = (today_intake / daily_goal) * 100
        avatar = get_avatar(progress)
        level = get_level(today_intake)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #00d4ff 100%); 
                    border-radius: 20px; padding: 14px; margin: 20px 0; 
                    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
                    border: 1px solid rgba(255, 255, 255, 0.2);">
            <div style="text-align: center;">
                <div style="font-size: 40px; margin-bottom: 16px;"></div>
                <h3 style="color: white; margin: 0 0 12px 0; font-weight: 600;">Here’s a wave of knowledge for you🌊!!</h3>
                <p style="color: rgba(255, 255, 255, 0.95); margin: 0; font-size: 15px; line-height: 1.2; font-style: italic;">
                    Just like molecules need bonding to stay strong, your body needs water to function at its best. 
                    Keep sipping, stay energized, and let every drop count! 🌟
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: white; padding: 40px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); text-align: center;">
            <div style="font-size: 80px; margin-bottom: 24px;" class="pulse-animation">{avatar}</div>
            <div style="margin: 24px 0;">
                <div style="font-size: 48px; color: #667eea; font-weight: 700;">{today_intake}ml</div>
                <p style="color: #666;">of {daily_goal}ml goal
                 You're evolving! Just like the moon🌙</p>
            </div>
            <div style="background: #e0e0e0; border-radius: 50px; height: 12px; overflow: hidden; margin: 16px 0;">
                <div style="background: linear-gradient(90deg, #667eea 0%, #00d4ff 100%); height: 100%; width: {min(progress, 100)}%; border-radius: 50px; transition: width 0.5s ease;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; color: #666; font-size: 14px;">
                <span>{int(min(progress, 100))}%</span>
                <span>Level {level}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        
        col_250, col_500, col_750 = st.columns(3)
        
        with col_250:
            if st.button("💧\n250ml", use_container_width=True):
                add_water(250)
        
        with col_500:
            if st.button("💧\n500ml", use_container_width=True, type="primary"):
                add_water(500)
        
        with col_750:
            if st.button("💧\n750ml", use_container_width=True):
                add_water(750)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("➕ Log Water Intake", use_container_width=True):
            st.session_state.current_page = 'log'
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Stats
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7)); padding: 20px; border-radius: 16px; text-align: center; box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
                <div style="font-size: 32px;">🔥</div>
                <p style="color: #666; font-size: 12px; margin: 8px 0 4px 0;">Streak</p>
                <p style="color: #f97316; font-size: 24px; font-weight: 700; margin: 0;">{st.session_state.water_data['streak']} days</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7)); padding: 20px; border-radius: 16px; text-align: center; box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
                <div style="font-size: 32px;">💧</div>
                <p style="color: #666; font-size: 12px; margin: 8px 0 4px 0;">Total Sips</p>
                <p style="color: #10b981; font-size: 24px; font-weight: 700; margin: 0;">{st.session_state.water_data['total_sips']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        

        
        # Navigation
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("📊 Progress\nView stats", use_container_width=True):
                st.session_state.current_page = 'progress'
                st.rerun()
        
        with col_nav2:
            if st.button("🎮 Games\nPlay & Learn", use_container_width=True):
                st.session_state.current_page = 'games'
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        
        if today_intake >= daily_goal:
            message = "You've reached your goal today! Amazing! 🎉"
            emoji = "🏆"
        else:
            remaining = daily_goal - today_intake
            message = f"You're {remaining}ml away from your goal"
            emoji = "💪"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 50%, #ec4899 100%); border-radius: 16px; padding: 24px; color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="font-size: 48px;">{emoji}</div>
                <div>
                    <h4 style="color: white; margin: 0 0 8px 0;">Keep it up!</h4>
                    <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 14px;">{message}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def add_water(amount):
    """Add water intake"""
    st.session_state.water_data['today_intake'] += amount
    st.session_state.water_data['total_sips'] += 1
    
    
    today_name = datetime.now().strftime('%a')
    for day in st.session_state.water_data['weekly_data']:
        if day['day'] == today_name:
            day['water'] = st.session_state.water_data['today_intake']
    
    
    update_water_data(st.session_state.user_id, st.session_state.water_data)
    
    st.success(f"Added {amount}ml! 💧")
    st.rerun()


import streamlit as st
from datetime import datetime
from database import update_water_intake, get_userdata
from helpers import get_avatar, get_level, reset_daily


def dashboard():
    st.session_state.water_data = reset_daily(st.session_state.water_data)
    update_water_intake(st.session_state.id_user, st.session_state.water_data)
    
    
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); padding: 24px; border-bottom: 1px solid rgba(255, 255, 255, 0.2); margin-bottom: 24px;">
        <h2 style="color: black; margin: 0;">Hi, {st.session_state.user_data['name']}! </h2>
        <p style="color: rgba(255, 255, 255, 0.8); margin: 4px 0 0 0;">How about a sip?!!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        
        water_intake = st.session_state.water_data['water_intake']
        water_goal = st.session_state.user_data['water_goal']
        progress = (water_intake / water_goal) * 100
        avatar = get_avatar(progress)
        level = get_level(water_intake)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #00d4ff 100%); 
                    border-radius: 20px; padding: 14px; margin: 20px 0; 
                    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
                    border: 1px solid rgba(255, 255, 255, 0.2);">
            <div style="text-align: center;">
                <div style="font-size: 40px; margin-bottom: 16px;"></div>
                <h3 style="color: white; margin: 0 0 12px 0; font-weight: 600;">Here's a wave of knowledge for you🌊!!</h3>
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
                <div style="font-size: 48px; color: #667eea; font-weight: 700;">{water_intake}ml</div>
                <p style="color: #666;">of {water_goal}ml goal
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
                add_intake(250)
        
        with col_500:
            if st.button("💧\n500ml", use_container_width=True, type="primary"):
                add_intake(500)
        
        with col_750:
            if st.button("💧\n750ml", use_container_width=True):
                add_intake(750)
        
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
                <p style="color: #666; font-size: 12px; margin: 8px 0 4px 0;">whole Sips</p>
                <p style="color: #10b981; font-size: 24px; font-weight: 700; margin: 0;">{st.session_state.water_data['whole_sips']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 🎉 EPIC CELEBRATION ANIMATION
        if water_intake >= water_goal:
            motivation = "You've reached your goal today! Amazing! 🎉"
            emoji = "🏆"

            st.markdown("""
            <style>
                @keyframes firework {
                    0% { transform: translate(0, 0); opacity: 1; }
                    100% { transform: translate(var(--x), var(--y)); opacity: 0; }
                }
                
                @keyframes trophy-bounce {
                    0%, 100% { transform: translateY(0) scale(1); }
                    25% { transform: translateY(-30px) scale(1.2); }
                    50% { transform: translateY(0) scale(1.1); }
                    75% { transform: translateY(-15px) scale(1.15); }
                }
                
                @keyframes wave-pulse {
                    0%, 100% { transform: scale(1); opacity: 0.8; }
                    50% { transform: scale(1.5); opacity: 0; }
                }
                
                @keyframes sparkle {
                    0%, 100% { transform: scale(0) rotate(0deg); opacity: 0; }
                    50% { transform: scale(1) rotate(180deg); opacity: 1; }
                }
                
                .celebration-container {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100vw;
                    height: 100vh;
                    pointer-events: none;
                    z-index: 9999;
                    overflow: hidden;
                }
                
                .trophy-celebration {
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    font-size: 120px;
                    animation: trophy-bounce 1s ease-in-out 3;
                    filter: drop-shadow(0 0 30px rgba(255, 215, 0, 0.8));
                }
                
                .success-text {
                    position: fixed;
                    top: 40%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    font-size: 48px;
                    font-weight: bold;
                    color: #FFD700;
                    text-shadow: 0 0 20px rgba(255, 215, 0, 0.8),
                                 0 0 40px rgba(255, 215, 0, 0.6),
                                 0 0 60px rgba(255, 215, 0, 0.4);
                    animation: trophy-bounce 1s ease-in-out 3;
                }
            </style>
            
            <div class="celebration-container" id="celebration">
                <div class="success-text">🎊 GOAL ACHIEVED! 🎊</div>
                <div class="trophy-celebration">🏆</div>
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
            <script>
                // Multi-stage confetti celebration
                const duration = 5000;
                const animationEnd = Date.now() + duration;
                const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 10000 };

                function randomInRange(min, max) {
                    return Math.random() * (max - min) + min;
                }

                // Stage 1: Initial burst
                confetti({
                    ...defaults,
                    particleCount: 200,
                    origin: { x: 0.5, y: 0.5 },
                    colors: ['#FFD700', '#FFA500', '#FF69B4', '#00CED1', '#9370DB', '#32CD32']
                });

                // Stage 2: Side bursts
                setTimeout(() => {
                    confetti({
                        ...defaults,
                        particleCount: 100,
                        origin: { x: 0, y: 0.6 },
                        colors: ['#00BFFF', '#1E90FF', '#87CEFA']
                    });
                    confetti({
                        ...defaults,
                        particleCount: 100,
                        origin: { x: 1, y: 0.6 },
                        colors: ['#FFD700', '#FFA500', '#FF6347']
                    });
                }, 400);

                // Stage 3: Emoji rain
                setTimeout(() => {
                    confetti({
                        particleCount: 50,
                        angle: 60,
                        spread: 55,
                        origin: { x: 0, y: 0.6 },
                        shapes: ['circle'],
                        colors: ['#FFD700', '#FFA500', '#FF69B4']
                    });
                    confetti({
                        particleCount: 50,
                        angle: 120,
                        spread: 55,
                        origin: { x: 1, y: 0.6 },
                        shapes: ['circle'],
                        colors: ['#00CED1', '#9370DB', '#32CD32']
                    });
                }, 800);

                // Stage 4: Continuous rain
                const interval = setInterval(function() {
                    const timeLeft = animationEnd - Date.now();

                    if (timeLeft <= 0) {
                        clearInterval(interval);
                        document.getElementById('celebration').style.display = 'none';
                        return;
                    }

                    const particleCount = 50 * (timeLeft / duration);
                    
                    confetti({
                        ...defaults,
                        particleCount: particleCount,
                        origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 },
                        colors: ['#00BFFF', '#1E90FF', '#87CEFA', '#ADD8E6']
                    });
                    
                    confetti({
                        ...defaults,
                        particleCount: particleCount,
                        origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 },
                        colors: ['#FFD700', '#FFA500', '#FF69B4', '#FF6347']
                    });
                }, 250);

                // Stage 5: Fireworks effect
                setTimeout(() => {
                    for(let i = 0; i < 5; i++) {
                        setTimeout(() => {
                            confetti({
                                particleCount: 150,
                                spread: 360,
                                origin: { 
                                    x: randomInRange(0.2, 0.8), 
                                    y: randomInRange(0.2, 0.6) 
                                },
                                colors: ['#FFD700', '#FFA500', '#FF69B4', '#00CED1', '#9370DB', '#32CD32'],
                                startVelocity: 45,
                                ticks: 80,
                                gravity: 1.2,
                                scalar: 1.2
                            });
                        }, i * 600);
                    }
                }, 1500);

                // Stage 6: Stars burst
                setTimeout(() => {
                    confetti({
                        particleCount: 100,
                        spread: 160,
                        origin: { y: 0.3 },
                        shapes: ['star'],
                        colors: ['#FFD700', '#FFA500', '#FFFF00'],
                        scalar: 1.5,
                        startVelocity: 35
                    });
                }, 2500);

                // Remove celebration overlay after animation
                setTimeout(() => {
                    document.getElementById('celebration').style.display = 'none';
                }, duration);
            </script>
            """, unsafe_allow_html=True)

        else:
            remaining = water_goal - water_intake
            motivation = f"You're {remaining}ml away from your goal"
            emoji = "💪"

        
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
        
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 50%, #ec4899 100%); border-radius: 16px; padding: 24px; color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="font-size: 48px;">{emoji}</div>
                <div>
                    <h4 style="color: white; margin: 0 0 8px 0;">Keep it up!</h4>
                    <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 14px;">{motivation}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def add_intake(amount):
    """Add water intake"""
    st.session_state.water_data['water_intake'] += amount
    st.session_state.water_data['whole_sips'] += 1
    
    
    today = datetime.now().strftime('%a')
    for day in st.session_state.water_data['weekly_hist']:
        if day['day'] == today:
            day['water'] = st.session_state.water_data['water_intake']
    
    
    update_water_intake(st.session_state.id_user, st.session_state.water_data)
    
    st.success(f"Added {amount}ml! 💧")
    st.rerun()

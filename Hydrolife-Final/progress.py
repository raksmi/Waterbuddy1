import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

def show_progress():
    """Progress page with stats and charts"""
    st.markdown('<h1 style="text-align: center; color: white;">Progress & Stats</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        weekly_data = st.session_state.water_data['weekly_data']
        total_week = sum(day['water'] for day in weekly_data)
        avg_daily = total_week / 7
        best_day = max(weekly_data, key=lambda x: x['water'])
        daily_goal = st.session_state.user_data['daily_goal']
        days_met = sum(1 for day in weekly_data if day['water'] >= daily_goal)
        consistency = int((days_met / 7) * 100)
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; 
                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px;">Avg Daily</p>
                <p style="color: #667eea; font-size: 28px; font-weight: 700;">{int(avg_daily)}ml</p>
                <p style="color: #10b981; font-size: 12px;">{'✓ Goal' if avg_daily >= daily_goal else 'Keep going!'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; 
                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px;">Best Day</p>
                <p style="color: #764ba2; font-size: 28px; font-weight: 700;">{best_day['water']}ml</p>
                <p style="color: #666; font-size: 12px;">{best_day['day']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; 
                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px;">Total Week</p>
                <p style="color: #00d4ff; font-size: 28px; font-weight: 700;">{total_week}ml</p>
                <p style="color: #10b981; font-size: 12px;">{'Goal met!' if total_week >= daily_goal * 7 else 'Keep going!'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; 
                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px;">Consistency</p>
                <p style="color: #f97316; font-size: 28px; font-weight: 700;">{consistency}%</p>
                <p style="color: #10b981; font-size: 12px;">{'Excellent' if consistency >= 80 else 'Keep it up!'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div style="background: white; padding: 4px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white; margin-bottom: 24px;">Daily Water Intake</h3>', unsafe_allow_html=True)
        
        days = [d['day'] for d in weekly_data]
        waters = [d['water'] for d in weekly_data]

        fig, ax = plt.subplots()
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        colors_gradient = plt.cm.cool(np.linspace(0.3, 0.9, len(waters)))
        bars = ax.bar(days, waters, color=colors_gradient, edgecolor='none', alpha=0.9, width=0.6)
        
        for bar, value in zip(bars, waters):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value}', ha='center', va='bottom',
                    fontsize=10, fontweight='bold', color='#333333')
        
        light_gray = (0, 0, 0, 0.05)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(light_gray)
        ax.spines['bottom'].set_color(light_gray)
        
        ax.tick_params(colors='#999999', labelsize=10)
        ax.grid(axis='y', alpha=0.05, linestyle='-', linewidth=0.5)
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div style="background: white; padding: 4px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white; margin-bottom: 24px;">Hydration Trend</h3>', unsafe_allow_html=True)
        
        fig2, ax2 = plt.subplots(figsize=(12, 3))
        fig2.patch.set_facecolor('white')
        ax2.set_facecolor('white')
        
        x_pos = np.arange(len(days))
        ax2.plot(x_pos, waters, color='#764ba2', linewidth=3, marker='o', 
                 markersize=10, markerfacecolor='#764ba2', markeredgecolor='white', 
                 markeredgewidth=2, zorder=3)
        
        ax2.fill_between(x_pos, waters, alpha=0.1, color='#764ba2')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(days)
        
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_color(light_gray)
        ax2.spines['bottom'].set_color(light_gray)
        
        ax2.tick_params(colors='#999999', labelsize=10)
        ax2.grid(axis='y', alpha=0.05, linestyle='-', linewidth=0.5)
        
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)
        
        st.markdown('</div>', unsafe_allow_html=True)









"""
Progress and statistics page
"""
'''
import streamlit as st
import plotly.graph_objects as go

def show_progress():
    """Progress page with stats and charts"""
    st.markdown('<h1 style="text-align: center; color: white;">Progress & Stats</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
       
        weekly_data = st.session_state.water_data['weekly_data']
        total_week = sum(day['water'] for day in weekly_data)
        avg_daily = total_week / 7
        best_day = max(weekly_data, key=lambda x: x['water'])
        daily_goal = st.session_state.user_data['daily_goal']
        days_met = sum(1 for day in weekly_data if day['water'] >= daily_goal)
        consistency = int((days_met / 7) * 100)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px; margin: 0 0 4px 0;">Avg Daily</p>
                <p style="color: #667eea; font-size: 28px; font-weight: 700; margin: 0 0 4px 0;">{int(avg_daily)}ml</p>
                <p style="color: #10b981; font-size: 12px; margin: 0;">{'✓ Goal' if avg_daily >= daily_goal else 'Keep going!'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px; margin: 0 0 4px 0;">Best Day</p>
                <p style="color: #764ba2; font-size: 28px; font-weight: 700; margin: 0 0 4px 0;">{best_day['water']}ml</p>
                <p style="color: #666; font-size: 12px; margin: 0;">{best_day['day']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px; margin: 0 0 4px 0;">Total Week</p>
                <p style="color: #00d4ff; font-size: 28px; font-weight: 700; margin: 0 0 4px 0;">{total_week}ml</p>
                <p style="color: #10b981; font-size: 12px; margin: 0;">{'Goal met!' if total_week >= daily_goal * 7 else 'Keep going!'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px; margin: 0 0 4px 0;">Consistency</p>
                <p style="color: #f97316; font-size: 28px; font-weight: 700; margin: 0 0 4px 0;">{consistency}%</p>
                <p style="color: #10b981; font-size: 12px; margin: 0;">{'Excellent' if consistency >= 80 else 'Keep it up!'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        
        st.markdown('<div style="background: white; padding: 4px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white; margin-bottom: 24px;">Daily Water Intake</h3>', unsafe_allow_html=True)
        
        days = [d['day'] for d in weekly_data]
        waters = [d['water'] for d in weekly_data]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=days,
            y=waters,
            marker=dict(
                color=waters,
                colorscale=[[0, '#667eea'], [1, '#00d4ff']],
                line=dict(width=0)
            ),
            text=waters,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>%{y}ml<extra></extra>'
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            font=dict(family='Inter, sans-serif')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        
        st.markdown('<div style="background: white; padding: 4px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white; margin-bottom: 24px;">Hydration Trend</h3>', unsafe_allow_html=True)
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=days,
            y=waters,
            mode='lines+markers',
            line=dict(color='white', width=3),
            marker=dict(size=10, color='#764ba2'),
            fill='tozeroy',
            fillcolor='rgba(118, 75, 162, 0.1)',
            hovertemplate='<b>%{x}</b><br>%{y}ml<extra></extra>'
        ))
        
        fig2.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            font=dict(family='Inter, sans-serif')
        )
    '''
        
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

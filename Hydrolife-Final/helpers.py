"""
Helper functions for HydroLife
Shared utilities across all pages
"""

from datetime import datetime, date

def calculate_goal(age, health_conditions):
    """Calculate recommended water intake based on age and health conditions"""
    age = int(age)
    nor_goal = 2500  
    
    
    if age < 18:
        nor_goal = 2000
    elif age >= 18 and age < 30:
        nor_goal = 2500
    elif age >= 30 and age < 50:
        nor_goal = 2500
    elif age >= 50 and age < 65:
        nor_goal = 2200
    else:  
        nor_goal = 2000
    
    
    if 'athletic' in health_conditions:
        nor_goal += 1000
    if 'pregnant' in health_conditions:
        nor_goal += 700
    if 'diabetes' in health_conditions:
        nor_goal += 500
    if 'kidney' in health_conditions:
        nor_goal -= 500
    
    return max(1500, min(nor_goal, 5000))

def get_avatar(progress):
    """Get avatar emoji based on progress percentage"""
    if progress >= 100:
        return "🌕"
    elif progress >= 75:
        return "🌔"
    elif progress >= 50:
        return "🌓"
    elif progress >= 25:
        return "🌒"
    else:
        return "🌑"

def get_level(intake):
    """Get level based on water intake"""
    if intake >= 4000:
        return 8
    elif intake >= 3500:
        return 7
    elif intake >= 3000:
        return 6
    elif intake >= 2500:
        return 5
    elif intake >= 2000:
        return 4
    elif intake >= 1500:
        return 3
    elif intake >= 1000:
        return 2
    else:
        return 1

def reset_daily(water_data):
    """Check if it's a new day and reset daily intake"""
    today = str(date.today())
    yesterday = water_data.get('yesterday', today)
    
    if yesterday != today:
        
        yesterday_intake = water_data.get('water_intake', 0)
        
        
        data = water_data.get('data', {})
        data[yesterday] = yesterday_intake
        
        
        water_goal = water_data.get('water_goal', 2500)
        goal_comp = yesterday_intake >= water_goal
        new_streak = water_data.get('streak', 0) + 1 if goal_comp else 0
        
        
        yesterdaytime = datetime.strptime(yesterday, '%Y-%m-%d')
        day_name = yesterdaytime.strftime('%a')
        
        weekly_hist = water_data.get('weekly_hist', [])
        
        for i, day in enumerate(weekly_hist):
            if day['day'] == day_name:
                weekly_hist[i]['water'] = yesterday_intake
                break
        
        
        water_data['water_intake'] = 0
        water_data['yesterday'] = today
        water_data['streak'] = new_streak
        water_data['weekly_hist'] = weekly_hist
        water_data['data'] = data
    
    return water_data


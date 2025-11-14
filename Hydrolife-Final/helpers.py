"""
Helper functions for HydroLife
Shared utilities across all pages
"""

from datetime import datetime, date

def calculate_daily_goal(age, health_conditions):
    """Calculate recommended water intake based on age and health conditions"""
    age_num = int(age)
    base_goal = 2500  
    
    
    if age_num < 18:
        base_goal = 2000
    elif age_num >= 18 and age_num < 30:
        base_goal = 2500
    elif age_num >= 30 and age_num < 50:
        base_goal = 2500
    elif age_num >= 50 and age_num < 65:
        base_goal = 2200
    else:  
        base_goal = 2000
    
    
    if 'athletic' in health_conditions:
        base_goal += 1000
    if 'pregnant' in health_conditions:
        base_goal += 700
    if 'diabetes' in health_conditions:
        base_goal += 500
    if 'kidney' in health_conditions:
        base_goal -= 500
    
    return max(1500, min(base_goal, 5000))

def get_avatar(progress):
    """Get avatar emoji based on progress percentage"""
    if progress >= 100:
        return "🫡"
    elif progress >= 75:
        return "😄"
    elif progress >= 50:
        return "🫠"
    elif progress >= 25:
        return "😗"
    else:
        return "😑"

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

def check_and_reset_daily(water_data):
    """Check if it's a new day and reset daily intake"""
    today = str(date.today())
    last_date = water_data.get('last_date', today)
    
    if last_date != today:
        
        yesterday_intake = water_data.get('today_intake', 0)
        
        
        history = water_data.get('history', {})
        history[last_date] = yesterday_intake
        
        
        daily_goal = water_data.get('daily_goal', 2500)
        goal_met = yesterday_intake >= daily_goal
        new_streak = water_data.get('streak', 0) + 1 if goal_met else 0
        
        
        last_datetime = datetime.strptime(last_date, '%Y-%m-%d')
        day_name = last_datetime.strftime('%a')
        
        weekly_data = water_data.get('weekly_data', [])
        
        for i, day in enumerate(weekly_data):
            if day['day'] == day_name:
                weekly_data[i]['water'] = yesterday_intake
                break
        
        
        water_data['today_intake'] = 0
        water_data['last_date'] = today
        water_data['streak'] = new_streak
        water_data['weekly_data'] = weekly_data
        water_data['history'] = history
    
    return water_data

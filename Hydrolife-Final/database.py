"""
Database module for HydroLife
Handles user authentication and data storage using SQLite
"""

import sqlite3
import hashlib
import json
from datetime import date
import os

DB_FILE = "hydrolife.db"

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT,
            age INTEGER,
            health_conditions TEXT,
            daily_goal INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS water_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            today_intake INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            total_sips INTEGER DEFAULT 0,
            weekly_data TEXT,
            last_date TEXT,
            history TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            notifications INTEGER DEFAULT 0,
            reminder_interval INTEGER DEFAULT 60,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(username, password, name, age, health_conditions, daily_goal):
    """Create a new user account"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        hashed_pwd = hash_password(password)
        health_json = json.dumps(health_conditions)
        
        
        cursor.execute('''
            INSERT INTO users (username, password, name, age, health_conditions, daily_goal)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, hashed_pwd, name, age, health_json, daily_goal))
        
        user_id = cursor.lastrowid
        
        
        weekly_data = json.dumps([
            {'day': 'Mon', 'water': 0},
            {'day': 'Tue', 'water': 0},
            {'day': 'Wed', 'water': 0},
            {'day': 'Thu', 'water': 0},
            {'day': 'Fri', 'water': 0},
            {'day': 'Sat', 'water': 0},
            {'day': 'Sun', 'water': 0},
        ])
        
        cursor.execute('''
            INSERT INTO water_data (user_id, weekly_data, last_date, history)
            VALUES (?, ?, ?, ?)
        ''', (user_id, weekly_data, str(date.today()), '{}'))
        
        
        cursor.execute('''
            INSERT INTO settings (user_id)
            VALUES (?)
        ''', (user_id,))
        
        conn.commit()
        conn.close()
        return True, user_id
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    except Exception as e:
        return False, str(e)

def verify_user(username, password):
    """Verify user credentials"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    hashed_pwd = hash_password(password)
    
    cursor.execute('''
        SELECT id FROM users WHERE username = ? AND password = ?
    ''', (username, hashed_pwd))
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None

def user_exists(username):
    """Check if username already exists"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    
    return result is not None

def get_user_data(user_id):
    """Get all user data"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    
    cursor.execute('''
        SELECT name, age, health_conditions, daily_goal
        FROM users WHERE id = ?
    ''', (user_id,))
    user_row = cursor.fetchone()
    
   
    cursor.execute('''
        SELECT today_intake, streak, total_sips, weekly_data, last_date, history
        FROM water_data WHERE user_id = ?
    ''', (user_id,))
    water_row = cursor.fetchone()
    
    
    cursor.execute('''
        SELECT notifications, reminder_interval
        FROM settings WHERE user_id = ?
    ''', (user_id,))
    settings_row = cursor.fetchone()
    
    conn.close()
    
    if user_row and water_row and settings_row:
        return {
            'user_data': {
                'name': user_row[0],
                'age': str(user_row[1]),
                'health_conditions': json.loads(user_row[2]),
                'daily_goal': user_row[3]
            },
            'water_data': {
                'today_intake': water_row[0],
                'streak': water_row[1],
                'total_sips': water_row[2],
                'weekly_data': json.loads(water_row[3]),
                'last_date': water_row[4],
                'history': json.loads(water_row[5])
            },
            'settings': {
                'notifications': bool(settings_row[0]),
                'reminder_interval': settings_row[1]
            }
        }
    return None

def update_water_data(user_id, water_data):
    """Update water data for user"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE water_data
        SET today_intake = ?, streak = ?, total_sips = ?, 
            weekly_data = ?, last_date = ?, history = ?
        WHERE user_id = ?
    ''', (
        water_data['today_intake'],
        water_data['streak'],
        water_data['total_sips'],
        json.dumps(water_data['weekly_data']),
        water_data['last_date'],
        json.dumps(water_data['history']),
        user_id
    ))
    
    conn.commit()
    conn.close()

def update_user_profile(user_id, name, age, daily_goal):
    """Update user profile"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users
        SET name = ?, age = ?, daily_goal = ?
        WHERE id = ?
    ''', (name, age, daily_goal, user_id))
    
    conn.commit()
    conn.close()

def update_settings(user_id, settings):
    """Update user settings"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE settings
        SET notifications = ?, reminder_interval = ?
        WHERE user_id = ?
    ''', (int(settings['notifications']), settings['reminder_interval'], user_id))
    
    conn.commit()
    conn.close()

def get_all_usernames():
    """Get list of all usernames (for user selection)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT username FROM users ORDER BY username')
    usernames = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return usernames
def reset_today_intake(user_id):
    """Reset only today's water intake for a given user"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE water_data
        SET today_intake = 0
        WHERE user_id = ?
    ''', (user_id,))

    conn.commit()
    conn.close()

init_database()


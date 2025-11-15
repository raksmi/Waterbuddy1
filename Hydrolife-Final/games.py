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

def database():
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
            water_goal INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS water_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER,
            water_intake INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            whole_sips INTEGER DEFAULT 0,
            weekly_hist TEXT,
            yesterday TEXT,
            data TEXT,
            FOREIGN KEY (id_user) REFERENCES users (id)
        )
    ''')
    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER,
            notification INTEGER DEFAULT 0,
            reminder_interval_user INTEGER DEFAULT 60,
            FOREIGN KEY (id_user) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def new_user(username, password, name, age, health_conditions, water_goal):
    """Create a new user account"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        hashed_pwd = hash_password(password)
        health_json = json.dumps(health_conditions)
        
        
        cursor.execute('''
            INSERT INTO users (username, password, name, age, health_conditions, water_goal)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, hashed_pwd, name, age, health_json, water_goal))
        
        id_user = cursor.lastrowid
        
        
        weekly_hist = json.dumps([
            {'day': 'Mon', 'water': 0},
            {'day': 'Tue', 'water': 0},
            {'day': 'Wed', 'water': 0},
            {'day': 'Thu', 'water': 0},
            {'day': 'Fri', 'water': 0},
            {'day': 'Sat', 'water': 0},
            {'day': 'Sun', 'water': 0},
        ])
        
        cursor.execute('''
            INSERT INTO water_data (id_user, weekly_hist, yesterday, data)
            VALUES (?, ?, ?, ?)
        ''', (id_user, weekly_hist, str(date.today()), '{}'))
        
        
        cursor.execute('''
            INSERT INTO settings (id_user)
            VALUES (?)
        ''', (id_user,))
        
        conn.commit()
        conn.close()
        return True, id_user
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

def get_userdata(id_user):
    """Get all user data"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    
    cursor.execute('''
        SELECT name, age, health_conditions, water_goal
        FROM users WHERE id = ?
    ''', (id_user,))
    userrow = cursor.fetchone()
    
   
    cursor.execute('''
        SELECT water_intake, streak, whole_sips, weekly_hist, yesterday, data
        FROM water_data WHERE id_user = ?
    ''', (id_user,))
    waterrow = cursor.fetchone()
    
    
    cursor.execute('''
        SELECT notification, reminder_interval_user
        FROM settings WHERE id_user = ?
    ''', (id_user,))
    settingsrow = cursor.fetchone()
    
    conn.close()
    
    if userrow and waterrow and settingsrow:
        return {
            'user_data': {
                'name': userrow[0],
                'age': str(userrow[1]),
                'health_conditions': json.loads(userrow[2]),
                'water_goal': userrow[3]
            },
            'water_data': {
                'water_intake': waterrow[0],
                'streak': waterrow[1],
                'whole_sips': waterrow[2],
                'weekly_hist': json.loads(waterrow[3]),
                'yesterday': waterrow[4],
                'data': json.loads(waterrow[5])
            },
            'settings': {
                'notification': bool(settingsrow[0]),
                'reminder_interval_user': settingsrow[1]
            }
        }
    return None

def update_water_intake(id_user, water_data):
    """Update water data for user"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE water_data
        SET water_intake = ?, streak = ?, whole_sips = ?, 
            weekly_hist = ?, yesterday = ?, data = ?
        WHERE id_user = ?
    ''', (
        water_data['water_intake'],
        water_data['streak'],
        water_data['whole_sips'],
        json.dumps(water_data['weekly_hist']),
        water_data['yesterday'],
        json.dumps(water_data['data']),
        id_user
    ))
    
    conn.commit()
    conn.close()

def update_water_settings(id_user, name, age, water_goal):
    """Update user profile"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users
        SET name = ?, age = ?, water_goal = ?
        WHERE id = ?
    ''', (name, age, water_goal, id_user))
    
    conn.commit()
    conn.close()

def update_remainder(id_user, settings):
    """Update user settings"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE settings
        SET notification = ?, reminder_interval_user = ?
        WHERE id_user = ?
    ''', (int(settings['notification']), settings['reminder_interval_user'], id_user))
    
    conn.commit()
    conn.close()

def get_all_user_name():
    """Get list of all user_name (for user selection)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT username FROM users ORDER BY username')
    user_name = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return user_name
def reset_water_intake(id_user):
    """Reset only today's water intake for a given user"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE water_data
        SET water_intake = 0
        WHERE id_user = ?
    ''', (id_user,))

    conn.commit()
    conn.close()

database()


"""
Games page - Snake game and Water quiz
"""

import streamlit as st
import random
import time
import asyncio
from streamlit.components.v1 import html

def show_games():
    """Games menu and games"""
    if 'game_mode' not in st.session_state:
        st.session_state.game_mode = 'menu'
    
    if st.session_state.game_mode == 'menu':
        show_games_menu()
    elif st.session_state.game_mode == 'snake':
        show_snake_game()
    elif st.session_state.game_mode == 'quiz':
        show_quiz()

def show_games_menu():
    """Games selection menu"""
    st.markdown('<h1 style="text-align: center; color: white;">Games & Fun</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 32px 0;">
            <div style="font-size: 80px; margin-bottom: 16px;">🎮</div>
            <h2 style="color: white;">Play & Learn</h2>
            <p style="color: rgba(255, 255, 255, 0.8);">Have fun while learning about hydration!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_game1, col_game2 = st.columns(2)
        
        with col_game1:
            st.markdown("""
            <div style="background: dark blue; padding: 32px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); text-align: center;">
                <div style="font-size: 48px; margin-bottom: 16px;">🐍</div>
                <h3>Snake Game</h3>
                <p style="color: sky blue; font-size: 14px; margin: 16px 0;">
                    Classic snake game with a hydration twist!
                </p>
                <div style="display: flex; gap: 8px; justify-content: center; margin: 16px 0;">
                    <span style="background: #d1fae5; color: #059669; padding: 4px 12px; border-radius: 12px; font-size: 12px;">Easy</span>
                    <span style="background: #dbeafe; color: #1e40af; padding: 4px 12px; border-radius: 12px; font-size: 12px;">Fun</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Play Now 🐍", use_container_width=True, type="primary"):
                st.session_state.game_mode = 'snake'
                initialize_snake_game()
                st.rerun()
        
        with col_game2:
            st.markdown("""
            <div style="background: dark blue; padding: 32px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); text-align: center;">
                <div style="font-size: 48px; margin-bottom: 16px;">🧠</div>
                <h3>Water Quiz</h3>
                <p style="color: sky blue; font-size: 14px; margin: 16px 0;">
                    Test your knowledge about hydration!
                </p>
                <div style="display: flex; gap: 8px; justify-content: center; margin: 16px 0;">
                    <span style="background: #e9d5ff; color: #7c3aed; padding: 4px 12px; border-radius: 12px; font-size: 12px;">Educational</span>
                    <span style="background: #dbeafe; color: #1e40af; padding: 4px 12px; border-radius: 12px; font-size: 12px;">5 Questions</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Start Quiz 🧠", use_container_width=True, type="primary"):
                st.session_state.game_mode = 'quiz'
                initialize_quiz()
                st.rerun()

def initialize_snake_game():
    """Initialize snake game state"""
    st.session_state.snake_board_size = 20
    st.session_state.snake_body = [(10, 10), (10, 9), (10, 8)]
    st.session_state.snake_direction = 'RIGHT'
    st.session_state.snake_food = generate_food()
    st.session_state.snake_score = 0
    st.session_state.snake_game_over = False
    st.session_state.snake_game_started = False
    st.session_state.snake_paused = False

def generate_food():
    """Generate random food position"""
    size = st.session_state.snake_board_size
    while True:
        food = (random.randint(0, size-1), random.randint(0, size-1))
        if food not in st.session_state.snake_body:
            return food

def show_snake_game():
    """Snake game with keyboard controls and continuous motion"""
    st.markdown('<h1 style="text-align: center; color: white;">Snake Game 🐍</h1>', unsafe_allow_html=True)
    
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div  style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); padding: 24px; border-bottom: 1px solid rgba(255, 255, 255, 0.2);padding: 20px; border-radius: 16px; margin-bottom: 20px; text-align: center;">
            <h4 style="margin: 0 0 10px 0;">🎮 Controls</h4>
            <p style="margin: 5px 0; font-size: 14px;">Use Arrow Keys: ⬆️ ⬇️ ⬅️ ➡️</p>
            <p style="margin: 5px 0; font-size: 14px;">Collect water drops 💧 to grow!</p>
            <p style="margin: 5px 0; font-size: 14px;">Press SPACE to pause/resume</p>
        </div>
        """, unsafe_allow_html=True)
        
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 15px; border-radius: 16px; margin-bottom: 20px; text-align: center;">
            <h3 style="margin: 0; color: white;">Score: {st.session_state.snake_score} 💧</h3>
            <p style="margin: 5px 0; color: rgba(255,255,255,0.8); font-size: 14px;">
                Length: {len(st.session_state.snake_body)}
            </p>
        </div>
        """, unsafe_allow_html=True)

    
    snake_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                font-family: Arial, sans-serif;
            }}
            #gameContainer {{
                text-align: center;
                background: white;
                padding: 20px;
                border-radius: 20px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            }}
            #gameCanvas {{
                border: 3px solid #333;
                border-radius: 10px;
                background: #000;
            }}
            #gameInfo {{
                margin: 15px 0;
                font-size: 18px;
                font-weight: bold;
            }}
            #gameStatus {{
                margin: 10px 0;
                font-size: 16px;
                color: #666;
            }}
            .btn {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 25px;
                font-size: 16px;
                cursor: pointer;
                margin: 5px;
                transition: transform 0.2s;
            }}
            .btn:hover {{
                transform: translateY(-2px);
            }}
            .game-over {{
                color: #dc2626;
                font-size: 24px;
                font-weight: bold;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div id="gameContainer">
            <canvas id="gameCanvas" width="600" height="590"></canvas>
            <div id="gameInfo">
                <div>Score: <span id="score">0</span> 💧 | Length: <span id="length">3</span></div>
            </div>
            <div id="gameStatus">Press SPACE to start/pause | Use Arrow Keys to move</div>
            <div id="gameOver" class="game-over" style="display: none;">
                Game Over! 💀<br>
                <button class="btn" onclick="restartGame()">🔄 Play Again</button>
                <button class="btn" onclick="backToMenu()">← Back to Games</button>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const scoreElement = document.getElementById('score');
            const lengthElement = document.getElementById('length');
            const gameOverElement = document.getElementById('gameOver');
            const gameStatusElement = document.getElementById('gameStatus');

            // Game settings
            const gridSize = 30;
            const tileCount = canvas.width / gridSize;

            let snake = [
                {{x: 10, y: 10}},
                {{x: 9, y: 10}},
                {{x: 8, y: 10}}
            ];
            let food = {{x: 15, y: 15}};
            let dx = 1;
            let dy = 0;
            let score = 0;
            let gameRunning = false;
            let gameOver = false;

            // Generate random food position
            function generateFood() {{
                food = {{
                    x: Math.floor(Math.random() * tileCount),
                    y: Math.floor(Math.random() * tileCount)
                }};
                
                // Make sure food doesn't spawn on snake
                for (let segment of snake) {{
                    if (segment.x === food.x && segment.y === food.y) {{
                        generateFood();
                        return;
                    }}
                }}
            }}

            // Draw game elements
            function drawGame() {{
                // Clear canvas
                ctx.fillStyle = '#000';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                // Draw snake
                ctx.fillStyle = '#10b981';
                for (let i = 0; i < snake.length; i++) {{
                    if (i === 0) {{
                        // Snake head
                        ctx.fillStyle = '#059669';
                        ctx.fillRect(snake[i].x * gridSize, snake[i].y * gridSize, gridSize-2, gridSize-2);
                        
                        // Draw eyes
                        ctx.fillStyle = '#fff';
                        ctx.fillRect(snake[i].x * gridSize + 8, snake[i].y * gridSize + 6, 4, 4);
                        ctx.fillRect(snake[i].x * gridSize + 18, snake[i].y * gridSize + 6, 4, 4);
                    }} else {{
                        // Snake body
                        ctx.fillStyle = '#10b981';
                        ctx.fillRect(snake[i].x * gridSize, snake[i].y * gridSize, gridSize-2, gridSize-2);
                    }}
                }}

                // Draw food (water drop)
                ctx.fillStyle = '#3b82f6';
                ctx.beginPath();
                ctx.arc(
                    food.x * gridSize + gridSize/2, 
                    food.y * gridSize + gridSize/2, 
                    gridSize/2 - 2, 
                    0, 
                    2 * Math.PI
                );
                ctx.fill();
                
                // Add water drop highlight
                ctx.fillStyle = '#60a5fa';
                ctx.beginPath();
                ctx.arc(
                    food.x * gridSize + gridSize/2 - 5, 
                    food.y * gridSize + gridSize/2 - 5, 
                    4, 
                    0, 
                    2 * Math.PI
                );
                ctx.fill();
            }}

            // Move snake
            function moveSnake() {{
                if (!gameRunning || gameOver) return;

                const head = {{x: snake[0].x + dx, y: snake[0].y + dy}};

                // Check wall collision
                if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {{
                    gameOver = true;
                    gameRunning = false;
                    showGameOver();
                    return;
                }}

                // Check self collision
                for (let segment of snake) {{
                    if (head.x === segment.x && head.y === segment.y) {{
                        gameOver = true;
                        gameRunning = false;
                        showGameOver();
                        return;
                    }}
                }}

                snake.unshift(head);

                // Check food collision
                if (head.x === food.x && head.y === food.y) {{
                    score += 10;
                    scoreElement.textContent = score;
                    lengthElement.textContent = snake.length;
                    generateFood();
                }} else {{
                    snake.pop();
                }}

                drawGame();
            }}

            // Show game over screen
            function showGameOver() {{
                gameOverElement.style.display = 'block';
                gameStatusElement.textContent = `Final Score: ${{score}} 💧`;
            }}

            // Restart game
            function restartGame() {{
                snake = [
                    {{x: 10, y: 10}},
                    {{x: 9, y: 10}},
                    {{x: 8, y: 10}}
                ];
                dx = 1;
                dy = 0;
                score = 0;
                gameOver = false;
                gameRunning = true;
                scoreElement.textContent = score;
                lengthElement.textContent = snake.length;
                gameOverElement.style.display = 'none';
                gameStatusElement.textContent = 'Game Running - Use Arrow Keys | SPACE to pause';
                generateFood();
                drawGame();
            }}

            // Back to menu
            function backToMenu() {{
                window.parent.postMessage({{type: 'backToMenu'}}, '*');
            }}

            // Keyboard controls
            document.addEventListener('keydown', (e) => {{
                if (gameOver) return;

                switch(e.key) {{
                    case 'ArrowUp':
                        if (dy !== 1) {{ dx = 0; dy = -1; }}
                        break;
                    case 'ArrowDown':
                        if (dy !== -1) {{ dx = 0; dy = 1; }}
                        break;
                    case 'ArrowLeft':
                        if (dx !== 1) {{ dx = -1; dy = 0; }}
                        break;
                    case 'ArrowRight':
                        if (dx !== -1) {{ dx = 1; dy = 0; }}
                        break;
                    case ' ':
                        e.preventDefault();
                        if (!gameOver) {{
                            gameRunning = !gameRunning;
                            gameStatusElement.textContent = gameRunning ? 
                                'Game Running - Use Arrow Keys | SPACE to pause' : 
                                'Game Paused - Press SPACE to resume';
                        }}
                        break;
                }}
            }});

            // Game loop
            function gameLoop() {{
                moveSnake();
                setTimeout(gameLoop, 150); // Game speed
            }}

            // Initialize game
            generateFood();
            drawGame();
            gameLoop();

            // Focus canvas for keyboard input
            canvas.focus();
            canvas.tabIndex = 1;
        </script>
    </body>
    </html>
    """

    
    html(snake_html, height=800)

    
    if st.button("← Back to Games", key="back_to_games"):
        st.session_state.game_mode = 'menu'
        st.rerun()

def initialize_quiz():
    """Initialize quiz with random questions"""
    all_questions = [
        {
            "question": "What percentage of the human body is water?",
            "options": ["50%", "60%", "70%", "80%"],
            "correct": 1,
            "explanation": "About 60% of the human body is water!"
        },
        {
            "question": "How many glasses should an adult drink daily?",
            "options": ["4-6", "8-10", "12-14", "2-4"],
            "correct": 1,
            "explanation": "8-10 glasses (2-2.5L) per day is recommended."
        },
        {
            "question": "Which organ contains the most water?",
            "options": ["Heart", "Lungs", "Brain", "Liver"],
            "correct": 2,
            "explanation": "The brain is about 75% water!"
        },
        {
            "question": "Best time to drink water?",
            "options": ["Only when thirsty", "Throughout the day", "Only with meals", "Only morning"],
            "correct": 1,
            "explanation": "Drink consistently throughout the day."
        },
        {
            "question": "Which is a sign of dehydration?",
            "options": ["Dry skin", "Dark urine", "Fatigue", "All of the above"],
            "correct": 3,
            "explanation": "All are common signs of dehydration."
        },
        {
            "question": "How long can humans survive without water?",
            "options": ["1-2 days", "3-5 days", "1 week", "2 weeks"],
            "correct": 1,
            "explanation": "Humans can typically survive only 3-5 days without water."
        },
        {
            "question": "Which drink is best for hydration?",
            "options": ["Coffee", "Soda", "Water", "Energy drinks"],
            "correct": 2,
            "explanation": "Plain water is the best choice for hydration."
        },
        {
            "question": "What color should healthy urine be?",
            "options": ["Dark yellow", "Light yellow", "Clear", "Orange"],
            "correct": 1,
            "explanation": "Light yellow indicates good hydration levels."
        },
        {
            "question": "Which activity increases water needs?",
            "options": ["Reading", "Exercise", "Sleeping", "Watching TV"],
            "correct": 1,
            "explanation": "Exercise increases fluid loss through sweat."
        },
        {
            "question": "What happens when you're dehydrated?",
            "options": ["Better focus", "Increased energy", "Reduced performance", "Better mood"],
            "correct": 2,
            "explanation": "Dehydration reduces both physical and mental performance."
        },
        {
        "question": "What is the main function of water in the body?",
        "options": ["Provide energy", "Carry nutrients", "Build muscles", "Store fat"],
        "correct": 1,
        "explanation": "Water helps transport nutrients and oxygen to cells."
    },
    {
        "question": "Which of these contains the most water naturally?",
        "options": ["Apple", "Cucumber", "Banana", "Bread"],
        "correct": 1,
        "explanation": "Cucumbers are about 95% water!"
    },
    {
        "question": "How does drinking water help your skin?",
        "options": ["Makes it dry", "Makes it glow", "Causes wrinkles", "Has no effect"],
        "correct": 1,
        "explanation": "Staying hydrated keeps skin soft, glowing, and healthy."
    },
    {
        "question": "What happens if you drink too much water too quickly?",
        "options": ["Improves focus", "Water intoxication", "Better sleep", "Nothing"],
        "correct": 1,
        "explanation": "Drinking excessive water can cause water intoxication (hyponatremia)."
    },
    {
        "question": "Which of these drinks causes dehydration?",
        "options": ["Juice", "Tea", "Alcohol", "Smoothie"],
        "correct": 2,
        "explanation": "Alcohol increases water loss and can lead to dehydration."
    },
    {
        "question": "Why is water important for digestion?",
        "options": ["Helps break down food", "Cools the stomach", "Creates acids", "Stops hunger"],
        "correct": 0,
        "explanation": "Water helps dissolve nutrients and move food through the digestive tract."
    },
    {
        "question": "How much of the Earth’s surface is covered by water?",
        "options": ["50%", "60%", "70%", "80%"],
        "correct": 2,
        "explanation": "Around 70% of Earth's surface is covered with water!"
    },
    {
        "question": "Which of these contains the least water?",
        "options": ["Fat tissue", "Muscle tissue", "Brain", "Liver"],
        "correct": 0,
        "explanation": "Fat tissue contains less water compared to muscles or organs."
    },
    {
        "question": "What does water help regulate in the body?",
        "options": ["Heart rate", "Body temperature", "Height", "Hair growth"],
        "correct": 1,
        "explanation": "Water helps maintain normal body temperature through sweating."
    },
    {
        "question": "When should you drink extra water?",
        "options": ["In cold weather", "During fever or exercise", "After sleeping", "Before eating"],
        "correct": 1,
        "explanation": "During fever or exercise, the body loses more fluids — extra water is essential."
    }
    ]
    
    
    st.session_state.quiz_questions = random.sample(all_questions, 5)
    st.session_state.quiz_question = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_answered = False
    st.session_state.quiz_complete = False

def show_quiz():
    """Water knowledge quiz with random questions"""
    if st.session_state.quiz_complete:
        st.markdown('<h1 style="text-align: center; color: black;">Quiz Complete!</h1>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            score = st.session_state.quiz_score
            total = len(st.session_state.quiz_questions)
            percentage = (score / total) * 100
            emoji = "🏆" if percentage >= 80 else "🎉" if percentage >= 60 else "💪"
            
            st.markdown(f"""
            <div style="background: white; padding: 40px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); text-align: center;">
                <div style="font-size: 80px; margin-bottom: 24px;">{emoji}</div>
                <h2 style="color:black;">Quiz Complete!</h2>
                <div style="font-size: 60px; color: #667eea; font-weight: 700; margin: 24px 0;">{score}/{total}</div>
                <p style="color: #666;">
                    {
                        "Excellent! You're a hydration expert! 🌟" if percentage >= 80
                        else "Great job! Keep learning! 💧" if percentage >= 60
                        else "Good effort! Try again! 📚"
                    }
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_retry, col_menu = st.columns(2)
            with col_retry:
                if st.button("🔄 Try Again", use_container_width=True, type="primary"):
                    initialize_quiz()
                    st.rerun()
            with col_menu:
                if st.button("← Back to Games", use_container_width=True):
                    st.session_state.game_mode = 'menu'
                    st.session_state.quiz_complete = False
                    st.rerun()
    else:
        st.markdown('<h1 style="text-align: center; color: white;">Water Quiz 🧠</h1>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            current_q = st.session_state.quiz_question
            question_data = st.session_state.quiz_questions[current_q]
            
            st.markdown(f"""
            <div style="background: white; padding: 24px; border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #666; font-size: 14px;">Question {current_q + 1} of {len(st.session_state.quiz_questions)}</span>
                    <span style="color: #667eea; font-size: 14px;">Score: {st.session_state.quiz_score}/{len(st.session_state.quiz_questions)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: black; padding: 32px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">
                <h3 style="text-align: center; margin-bottom: 24px; color: white;">{question_data['question']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if not st.session_state.quiz_answered:
                for i, option in enumerate(question_data['options']):
                    if st.button(option, use_container_width=True, key=f"opt_{i}"):
                        st.session_state.quiz_answered = True
                        st.session_state.selected_answer = i
                        if i == question_data['correct']:
                            st.session_state.quiz_score += 1
                        st.rerun()
            else:
                for i, option in enumerate(question_data['options']):
                    is_correct = i == question_data['correct']
                    is_selected = i == st.session_state.selected_answer
                    
                    if is_correct:
                        st.success(f"✓ {option}")
                    elif is_selected and not is_correct:
                        st.error(f"✗ {option}")
                    else:
                        st.info(option)
                
                st.markdown(f"""
                <div style="background: #dbeafe; padding: 16px; border-radius: 12px; margin: 16px 0;">
                    <p style="color: #1e40af; margin: 0;">{question_data['explanation']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if current_q < len(st.session_state.quiz_questions) - 1:
                    if st.button("Next Question ", use_container_width=True, type="primary"):
                        st.session_state.quiz_question += 1
                        st.session_state.quiz_answered = False
                        st.rerun()
                else:
                    if st.button("Results", use_container_width=True, type="primary"):
                        st.session_state.quiz_complete = True
                        st.rerun()


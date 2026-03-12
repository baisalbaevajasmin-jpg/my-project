from flask import Flask, render_template, request, jsonify
import re
import random
import string

app = Flask(__name__)

# Құпия сөзді тексеру алгоритмі
def check_password(password):
    score = 0
    if len(password) >= 8: score += 1
    if re.search("[a-z]", password) and re.search("[A-Z]", password): score += 1
    if re.search("[0-9]", password): score += 1
    if re.search("[!@#$%^&*]", password): score += 1
    
    if score <= 2: return "Әлсіз", "#ff4d4d"
    elif score == 3: return "Орташа", "#ffbd44"
    else: return "Өте жақсы", "#00ff00"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    pwd = data.get('password', '')
    url = data.get('url', '')
    
    p_status, p_color = check_password(pwd)
    
    # Фишинг сілтемелерді қарапайым тексеру
    suspicious_words = ["login", "bank", "free", "gift", "verify", "update"]
    u_status, u_color = "Қауіпсіз көрінеді", "#00ff00"
    if any(word in url.lower() for word in suspicious_words) or "@" in url:
        u_status, u_color = "Күмәнді сілтеме!", "#ff4d4d"
        
    return jsonify({
        'pwd_status': p_status, 'pwd_color': p_color,
        'url_status': u_status, 'url_color': u_color
    })

@app.route('/generate_password', methods=['POST'])
def generate_password():
    # Мықты құпия сөз жасау (14 таңбалы)
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    secure_pwd = ''.join(random.choice(chars) for _ in range(14))
    return jsonify({'password': secure_pwd})

if __name__ == '__main__':
    # Портты 5001 қылдық, 5000 бос болмаса кедергі жасамайды
    app.run(debug=True, port=5001)

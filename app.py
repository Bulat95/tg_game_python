from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from pathlib import Path

app = Flask(__name__, static_folder='static', template_folder='templates')

# Конфигурация
PRISONER_NAME = "Иван"
DATA_DIR = Path("data/users")
PROMPT_PATH = Path("prompts/promptforai.txt")

# Создаем необходимые директории
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs("prompts", exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/api/start', methods=['POST'])
def start_game():
    data = request.json
    detective_name = data.get('detective_name', '').strip()

    if not detective_name:
        return jsonify({"error": "Введите имя!"}), 400

    # Здесь можно добавить логику загрузки предыдущего чата
    return jsonify({
        "prisoner_name": PRISONER_NAME,
        "initial_messages": [
            f"Добро пожаловать в тюрьму, {detective_name}!",
            "Ваша задача - расколоть убийцу. Удачи!",
            f"К вам приходит заключенный по имени {PRISONER_NAME}."
        ]
    })


@app.route('/api/send', methods=['POST'])
def send_message():
    data = request.json
    user_input = data.get('message', '').strip()
    chat_history = data.get('chat_history', '')
    detective_name = data.get('detective_name', 'Детектив')

    if not user_input:
        return jsonify({"error": "Пожалуйста, введите сообщение!"}), 400

    # Здесь будет интеграция с Google Gemini API
    # Пока используем заглушку
    response = f"{PRISONER_NAME}: *нервно почесывает шею* Я не виновен, детектив {detective_name}!"

    return jsonify({
        "response": response,
        "updated_history": f"{chat_history}\n{detective_name}: {user_input}\n{response}"
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
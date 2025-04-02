from flask import Flask, request, send_file
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return send_file('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '')

    # Читаем HTML шаблон
    with open('index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Заменяем плейсхолдер на введенное имя
    if '<!-- NAME_PLACEHOLDER -->' in html_content:
        result_html = html_content.replace('<!-- NAME_PLACEHOLDER -->', f'''
        <div class="result">
            <h2>Привет, {name}!</h2>
            <p>Спасибо, что посетили наш сайт.</p>
        </div>
        ''')
    else:
        result_html = html_content

    # Создаем временный файл с результатом
    with open('temp_result.html', 'w', encoding='utf-8') as file:
        file.write(result_html)

    return send_file('temp_result.html')


if __name__ == '__main__':
    app.run(debug=True)
    # Удаляем временный файл при завершении
    if os.path.exists('temp_result.html'):
        os.remove('temp_result.html')
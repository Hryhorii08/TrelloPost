import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔹 ДАННЫЕ TRELLO (замени на свои)
TRELLO_API_KEY = "5880197335c3d727693408202c68375d"
TRELLO_TOKEN = "ATTA1ea4c6edf0b2892fec32580ab1417a42f521cd70c11af1453ddd0a4956e72896C175BE4E"
TRELLO_LIST_ID = "67c19cd6641117e44ae95227"

# 🔹 ДАННЫЕ TELEGRAM (замени на свои)
TELEGRAM_BOT_TOKEN = "7788946008:AAGULYh-GIkpr-GA3ZA70ERdCAT6BcGNW-g"
TELEGRAM_CHAT_ID = "-1002307069728"

# 🔹 Функция отправки заявки в Trello
def create_trello_card(name, course, age, city):
    url = "https://api.trello.com/1/cards"
    query = {
        "name": f"Заявка от {name}",
        "desc": f"Курс: {course}\nВозраст: {age}\nГород: {city}",
        "idList": TRELLO_LIST_ID,
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN
    }
    response = requests.post(url, params=query)
    return response.status_code, response.json()

# 🔹 Функция отправки заявки в Telegram
def send_to_telegram(name, course, age, city):
    message = f"📌 *Новая заявка:*\n👤 Имя: {name}\n📚 Курс: {course}\n🎂 Возраст: {age}\n🌍 Город: {city}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=data)
    return response.status_code, response.json()

# 🔹 API-эндпоинт для обработки заявки
@app.route("/send_to_trello", methods=["POST"])
def send_to_trello():
    data = request.json
    name = data.get("name")
    course = data.get("course")
    age = data.get("age")
    city = data.get("city")

    if not all([name, course, age, city]):
        return jsonify({"error": "Не все данные заполнены"}), 400

    # Отправка в Trello
    trello_status, trello_response = create_trello_card(name, course, age, city)

    # Отправка в Telegram
    tg_status, tg_response = send_to_telegram(name, course, age, city)

    if trello_status == 200 and tg_status == 200:
        return jsonify({"message": "Заявка успешно отправлена в Trello и Telegram"})
    else:
        return jsonify({
            "error": "Ошибка при обработке заявки",
            "trello_status": trello_status,
            "trello_response": trello_response,
            "telegram_status": tg_status,
            "telegram_response": tg_response
        }), 500

# 🔹 Запуск сервера
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

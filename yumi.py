import telebot
import requests
import time
import random

TELEGRAM_TOKEN = '6994434259:AAHfg9ddIPR06tW9hIL7Woh21ffugusoJMw'
COHERE_API_KEY = 'Zoy1VWuyCwmh8dMJnhruyaEpC9lNrrk5joWcZsx6'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

COHERE_URL = "https://api.cohere.ai/v1/generate"
HEADERS = {
    "Authorization": f"Bearer {COHERE_API_KEY}",
    "Content-Type": "application/json"
}

# Мур-мур фразы для поднятия настроения (русский и английский)
FUN_PHRASES_RU = [
    "😺 Мррр... слушай, что я тебе мурлычу: ",
    "🐾 Лапками печатаю... держись! ",
    "😽 Мяу! Вот мой ответ, прямо из сердечка: ",
    "😻 Пушистый совет для тебя: ",
    "🐱 Хвостик вверх, а вот и ответ: "
]

FUN_PHRASES_EN = [
    "😺 Purr... listen to what I’m purring for you: ",
    "🐾 Typing with paws... hold tight! ",
    "😽 Meow! Here’s my answer, straight from my heart: ",
    "😻 A fluffy advice for you: ",
    "🐱 Tail up, here comes the answer: "
]

# Котоприветствия (русский и английский)
GREETINGS_RU = [
    "Привет-привет! Я Юми — твой пушистый помощник с лапками и хвостиком! 🐾😸",
    "Мяу! Напиши мне что-нибудь, и я сотворю для тебя сказку с кошачьим настроением! 🐱✨",
    "Хэллоу! Готова играть и веселиться? Пиши — и я отвечу с мурчанием и улыбкой! 😻"
]

GREETINGS_EN = [
    "Hi there! I'm Yumi — your fluffy helper with paws and tail! 🐾😸",
    "Meow! Write me something, and I’ll spin you a tale with kitty vibes! 🐱✨",
    "Hello! Ready to play and have fun? Write to me — I’ll answer with purrs and smiles! 😻"
]

def generate_response(prompt):
    data = {
        "model": "command",
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.8,
        "stop_sequences": ["--"]
    }
    try:
        response = requests.post(COHERE_URL, headers=HEADERS, json=data, timeout=10)
        print("Response status code:", response.status_code)
        print("Response content:", response.content)
        response.raise_for_status()
        response_json = response.json()
        text = response_json['generations'][0]['text'].strip()

        # Если сервер грустит, заменим ответ на что-то милое
        if "лапки" in text.lower() or "try later" in text.lower():
            return "😿 Ой, лапки у меня устали, давай передохнём и попробуем чуть позже? 🐾"

        # По умолчанию считаем русский — выбираем русские весёлые фразы
        # Можно потом добавить анализ языка пользователя для автоматического выбора
        return random.choice(FUN_PHRASES_RU) + text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content}")
        return "😿 Упс, лапки у меня запутались — сейчас не могу ответить, попробуй через минутку! 🐾"
    except Exception as e:
        print("Ошибка при запросе к Cohere:", e)
        return "😿 Мяу! Что-то пошло не так, но я уже пытаюсь всё поправить. Попробуй ещё раз через минутку! 🐱"

@bot.message_handler(commands=['start'])
def start_handler(message):
    # Приветствие на русском (можно расширить на другие языки)
    greeting = random.choice(GREETINGS_RU)
    bot.send_message(message.chat.id, greeting)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text.strip()
    if not user_text:
        bot.send_message(message.chat.id, "😽 Мяу! Пусто же, напиши что-нибудь, пожалуйста! 🐾")
        return

    bot.send_chat_action(message.chat.id, 'typing')
    reply = generate_response(user_text)
    bot.send_message(message.chat.id, reply)

def run_bot():
    print("Юми запускается... 🐱")
    while True:
        try:
            bot.polling(non_stop=True, timeout=20)
        except Exception as e:
            print(f"Ой, Юми устала, перезапускаюсь... Ошибка: {e}")
            time.sleep(5)

if __name__ == '__main__':
    run_bot()
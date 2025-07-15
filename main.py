from keep_alive import keep_alive
import telebot
import os

bot = telebot.TeleBot(os.environ['TOKEN'])
ADMIN_CHAT_ID = os.environ['CHAT_ID']
PAYPAL_EMAIL = os.environ['PAYPAL_EMAIL']

keep_alive()

# Мультиязычные сообщения
messages = {
    "start": {
        "ru": "Привет! Мы предлагаем:\n\n📝 Перевод писем — 3 €\n📄 Написание резюме — 5 €\n\nОтправь текст или фото, затем оплати — и мы начнём.",
        "en": "Hi! We offer:\n\n📝 Letter translation – €3\n📄 CV writing – €5\n\nSend your text or image, then pay — and we’ll begin.",
        "de": "Hallo! Unsere Dienste:\n\n📝 Briefübersetzung – 3 €\n📄 Lebenslauf schreiben – 5 €\n\nSende Text oder Bild und bezahle, dann legen wir los."
    },
    "payment": {
        "ru": "💳 Оплата через PayPal:\nПисьмо: 3 €\nРезюме: 5 €\nhttps://www.paypal.me/{email}",
        "en": "💳 Pay via PayPal:\nLetter: €3\nCV: €5\nhttps://www.paypal.me/{email}",
        "de": "💳 Zahlung via PayPal:\nBrief: 3 €\nLebenslauf: 5 €\nhttps://www.paypal.me/{email}"
    },
    "thankyou": {
        "ru": "Спасибо! Мы получили сообщение. Пожалуйста, оплатите и мы начнём.",
        "en": "Thanks! We received your message. Please proceed with payment.",
        "de": "Danke! Wir haben deine Nachricht erhalten. Bitte bezahle jetzt."
    }
}

def get_lang(text):
    text = text.lower()
    if any(w in text for w in ['hi', 'hello', 'please', 'pay', 'cv']):
        return 'en'
    elif any(w in text for w in ['hallo', 'bitte', 'bezahlen', 'lebenslauf']):
        return 'de'
    return 'ru'

@bot.message_handler(commands=['start'])
def start(message):
    lang = get_lang(message.text)
    bot.reply_to(message, messages['start'][lang])

@bot.message_handler(content_types=['text', 'photo', 'document'])
def handle_message(message):
    lang = get_lang(message.text or message.caption or "")

    # Пересылка админу
    if message.content_type == 'text':
        bot.send_message(ADMIN_CHAT_ID, f"📩 Новое сообщение:\n\n{message.text}")
    elif message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        bot.send_photo(ADMIN_CHAT_ID, file_id, caption=message.caption or "")
    elif message.content_type == 'document':
        file_id = message.document.file_id
        bot.send_document(ADMIN_CHAT_ID, file_id, caption=message.caption or "")

    # Ответ пользователю
    bot.reply_to(message, messages['thankyou'][lang])
    bot.send_message(message.chat.id, messages['payment'][lang].format(email=PAYPAL_EMAIL))

bot.infinity_polling()

import telebot
import os
import sqlite3
from telebot import types

# Отримання токену бота з змінної середовища
TOKEN = os.environ.get('TOKEN')

# Перевірка, чи токен бота існує
if not TOKEN:
    raise ValueError('Не вдалося знайти токен бота. Переконайтесь, що ви встановили змінну середовища BOT_TOKEN з коректним токеном бота.')

# Ініціалізація бота
bot = telebot.TeleBot(TOKEN)

# Підключення до бази даних SQLite
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Створення таблиці для збереження витрат, якщо вона не існує
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   name TEXT,
                   amount REAL,
                   category TEXT,
                   description TEXT)''')
conn.commit()

# Список доступних імен
names = ['Наташа', 'Саша', 'Мирослав', 'Валентина', 'Яна']

# Обробник команди /start
@bot.message_handler(commands=['start'])
def start(message):
    # Створення меню з кнопками
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton('Додати витрати')
    button2 = types.KeyboardButton('Статистика')
    button3 = types.KeyboardButton('Допомога')
    markup.add(button1, button2, button3)

    bot.reply_to(message, 'Вітаю! Ви підключилися до бота.', reply_markup=markup)

# Обробник натискання на кнопку "Додати витрати"
@bot.message_handler(func=lambda message: message.text == 'Додати витрати')
def add_expenses(message):
    # Створення меню для вибору імен
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(name) for name in names]
    markup.add(*buttons)

    msg = bot.reply_to(message, 'Виберіть ім\'я:', reply_markup=markup)
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    name = message.text
    if name in names:
        bot.reply_to(message, f'Ви обрали ім\'я: {name}')
        msg = bot.reply_to(message, 'Введіть суму витрат:')
        bot.register_next_step_handler(msg, process_amount_step, name)
    else:
        bot.reply_to(message, 'Будь ласка, виберіть ім\'я зі списку доступних імен.')

def process_amount_step(message, name):
    amount = message.text
    # Перевірка, чи введено числове значення
    try:
        amount = float(amount.replace(',', '.'))
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        yes_button = types.KeyboardButton('Так')
        no_button = types.KeyboardButton('Ні')
        markup.add(yes_button, no_button)
        msg = bot.reply_to(message, f'Ви ввели суму: {amount}. Ви впевнені, що ввели правильну суму?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_confirmation_step, name, amount)
    except ValueError:
        bot.reply_to(message, 'Будь ласка, введіть числове значення суми витрат.')

def process_confirmation_step(message, name, amount):
    confirmation = message.text
    if confirmation == 'Так':
        # Отримання категорій із бази даних або з відповідного джерела
        categories = ['Їжа', 'Гігієна', 'Транспорт', 'Розваги', 'Інше']
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons = [types.KeyboardButton(category) for category in categories]
        markup.add(*buttons)

        msg = bot.reply_to(message, 'Оберіть категорію:', reply_markup=markup)
        bot.register_next_step_handler(msg, process_category_step, name, amount)
    elif confirmation == 'Ні':
        msg = bot.reply_to(message, 'Будь ласка, введіть суму витрат:')
        bot.register_next_step_handler(msg, process_amount_step, name)
    else:
        bot.reply_to(message, 'Будь ласка, виберіть один з варіантів відповіді.')

def process_category_step(message, name, amount):
    category = message.text
    # Отримання опису витрат від користувача
    msg = bot.reply_to(message, 'Введіть опис витрат:')
    bot.register_next_step_handler(msg, process_description_step, name, amount, category)

def process_description_step(message, name, amount, category):
    description = message.text
    # Збереження витрат у базі даних
    cursor.execute("INSERT INTO expenses (user_id, name, amount, category, description) VALUES (?, ?, ?, ?, ?)",
                   (message.from_user.id, name, amount, category, description))
    conn.commit()

    # Виведення повідомлення з деталями витрат
    bot.reply_to(message, f'Витрати успішно збережено:\nІм\'я: {name}\nСума: {amount}\nКатегорія: {category}\nОпис: {description}')

# Запуск бота
if __name__ == '__main__':
    bot.polling()

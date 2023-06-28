import telebot
import os
from telebot import types
from database import Database, Expense

TOKEN = os.environ.get('TOKEN')

if not TOKEN:
    raise ValueError(
        'Не вдалося знайти токен бота. Переконайтесь, що ви встановили змінну середовища BOT_TOKEN з коректним токеном бота.')

bot = telebot.TeleBot(TOKEN)
db = Database()
names = ['Наташа', 'Саша', 'Мирослав', 'Валентина', 'Яна']


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton('Додати витрати')
    button2 = types.KeyboardButton('Статистика')
    button3 = types.KeyboardButton('Допомога')
    markup.add(button1, button2, button3)

    bot.reply_to(message, 'Вітаю! Ви підключилися до бота.',
                 reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Додати витрати')
def add_expenses(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(name) for name in names]
    markup.add(*buttons)

    msg = bot.reply_to(message, 'Виберіть ім\'я:', reply_markup=markup)
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    global name
    name = message.text
    if name in names:
        bot.reply_to(message, f'Ви обрали ім\'я: {name}')
        msg = bot.reply_to(message, 'Введіть суму витрат:')
        bot.register_next_step_handler(msg, process_amount_step)
    else:
        bot.reply_to(
            message, 'Будь ласка, виберіть ім\'я зі списку доступних імен.')


def process_amount_step(message):
    try:
        amount = float(message.text.replace(',', '.'))
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        yes_button = types.KeyboardButton('Так')
        no_button = types.KeyboardButton('Ні')
        markup.add(yes_button, no_button)
        msg = bot.reply_to(message, 'Ви впевнені?', reply_markup=markup)
        bot.register_next_step_handler(
            msg, process_first_confirmation_step, amount)
    except ValueError:
        msg = bot.reply_to(
            message, 'Сума повинна бути числом. Будь ласка, введіть суму ще раз.')
        bot.register_next_step_handler(msg, process_amount_step)


def process_first_confirmation_step(message, amount):
    confirmation = message.text
    if confirmation == 'Так':
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        general_button = types.KeyboardButton('General')
        food_button = types.KeyboardButton('Food')
        markup.add(general_button, food_button)
        msg = bot.reply_to(message, 'Виберіть категорію:', reply_markup=markup)
        bot.register_next_step_handler(msg, process_category_step, amount)
    else:
        msg = bot.reply_to(message, 'Будь ласка, введіть суму витрат ще раз.')
        bot.register_next_step_handler(msg, process_amount_step)


def process_category_step(message, amount):
    global category
    category = message.text
    bot.reply_to(message, f'Ви обрали категорію: {category}')
    msg = bot.reply_to(message, 'Введіть опис витрат:')
    bot.register_next_step_handler(
        msg, process_description_step, message.from_user.id, name, amount, category)


def process_description_step(message, user_id, name, amount, category):
    description = message.text
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    yes_button = types.KeyboardButton('Так')
    no_button = types.KeyboardButton('Ні')
    markup.add(yes_button, no_button)
    msg = bot.send_message(
        message.chat.id, f"Ім'я: {name}\nСума: {amount}\nКатегорія: {category}\nОпис: {description}\nВсе вірно?", reply_markup=markup)
    bot.register_next_step_handler(
        msg, process_final_confirmation_step, user_id, name, amount, category, description)


def process_final_confirmation_step(message, user_id, name, amount, category, description):
    if message.text.lower() == 'так':
        expense = Expense(user_id, name, amount, category, description)
        db.add_expense(expense)
        bot.send_message(message.chat.id, 'Витрати успішно додано!')
    else:
        bot.send_message(
            message.chat.id, 'Введення відмінено. Спробуйте знову.')
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('Додати витрати')
    button2 = types.KeyboardButton('Статистика')
    button3 = types.KeyboardButton('Допомога')
    markup.add(button1, button2, button3)
    msg = bot.send_message(
        message.chat.id, 'Чи хочете ви щось ще зробити?', reply_markup=markup)
    bot.register_next_step_handler(msg, start)


bot.infinity_polling()

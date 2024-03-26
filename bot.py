import telebot
import bot_utilites
from telebot import types

token = 'YOUR_TOKEN'

bot = telebot.TeleBot(token, parse_mode='markdown')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id,
                     text=f'Привет, {name}! Я телеграм-бот, который предоставляет данные из FakeStoreAPI 😊 \n\n'
                          'Нажмите /help чтобы увидеть все команды')


@bot.message_handler(commands=['help'])
def show_commands(message):
    bot.send_message(message.chat.id, text='''
Список всех комманд:
Получить все товары: /products
Получить все категории: /categories
Посмотреть корзину: /bin''')


@bot.message_handler(commands=['products'])
def send_products(message):
    products = bot_utilites.get_all_products()
    bot.send_message(message.chat.id,
                     text=f'''{products}
Чтобы выбрать товар нажмите /choose и напишите ID товара
Чтобы вернуться в главное меню нажмите /help''')


@bot.message_handler(commands=['categories'])
def send_categories(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='electronics', callback_data='category1')
    btn2 = types.InlineKeyboardButton(text='jewelery', callback_data='category2')
    btn3 = types.InlineKeyboardButton(text="men's clothing", callback_data='category3')
    btn4 = types.InlineKeyboardButton(text="women's clothing", callback_data='category4')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, text="Выберите категорию: ", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def message_reply(call):
    if call:
        if call.data == "category1":
            bot.send_message(call.message.chat.id, text=f'''{bot_utilites.get_product_in_category('electronics')}
Чтобы выбрать товар нажмите /choose и напишите ID товара
Чтобы вернуться в главное меню нажмите /help''')
        elif call.data == "category2":
            bot.send_message(call.message.chat.id, text=f'''{bot_utilites.get_product_in_category('jewelery')}
Чтобы выбрать товар нажмите /choose и напишите ID товара
Чтобы вернуться в главное меню нажмите /help''')
        elif call.data == "category3":
            bot.send_message(call.message.chat.id, text=f'''{bot_utilites.get_product_in_category("men's clothing")}
Чтобы выбрать товар нажмите /choose и напишите ID товара
Чтобы вернуться в главное меню нажмите /help''')
        elif call.data == "category4":
            bot.send_message(call.message.chat.id, text=f'''{bot_utilites.get_product_in_category("women's clothing")}
Чтобы выбрать товар нажмите /choose и напишите ID товара
Чтобы вернуться в главное меню нажмите /help''')


@bot.message_handler(commands=['bin'])
def show_bin(message):
    bot_utilites.create_table()
    if bot_utilites.is_empty(message.chat.id):
        text = '''
Корзина пустая!

Чтобы вернуться в главное меню нажмите /help'''
    else:
        text = f'''{bot_utilites.show_table(message.chat.id)}
Чтобы удалить товар из корзины нажмите /delete
Чтобы очистить корзину нажмите /clear
Чтобы вернуться в главное меню нажмите /help'''
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=['choose'])
def choose_product(message):
    bot.send_message(message.from_user.id, "Введите ID товара: ")
    bot.register_next_step_handler(message, save_product_in_db)
    return ''


def save_product_in_db(message):
    text = message.text
    bot_utilites.create_table()
    if 0 < int(message.text) <= 20:
        if bot_utilites.is_exist(message.text, message.chat.id):
            bot.send_message(message.chat.id, text='''
Товар уже в корзине!

Чтобы посмотреть корзину нажмите /bin
Чтобы вернуться в главное меню нажмите /help''')
        else:
            bot_utilites.save_product_to_db(text, message.chat.id)
            bot.send_message(message.chat.id, text='''
Товар успешно добавлен в корзину!

Чтобы посмотреть корзину нажмите /bin
Чтобы вернуться в главное меню нажмите /help''')
    else:
        bot.send_message(message.from_user.id, f'''
Введите число от 1 до 20
{choose_product(message)}''')


@bot.message_handler(commands=['delete'])
def delete_product(message):
    bot.send_message(message.from_user.id, "Введите ID товара, который хотите удалить из корзины: ")
    bot.register_next_step_handler(message, delete_product_in_db)
    return ''


def delete_product_in_db(message):
    text = message.text
    if 0 < int(message.text) <= 20:
        if bot_utilites.is_exist(message.text, message.chat.id):
            bot_utilites.delete_product(text, message.chat.id)
            bot.send_message(message.chat.id, text='''
Товар успешно удален!

Чтобы посмотреть корзину нажмите /bin
Чтобы вернуться в главное меню нажмите /help''')
        else:
            bot.send_message(message.chat.id, text='''
Такого товара нет в корзине!

Чтобы посмотреть корзину нажмите /bin
Чтобы вернуться в главное меню нажмите /help''')
    else:
        bot.send_message(message.chat.id, text=f'''
Введите число от 1 до 20
{delete_product(message)}''')


@bot.message_handler(commands=['clear'])
def clear_bin(message):
    bot_utilites.delete_all(message.chat.id)
    bot.send_message(message.chat.id, text='''
Корзина пустая!
Чтобы вернуться в главное меню нажмите /help''')


print('start bot')
bot.infinity_polling()

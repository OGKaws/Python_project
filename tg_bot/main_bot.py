from Class_client import Client
from Class_clients import Clients
import json
import telebot
from telebot import types

########################################################################################################################-------- ПЕРЕМЕННЫЕ

bot = telebot.TeleBot('7073557228:AAHxo15uAsWyGQ7sRvv8POBqGjX1yNlHFf0')
clients = Clients('clients.json')
# client_q = 0
user_action = {}

########################################################################################################################--------- БЛОК ОБРАБОТКИ КОМАНД

@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = types.ReplyKeyboardMarkup()
    btn_add_client = types.KeyboardButton('Добавить клиента')
    btn_show_clients = types.KeyboardButton('Показать клиентов')
    btn_complet_training = types.KeyboardButton('Отметить проведенную тренировку')
    btn_delete_client = types.KeyboardButton('Удалить клиента')
    markup.add(btn_add_client, btn_show_clients, btn_complet_training, btn_delete_client)
    bot.send_message(message.chat.id,'Выберите действие ', reply_markup=markup)

@bot.message_handler(commands=['save'])
def save_data(message):
    clients.load_to_json()
    bot.send_message(message.chat.id, "Данные записаны в файл")

@bot.message_handler(func=lambda message:message.text=='Добавить клиента')
def handle_message(message):
    ask_for_name(message)

@bot.message_handler(func=lambda message : message.text == 'Отметить проведенную тренировку')
def handle_complete_training(message):
    user_action[message.chat.id] = 'complete_training'
    select_client(message)

@bot.message_handler(func=lambda message : message.text == 'Удалить клиента')
def handle_delete_client(message):
    user_action[message.chat.id] = 'delete'
    select_client(message)

@bot.message_handler(func=lambda message : message.text == 'Показать клиентов')
def client_info(message):
    try:
        cl_info = clients.Clients_info()
        bot.send_message(message.chat.id, cl_info)
    except ValueError:
        bot.send_message(message.chat.id, 'Список клиентов пуст')

# @bot.message_handler(func=lambda message : message.text == 'Выключить бота')
# def exit_bot(message):
#     clients.load_to_json()
#     exit()

########################################################################################################################------ БЛОК ОБРАБОТКИ ВЫЗОВА КНОПОК

@bot.callback_query_handler(func=lambda call: call.data.startswith('select_'))
def select_action_with_client(call):
    action = user_action[call.message.chat.id]
    client_name = call.data.replace('select_', '').replace('_',' ')
    if action == 'delete':
        confirm_delete(call, client_name)
    elif action == 'complete_training':
        clients.Clients_mark_training(client_name)
        bot.answer_callback_query(call.id, f"Тренировка клиента {client_name} отмечена как пройденная")

@bot.callback_query_handler(func=lambda call : call.data.startswith('confirm_delete_') or call.data == 'cancel_delete')
def delete_client(call):
    if call.data.startswith('confirm_delete_'):
        client_name = call.data.replace('confirm_delete_', '').replace('_', ' ')
        result = clients.Clients_delete(client_name)
        bot.send_message(call.message.chat.id, result)
    elif call.data.startswith('cancel_delete'):
        bot.send_message(call.message.chat.id, 'Удаление клиента отменено')

########################################################################################################################------- ОСНОВНОЙ КОД БОТА

def ask_for_name (message):
    bot.send_message(message.chat.id, 'Введите имя клиента')
    bot.register_next_step_handler(message, ask_for_paid_sessions)

def ask_for_paid_sessions(message):
    client_name = message.text
    msg = bot.send_message(message.chat.id, 'Сколько занятий оплачено? ')
    bot.register_next_step_handler(msg, paid_sessions_to_int, client_name)

def paid_sessions_to_int(message, client_name):
    try:
        paid_sessions = int(message.text)
        create_client(message, client_name, paid_sessions)
    except ValueError:
        bot.send_message(message.chat.id, 'Введите целое число')

def create_client(message, client_name, paid_sessions):
    clients.Clients_create(client_name)
    clients.Clients_paid_done(client_name, paid_sessions)
    bot.send_message(message.chat.id, 'Клиент успешно добавлен ')

def select_client(message):
    markup = types.InlineKeyboardMarkup()
    try:
        for client in clients.client_list:
            callback_data = f"select_{client.name.replace(' ', '_')}"
            client_button = types.InlineKeyboardButton(client.name, callback_data=callback_data)
            markup.add(client_button)
        bot.send_message(message.chat.id,'Выберите клиента', reply_markup=markup)
    except ValueError:
        bot.send_message(message.chat.id, 'Клиенты не найдены')

def confirm_delete(call,client_name):
    markup = types.InlineKeyboardMarkup()
    yes_btn = types.InlineKeyboardButton('Да', callback_data=f'confirm_delete_{client_name}')
    no_btn = types.InlineKeyboardButton('Нет', callback_data='cancel_delete')
    markup.add(yes_btn,no_btn)
    bot.send_message(call.message.chat.id, f'Уверены что хотите удалить клиента {client_name}?', reply_markup=markup)

bot.polling()






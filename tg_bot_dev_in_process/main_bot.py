from Training_client.dev_in_process_tg_bot.Class_client import Client
import json
import telebot



bot = telebot.TeleBot('7073557228:AAHxo15uAsWyGQ7sRvv8POBqGjX1yNlHFf0')
clients = {}
client_q = 0

@bot.message_handler(commands=['add_client'])
def start_bot(message):
    msg = bot.reply_to(message, "Создать клиента? (y/n) ")
    bot.register_next_step_handler(msg, registry_new_client)

def registry_new_client (message):
    if message.text.lower() == 'y':
        bot.send_message(message.chat.id, 'Введите имя клиента ')
        bot.register_next_step_handler(message, create_client_name)
    else :
        bot.send_message(message.chat.id, "Добавление клиента отменено ")

def create_client_name(message):
    client_name = message.text
    msg = bot.send_message(message.chat.id, 'Сколько занятий оплачено? ')
    bot.register_next_step_handler(msg, create_client_p_session, client_name)

def create_client_p_session(message, client_name):
    client_session = message.text
    global client_q
    client_q += 1
    new_client = Client(client_name)
    new_client.Client_paid_training(client_session)
    client_data = new_client.Client_to_dict()

    try:
        with open('clients.json', 'r+') as client_json:
            data = json.load(client_json)
            data['clients'].append(client_data)
            client_json.seek(0)
            json.dump(data, client_json, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        with open ('clients.json', 'w') as client_json:
            json.dump({'clients' : [client_data]}, client_json, ensure_ascii=False, indent=4)

    bot.send_message(message.chat.id, 'Клиент успешно добавлен ')

bot.polling()






import telebot
import threading
from telebot import types


#########################Bot###################################################
bot = telebot.TeleBot('5774941990:AAG1jELhrEo5g6122ac5Ooxc7U0N8JhzJTo')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Define the inline keyboard buttons
    get_max_messages_button = types.InlineKeyboardButton(text='Max Message', callback_data='get_max_messages')
    get_resend_time_limit_button = types.InlineKeyboardButton(text='Timer Interval', callback_data='get_resend_time_limit')
    get_channel_id_button = types.InlineKeyboardButton(text='Add new channel', callback_data='get_channel_id')
    get_session_file_button = types.InlineKeyboardButton(text='Session id', callback_data='get_session_file')
    get_destination_channel_button = types.InlineKeyboardButton(text='My Channel id', callback_data='get_destination_channel')
    status_button = types.InlineKeyboardButton(text='Status', callback_data='status')
    # Create the markup for the inline keyboard
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(get_max_messages_button, get_resend_time_limit_button)
    keyboard.add(status_button)
    keyboard.add(get_channel_id_button, get_session_file_button,get_destination_channel_button,)

    chat_id = message.chat.id
    text = "Welcome to the Program Bot🤖! Here are the available commands:"
    # Send the message with inline keyboard
    bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
    text = "©️Create by @Najjix , Buy : 🌐 https://cybersell.pro/ "
    bot.send_message(chat_id=chat_id,text=text,reply_markup=Config)



# Define the Config keyboard botton

Config = telebot.types.ReplyKeyboardMarkup(row_width=10)
Config.row('/start')

# Define a dictionary to store locks for each function
function_locks = {
    'get_max_messages': threading.Lock(),
    'get_resend_time_limit': threading.Lock(),
    'get_channel_id': threading.Lock(),
    'get_session_file': threading.Lock(),
    'get_destination_channel': threading.Lock(),
    'status': threading.Lock(),
}

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    function_name = call.data
    # Check if the lock for this function is acquired
    if function_locks[function_name].locked():
        bot.answer_callback_query(call.id, text="Please wait for the previous action to finish.")
        return
    # If the lock is not acquired, acquire it and execute the function
    with function_locks[function_name]:
        if function_name == 'get_max_messages':
            get_max_messages(call.message)
        elif function_name == 'get_resend_time_limit':
            get_resend_time_limit(call.message)
        elif function_name == 'get_channel_id':
            get_channel_id(call.message)
        elif function_name == 'get_session_file':
            get_session_file(call.message)
        elif function_name == 'get_destination_channel':
            change_destination_channel(call.message)
        elif function_name == 'status':
            status(call.message)


def get_destination_channel(message):
        bot.reply_to(message, "Please enter the channel destination id you want to add:")
        bot.register_next_step_handler(message, change_destination_channel)

def change_destination_channel(message):
    try:
        new_channel_id = int(message.text)
        global TO_CHANNEL
        TO_CHANNEL = new_channel_id
        print(f"Destination channel changed to {new_channel_id}.")

    except ValueError:
        print("Error: Invalid channel ID. Please enter a numeric value.")


# Define the function to change the session file
def get_session_file(message):
    bot.reply_to(message, "Please send the session id you want to add:")
    bot.register_next_step_handler(message, change_session_file)

def change_session_file(message):
    try:
        new_session_path = message.text
        global SESSION
        SESSION = new_session_path
        print(f"Session file changed to {new_session_path}.")

    except FileNotFoundError:
        print("Error: Session file not found. Please check the file path and try again.")


# Define the function to change the resending time limit
def get_resend_time_limit(message):
    bot.reply_to(message, "Please send the resend time do you prefer:")
    bot.register_next_step_handler(message, change_resend_time_limit)

def change_resend_time_limit(message):
    try:
        new_limit = int(message.text)
        global HOUR_LIMIT
        HOUR_LIMIT = new_limit
        bot.reply_to(message,f" new limit set to : {HOUR_LIMIT}")
        print(f"Resending time limit changed to {new_limit} seconds.")

    except ValueError:
        print("Invalid value entered for resending time limit.")

    except Exception as e:
        print(f"An error occurred while changing the resending time limit: {e}")


# Define the function to change the maximum number of messages sent in an hour
def get_max_messages(message):
    bot.reply_to(message, "Please send the number of max messages do you prefer:")
    bot.register_next_step_handler(message, change_max_messages)

def change_max_messages(message):
    try:
        global MAX_MESSAGES_PER_HOUR
        new_limit = int(message.text)
        MAX_MESSAGES_PER_HOUR = new_limit
        bot.reply_to(message, f" new limit set to : {MAX_MESSAGES_PER_HOUR}")
        print(f"Maximum messages per hour changed to {new_limit}.")
    except ValueError:
        print("Invalid value entered for maximum messages per hour.")
    except Exception as e:
        print(f"An error occurred while changing the maximum messages per hour: {e}")

def status(message):
    required_text = "『 @ProxyKeder 』"
    bot.reply_to(message,f"The Program is Running for this channel! :🆔 {required_text}\n\n🔢 Max Message = {MAX_MESSAGES_PER_HOUR}\n\n⏳Timer Interval= {HOUR_LIMIT}\n\nℹ️session:\n {SESSION} \n\nℹ️My channel id : {TO_CHANNEL}")

#################################################################################################

bot.polling()
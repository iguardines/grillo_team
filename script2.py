# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
import yfinance as yf

API_TOKEN = '1448700623:AAFyKeGUL3eTFkbHbqTTb9KT87-tX-jBh8s'

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hola! soy nacho_java_bot, una porcion de codigo que contesta mensajes, no hago mucho aun
pero es una muestra de lo que esta herramienta puede empezar a hacer
""")
    
# Handle '/funciones
@bot.message_handler(commands=['opciones'])
def send_function3(message):
    bot.reply_to(message, """\
    las funciones posibles son
    /start da mensaje de bienvenida
    /help lo mismo que /start
    /volumen_ggal da el monto en nominales hasta el momento
    /este no existe
""")

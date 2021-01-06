
# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
import yfinance as yf


def obtenerVolumenActivo(activo="ggal.ba"):
  data = yf.download(activo)
  volumen = data.iloc[-1, -1]
  precio = data.iloc[-1, -2]
  return volumen * precio

def obtenerPrecioActivo(activo="ggal.ba"):
  data = yf.download(activo)
  precio = data.iloc[-1, -2]
  return  precio


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


    
# Handle '/funciones
@bot.message_handler(commands=['volumen_ggal'])
def send_function1(message):
    bot.reply_to(message, obtenerVolumenActivo("ggal.ba"))

# Handle '/funciones
@bot.message_handler(commands=['precio_ggal'])
def send_function2(message):
    bot.reply_to(message, obtenerPrecioActivo("ggal.ba"))


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.polling(none_stop=True)

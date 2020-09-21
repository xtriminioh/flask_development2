"""
create telegrambot of raspberry pi
by: xtriminioh
"""
import sys
import os
import time
import json  # para leer el documento json donde esta la ip y id
from os.path import abspath  # libreria para uso de rutas dentro del document
import telebot  # importamos la libreria a utilizar, donde esta la api de telegram


# Esta funcion devuelve el documento json, donde se alojan el token y id
def open_document_token(path):
    src = abspath(path)
    with open(src, 'r') as f:
        return json.load(f)


commands = {
    'start': 'Inicializa el bot.',
    'help': 'Da informacion sobre los comandos disponibles.',
    'status': 'Estatus del servicio del boy, montado en una rpi.',
    'getip': 'Obtener el ip del servidor.',
    'reboot': 'Reinici los servicios de la rpi.'
}

doc = open_document_token(sys.argv[1])
bot = telebot.TeleBot(doc['TOKEN'], parse_mode=None)
message = "Soy un bot de telegram para asistencia remota de una raspberry"


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(chat_id=doc['ID'],
                     text="Bienvenido, help para mas ayuda.")


@bot.message_handler(commands=['help'])
def help_bot(message):
    help_text = "Comandos disponibles: \n"
    for key in commands:
        help_text += "/{0}:{1}\n".format(key, commands[key])
    bot.send_message(chat_id=doc['ID'], text=help_text)


@bot.message_handler(commands=['status'])
def send_status(message):
    bot.send_message(chat_id=doc['ID'], text="Servicio actualmente activo")


@bot.message_handler(commands=['getip'])
def send_ip(message):
    ip_text = os.popen("hostname -i")
    ip_text = "IP: {0}".format(ip_text.read())
    bot.send_message(chat_id=doc['ID'], text=ip_text)


@ bot.message_handler(commands=['reboot'])
def send_reboot(message):
    bot.send_message(chat_id=doc['ID'], text="Voy a reinicial el servidor...")
    bot.send_chat_action(chat_id=doc['ID'], action='typing')
    time.sleep(3)
    bot.send_message(chat_id=doc['ID'],
                     text="El servidor se esta reiniciando.")
    os.system("sudo shutdown -r now")


bot.polling()

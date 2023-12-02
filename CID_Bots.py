#Main libs
import os
import json
import telebot

#Components
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from telebot.types import ForceReply
from telebot.types import BotCommand



#Essentials
bot_Token : str = "6604703150:AAHYcCPG8jJPOX7p-R9_CKBQYevEEYG2nw0"
bot = telebot.TeleBot(bot_Token)



#publics
@bot.message_handler(content_types = ["new_chat_members"])
def _welcome(message) -> None:
    for i in message.new_chat_members:
        bot.reopen_general_forum_topic(message.chat.id)
        
        if i.username != None:
            msg = bot.send_photo(chat_id = message.chat.id, caption = f"Bienvenid@ @<b>{i.username}</b> a {message.chat.title}. \n\nAqui podras aprender y compartir tus experiencias relacionadas a todos los aspectos del <i><b>desarrollo de videojuegos</b></i> o <i><b>cualquiera de sus ramas</b></i>. \nUtiliza <b>/start</b> en el chat grupal!.", parse_mode = "HTML", photo = "https://www.google.com/imgres?imgurl=https%3A%2F%2Fi.pinimg.com%2F564x%2F98%2F50%2F22%2F985022ad17ee2ef4b3abe973289651b4.jpg&tbnid=vJsSru9cJ6dnzM&vet=12ahUKEwjI6sLX_76CAxXmM1kFHfdlDf4QMygfegUIARCaAQ..i&imgrefurl=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F436989970087800497%2F&docid=95p67iX4GQawiM&w=506&h=400&q=Dragon%20Pixel%20art%20style&client=firefox-b-d&ved=2ahUKEwjI6sLX_76CAxXmM1kFHfdlDf4QMygfegUIARCaAQ")
        
        else :
            msg = bot.send_photo(chat_id = message.chat.id, caption = f"Bienvenid@ <b>{i.first_name}</b> a {message.chat.title}. \n\nAqui podras aprender y compartir tus experiencias relacionadas a todos los aspectos del <i><b>desarrollo de videojuegos</b></i> o <i><b>cualquiera de sus ramas</b></i>. \nUtiliza <b>/start</b> en el chat grupal!.", parse_mode = "HTML", photo = "https://www.google.com/imgres?imgurl=https%3A%2F%2Fi.pinimg.com%2F564x%2F98%2F50%2F22%2F985022ad17ee2ef4b3abe973289651b4.jpg&tbnid=vJsSru9cJ6dnzM&vet=12ahUKEwjI6sLX_76CAxXmM1kFHfdlDf4QMygfegUIARCaAQ..i&imgrefurl=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F436989970087800497%2F&docid=95p67iX4GQawiM&w=506&h=400&q=Dragon%20Pixel%20art%20style&client=firefox-b-d&ved=2ahUKEwjI6sLX_76CAxXmM1kFHfdlDf4QMygfegUIARCaAQ")
        
        bot.delete_message(chat_id = message.chat.id, message_id = msg.id-1)
        bot.close_general_forum_topic(message.chat.id)
        bot.delete_message(chat_id = message.chat.id, message_id = msg.id+1)

@bot.message_handler(commands = ["start"])
def _start(message) -> None:
    if message.chat.title != None:
        bot.reply_to(message, f"Soy el bot de {message.chat.title}. Este bot esta diseñado para ayudarte en tu camino para conseguir y mejorar varias de tus habilidades, para ver una lista de recursos utiles utiliza <b>/resources</b>.", parse_mode = "HTML")

    else :
        bot.send_message(chat_id = message.chat.id, text = f"Este bot fue diseñado para ayudarte a conseguir y mejorar varias de tus habilidades, para ver una lista de recursos utiles utiliza <b>/resources</b>.", parse_mode = "HTML")

@bot.message_handler(commands = ["resources"])
def _resources(message) -> None:
    with open("CID_Data/resources_Titles.json", "r") as json_IMP:
        resources_Lib : dict = json.loads(json_IMP.read())

    resources_Query = InlineKeyboardMarkup()
    for key, value in resources_Lib.items():
        add_Query = InlineKeyboardButton(text = key, callback_data = value)
        resources_Query.add(add_Query)
    
    bot.reply_to(message = message, text = f"Seleccione la categoria de <b>recursos</b> que desee.", reply_markup = resources_Query, parse_mode = "HTML")

@bot.callback_query_handler(func = lambda call: True)
def _view_resources(call) -> None:
    if call.data != "back":
        edited_text : str = "<i><b>Lista de recursos.</b></i>"
        with open("CID_Data/resources_Data.json", "r", encoding = "utf-8") as json_IMP:
            resources_Lib : dict = json.loads(json_IMP.read())
        
        resources_Query = InlineKeyboardMarkup()
        for key, value in resources_Lib[call.data].items():
            add_Query = InlineKeyboardButton(text = key, url = value)
            resources_Query.add(add_Query)
        
        add_Query = InlineKeyboardButton(text = "Atras", callback_data = "back")
        resources_Query.add(add_Query)
    
    else :
        edited_text : str = "Seleccione la categoria de <b>recursos</b> que desee."
        with open("CID_Data/resources_Titles.json", "r") as json_IMP:
            resources_Lib : dict = json.loads(json_IMP.read())

        resources_Query = InlineKeyboardMarkup()
        for key, value in resources_Lib.items():
            add_Query = InlineKeyboardButton(text = key, callback_data = value)
            resources_Query.add(add_Query)
        
    bot.edit_message_text(
        text = edited_text,
        chat_id = call.message.chat.id,
        message_id = call.message.id,
        parse_mode = "HTML",
        reply_markup = resources_Query
    )

@bot.message_handler(commands = ["wish"])
def _wish(message) -> None:
    msg = bot.reply_to(message = message, text = "Escriba a continuacion el contenido que desea.")
    bot.register_next_step_handler(msg, _send_wish)

def _send_wish(message) -> None:
    bot.reply_to(message = message, text = "Gracias por su pedido!. Hemos enviado los mensajes al equipo de administracion.")

    with open("CID_Data/admin_Data.json", "r") as json_IMP:
        admins_Lib : dict = json.loads(json_IMP.read())
        
    for key, value in admins_Lib.items():
        bot.send_message(chat_id = value, text = f"Hola @{key}, uno de los miembros, @{message.from_user.username} tiene un pedido:\n<i>{message.text}</i>", parse_mode = "HTML")
    
@bot.message_handler(commands = ["subscribe"])
def _subscribe(message) -> None:

    with open("CID_Data/subscriptions_Data.json", "r") as json_IMP:
        subscriptions_Lib : dict = json.loads(json_IMP.read())
        
    if not subscriptions_Lib.__contains__(message.from_user.username):
        subscriptions_Lib[message.from_user.username] = message.from_user.id

        with open("CID_Data/subscriptions_Data.json", "w") as json_IMP:
            json.dump(subscriptions_Lib, json_IMP)

        bot.reply_to(message = message, text = f"Le agradecemos por su subscripcion <b><i>@{message.from_user.username}</i></b>. A apartir de ahora recibira los beneficios para <b><i>subscriptores</i></b>.", parse_mode = "HTML")

    else :
        bot.reply_to(message = message, text = f"Usted ya esta subscrito al <b><i>servicio de notificaciones</i></b>", parse_mode = "HTML")


@bot.message_handler(commands = ["unsub"])
def _unsub(message) -> None:
        
    with open("CID_Data/subscriptions_Data.json", "r") as json_IMP:
        subscriptions_Lib : dict = json.loads(json_IMP.read())

    if subscriptions_Lib.__contains__(message.from_user.username):
            
        subscriptions_Lib.pop(message.from_user.username)
        bot.reply_to(message = message, text = f"<b><i>Subscripcion</i></b> retirada", parse_mode = "HTML")
            
        with open("CID_Data/subscriptions_Data.json", "w") as json_IMP:
            json.dump(obj = subscriptions_Lib, fp = json_IMP)
        
    else :
        bot.send_message(chat_id = message.chat.id, text = f"Usted no esta subscrito al servicio de notificaciones, para subscribirse utilice <b><i>/subscribe</i></b>", parse_mode = "HTML")

@bot.message_handler(commands = ["dice"])
def _dice(message) -> None:
    bot.send_dice(chat_id = message.chat.id, emoji = "🎲", reply_to_message_id = message.id, message_thread_id = message.message_thread_id)

@bot.message_handler(commands = ["report"])
def _get_report(messsage) -> None:
    if messsage.from_user.username != None:
        msg = bot.reply_to(message = messsage, text = f"Hola <b>@{messsage.from_user.username}</b>!. Indica el error encontrado en tu siguiente mensaje por favor.", parse_mode = "HTML")
    
    else :
        msg = bot.reply_to(message = messsage, text = f"Hola <b>{messsage.from_user.first_name}</b>!. Indica el error encontrado en tu siguiente mensaje por favor.", parse_mode = "HTML")
    
    bot.register_next_step_handler(msg, _send_report)

def _send_report(message) -> None:
    bot.reply_to(message = message, text = "Tu reporte sera revisado lo mas pronto posible!.")

    with open("CID_Data/reports_Data.json", "r", encoding = "utf-8") as json_IMP:
        reports_Lib : dict = json.loads(json_IMP.read())

    reports_Lib[message.from_user.username] = message.text+"\n"
    
    with open("CID_Data/reports_Data.json", "w", encoding = "utf-8") as json_EXP:
        json.dump(obj = reports_Lib, fp = json_EXP)



#privates
@bot.message_handler(commands = ["news_send"])
def _news_send(message) -> None:
    msg = bot.send_message(chat_id = message.chat.id, text = "A continuacion escriba el comunicado.")
    bot.register_next_step_handler(msg, _news_global)

def _news_global(message) -> None:
    with open("CID_Data/admin_Data.json", "r") as json_IMP:
        admins_Lib : dict = json.loads(json_IMP.read())
    
    with open("CID_Data/chats_Data.json", "r") as json_IMP:
        group_Libs : dict = json.loads(json_IMP.read())

    for key, value in admins_Lib.items():
        if (message.from_user.username == key):

            for key, value in group_Libs.items():
                bot.reopen_forum_topic(chat_id = key, message_thread_id = value)

                if message.document != None:
                    bot.send_chat_action(chat_id = key, action = "upload_document")
                    msg = bot.send_document(chat_id = key, document = message.document.file_id, caption = f"Comunicado de <b>@{message.from_user.username}</b> \n\n<i>{message.caption}</i>", message_thread_id = value, parse_mode = "HTML")

                elif message.photo != None:
                    bot.send_chat_action(chat_id = key, action = "upload_photo")
                    msg = bot.send_photo(chat_id = key, photo = message.photo[0].file_id, caption = f"Comunicado de <b>@{message.from_user.username}</b> \n\n<i>{message.caption}</i>", message_thread_id = value, parse_mode = "HTML")

                else :
                    bot.send_chat_action(chat_id = key, action = "typing")
                    msg = bot.send_message(chat_id = key, text = f"Comunicado de <b>@{message.from_user.username}</b> \n\n<i>{message.text}</i>", message_thread_id = value, parse_mode = "HTML")
                
                bot.delete_message(chat_id = key, message_id = msg.id-1)
                bot.close_forum_topic(chat_id = key, message_thread_id = value)
                bot.delete_message(chat_id = key, message_id = msg.id+1)
    
@bot.message_handler(commands = ["subs_send"])
def _subs_send(message) -> None:
    msg = bot.reply_to(message = message, text = "Diga el comuncado a continuacion.")
    bot.register_next_step_handler(msg, _subs_global)

def _subs_global(message) -> None:
    bool_TMP : bool = None

    with open("CID_Data/admin_Data.json", "r") as json_IMP:
        admin_lib : dict = json.loads(json_IMP.read())
    
    with open("CID_Data/subscriptions_Data.json", "r") as json_IMP:
        subscriptions_Lib : dict = json.loads(json_IMP.read())

    for key, value in admin_lib.items():
        if (message.from_user.username == key):

            for key_2, value_2 in subscriptions_Lib.items():

                if message.document != None :
                    bot.send_chat_action(chat_id = value_2, action = "upload_document")
                    msg = bot.send_document(chat_id = value_2, document = message.document.file_id, caption = f"Hola @{key_2}, este archivo fue enviado por los administradores \n\n<i>{message.caption}</i>", parse_mode = "HTML")

                elif message.photo != None:
                    bot.send_chat_action(chat_id = value_2, action = "upload_photo")
                    bot.send_photo(chat_id = value_2, photo = message.photo[0].file_id, caption = f"Hola @{key_2}, uno de los administradores a enviado esta imagen \n<i>{message.caption}</i>", parse_mode = "HTML")

                else :
                    bot.send_chat_action(chat_id = value_2, action = "typing")
                    bot.send_message(chat_id = value_2, text = f"<b>Hola @{key_2}, aqui tienes un comunicado enviado por los administradores.</b>\n<i>{message.text}</i>", parse_mode = "HTML")

@bot.message_handler(commands = ["_send"])
def _send(message) -> None:
    msg = bot.reply_to(message = message, text = "Escriba el comunicado a continuacion")
    bot.register_next_step_handler(msg, _send_global)

def _send_global(message) -> None:
    with open("CID_Data/admin_Data.json", "r") as json_IMP:
        admins_Lib : dict = json.loads(json_IMP.read())
    
    with open("CID_Data/chats_Data.json", "r") as json_IMP:
        chats_Lib : dict = json.loads(json_IMP.read())
    
    for key, value in admins_Lib.items():
        if (message.from_user.username == key):
            
            for key, value in chats_Lib.items():
                bot.reopen_general_forum_topic(key)

                if message.document != None :
                    bot.send_chat_action(chat_id = key, action = "upload_document")
                    msg = bot.send_document(chat_id = key, document = message.document.file_id, caption = f"Comunicado global de <b>@{message.from_user.username}</b> \n\n<i>{message.caption}</i>", parse_mode = "HTML")

                elif message.photo != None:
                    bot.send_chat_action(chat_id = key, action = "upload_photo")
                    msg = bot.send_photo(chat_id = key, photo = message.photo[0].file_id, caption = f"Comunicado global de <b>@{message.from_user.username}</b> \n\n<i>{message.caption}</i>", parse_mode = "HTML")
                
                else : 
                    bot.send_chat_action(chat_id = key, action = "typing")
                    msg = bot.send_message(chat_id = key, text = f"Comunicado global de <b>@{message.from_user.username}</b> \n\n<i>{message.text}</i>", parse_mode = "HTML", disable_web_page_preview = True)
        
                bot.delete_message(chat_id = key, message_id = msg.id-1)
                bot.close_general_forum_topic(key)
                bot.delete_message(chat_id = key, message_id = msg.id+1)

@bot.message_handler(commands = ["send_poll"])

def _poll_get(message) -> None:
    msg = bot.send_message(chat_id = message.chat.id, text = "Envie el formulario JSON a continuacion.")
    bot.register_next_step_handler(msg, _poll_send)

def _poll_send(message) -> None:

    with open("CID_Data/admin_Data.json", "r") as json_IMP:
        admins_Lib : dict = json.loads(json_IMP.read())

    with open("CID_Data/chats_Data.json", "r") as json_IMP:
        chats_Lib : dict = json.loads(json_IMP.read())

    data_Lib : dict = json.loads(message.text)
    
    for key, value in admins_Lib.items():
        if (message.from_user.username == key):

            for key, value in chats_Lib.items():

                bot.reopen_general_forum_topic(key)
                msg = bot.send_poll(chat_id = key, question = f"El administrador @{message.from_user.username} ha enviado una encuesta.\n\n" + data_Lib["question"], options = data_Lib["options"], is_anonymous = data_Lib["anonymous"], allows_multiple_answers = data_Lib["multiple_answer"])
                
                bot.delete_message(chat_id = key, message_id = msg.id-1)
                bot.close_general_forum_topic(key)
                bot.delete_message(chat_id = key, message_id = msg.id+1)

@bot.message_handler(commands = ["get_reports"])
def _show_reports(message) -> None:

    with open("CID_Data/reports_Data.json", "r") as json_IMP:
        errors_Lib : dict = json.loads(json_IMP.read())

    tmp_STR : str = ""
    for key, value in errors_Lib.items():
        tmp_STR += f"{key} : {value}"
    
    bot.send_message(chat_id = message.chat.id, text = f"<b>Reportes de error:</b> \n{tmp_STR}", parse_mode = "HTML")



#Debug mode
@bot.message_handler(commands = ["get_id"])
def _get_id(message) -> None:
    print(message.chat.id)
    
@bot.message_handler(commands = ["news_letter"])
def _set_global(message) -> None:
    print(message.message_thread_id)
    with open("CID_Data/admin_Data.json", "r") as json_IMP:
        admins_Lib : dict = json.loads(json_IMP.read())

    with open("CID_Data/chats_Data.json", "r") as json_IMP:
        group_Libs : dict = json.loads(json_IMP.read())

    for key, value in admins_Lib.items():
        if (message.from_user.username == key):

            if group_Libs.__contains__(str(message.chat.id)) == False:
                group_Libs[message.chat.id] = message.message_thread_id

            else :
                group_Libs.__setitem__(message.chat.id, message.message_thread_id)

            with open("CID_Data/chats_Data.json", "w") as json_DMP:
                json.dump(obj = group_Libs, fp = json_DMP)

@bot.message_handler(commands = ["get_form"])
def _form(message) -> None:
    bot.send_message(chat_id = message.chat.id, text = "{ \"question\" : \"title\" , \"options\" : [\"opt_1\", \"opt_2\"] , \"anonymous\" : false , \"multiple_answer\" : false }")

@bot.message_handler(commands = ["test"])
def _test(message) -> None:
    msg = bot.reply_to(message, message.text)
    bot.register_next_step_handler(msg, _test2)

def _test2(message) -> None:
    bot.send_message(chat_id = message.chat.id, text = message.text, parse_mode = "HTML")



#Bot menu commands
bot.set_my_commands([
    BotCommand("/start", "Inicia la actividad del bot."),
    BotCommand("/dice", "Lanzara un dado de 6 caras."),
    BotCommand("/resources", "Muestra una lista de recursos utiles."),
    BotCommand("/wish", "Utilice este comando para pedir recursos a administracion."),
    BotCommand("/subscribe", "Subscribirse al servicio de notificaciones del grupo."),
    BotCommand("/unsub", "Darse de baja del servicio de notificaciones."),
    BotCommand("/report", "Reportar un error en el bot.")
    ])

#loop
os.system("cls")
print("Start Debug")

bot.infinity_polling()

print("Debug end")
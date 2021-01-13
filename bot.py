from config import bot_token, creater_name, api_endpoint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import MessageEntity,InlineKeyboardButton, InlineKeyboardMarkup
import requests
import json

response_json = {}
deleted_msg_id = 0

wait = False

def fetchjson(url):
    
    response = requests.get(url)
    return response
        

def start(update, context):
    text=f"Hey {update.effective_user.full_name}!\n\n->You can download any song for free by using  me.\n-> Just share the name of the song\n\nI am created by {creater_name}"
    update.message.reply_text(text)

def buttonToDownload(update, context):
    query = update.callback_query
    query.answer()

    index = int(query.data)

    downloading_msg = context.bot.sendMessage(chat_id=update.effective_chat.id, text="Downloading 🏃‍♂️")

    

    context.bot.delete_message(chat_id=update.effective_chat.id,message_id=deleted_msg_id)

    song = response_json["result"][index]

    caption = f"{song['song_title']}\n{song['album_title']}\n{song['artist_name']}"

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=song["song_image"], caption=caption)

    context.bot.send_audio(chat_id=update.effective_chat.id, audio=song["stream_link"], title=song['song_title'])


    context.bot.delete_message(chat_id=update.effective_chat.id,message_id=downloading_msg.message_id)







def download(update, context):

    if not wait:
        searched_text = update.message.text
        outcome_msg = update.message.reply_text("Working on it...")
        try:
            response = fetchjson(api_endpoint + searched_text).text

            try:
                global response_json
                response_json = json.loads(response)
            except:
                outcome_msg.edit_text("No results found.")

            if (response_json["result"]):
                

                keyboard = []
                count = 0

                temp_list = []
                for result in response_json["result"]:
                    temp_list.append(InlineKeyboardButton(result["song_title"], callback_data=str(count)))
                    
                    keyboard.append(list(temp_list))
                    temp_list.clear()
                    count += 1
                
                reply_markup = InlineKeyboardMarkup(keyboard)

                context.bot.delete_message(chat_id=update.effective_chat.id,message_id=outcome_msg.message_id)

                select_msg = update.message.reply_text(f"Results for : {searched_text}\nClick the Button to download.", reply_markup=reply_markup)

                global deleted_msg_id

                deleted_msg_id = select_msg.message_id

    
        except KeyError:
            outcome_msg.edit_text("No results found.")

    else:
        update.message.reply_text("Please Wait..")  

    

updater = Updater(token=bot_token, use_context=True)

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))

dispatcher.add_handler(MessageHandler(Filters.text,download))

dispatcher.add_handler(CallbackQueryHandler(buttonToDownload))

updater.start_polling()
updater.idle()
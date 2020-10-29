from telegram.ext import Updater,CommandHandler,MessageHandler,Filters #importing requires handlers from telegram.ext
from Adafruit_IO import Client, Feed,Data #import libraries for adafruit
import requests #for getting data from cloud
import os #operating system

ADAFRUIT_IO_USERNAME = os.getenv('ADAFRUIT_IO_USERNAME')  #adafruit username and password should be given as 'Config Vars' in the settings of your app on Heroku 
ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY') 
#these keys are from adafruit .io

aio = Client(ADAFRUIT_IO_USERNAME,ADAFRUIT_IO_KEY) # create instance of REST client
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN') #token is generate from telebot

# Create Feed object with name 'projectbot'.
#feed = Feed(name='projectbot')

# Send the Feed to IO to create.
# The returned object will contain all the details about the created feed.
#result = aio.create_feed(feed)
#try to run upto these in separate cell after running create a dashboard in adafruit with the feed 'projectbot' and status indicator



def start(update,context):
   print(str(update.effective_chat.id))
   context.bot.send_message(chat_id=update.effective_chat.id,text="hello! Type  /lighton  to switch on light.Type  /light off to turn off light")
def unknown(update,context):
   context.bot.send_message(chat_id=update.effective_chat.id,text='illegal command')  
   
def turnonthelight(update,context): 
    chat_id=update.message.chat_id
    context.bot.send_message(chat_id=update.effective_chat.id,text="bulb is switched on")
    aio.create_data('projectbot',Data(value=1))
    context.bot.send_photo(chat_id=update.effective_chat.id,photo='https://png.pngtree.com/png-clipart/20191121/original/pngtree-light-bulb-vector-glowing-bright-light-bulb-icon-fluorescent-invention-3d-png-image_5138824.jpg')
    
def turnoffthelight(update,context):
    chat_id=update.message.chat_id
    aio.create_data('projectbot',Data(value=0))
    context.bot.send_message(chat_id=update.effective_chat.id,text="bulb is switched off")
    context.bot.send_photo(chat_id=update.effective_chat.id,photo='https://www.pngfind.com/pngs/m/530-5303728_light-off-incandescent-light-bulb-hd-png-download.png')
    
def given_message(bot,update):
    text=update.message.text.upper()
    text=update.message.text

    if text =='Turn on the light':
      turnonthelight(bot,update)
    elif text=='Turn off the light':
       turnoffthelight(bot,update)  
    else:
      unknown(bot,update)  
u=Updater('TELEGRAM_TOKEN',use_context=True) #api token of telegram bot
dp=u.dispatcher
dp.add_handler(CommandHandler('lighton',turnonthelight))
dp.add_handler(CommandHandler('lightoff',turnoffthelight))
dp.add_handler(CommandHandler('start',start))
dp.add_handler(MessageHandler(Filters.command,unknown))
dp.add_handler(MessageHandler(Filters.text,given_message))
u.start_polling()
u.idle()   

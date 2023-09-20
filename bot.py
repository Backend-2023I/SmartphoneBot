from pprint import pprint
from db import DB
from cart import Cart
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler
import os

brand='Apple'
doc_id=''
cart_py=Cart("cart.json")
db_py=DB("data.json")

TOKEN="6662177620:AAH-dEI7vGQWh-v3_piDLmm0qRnxptBqF2U"

def start(update:Update, context:CallbackContext):
    bot=context.bot
    chat_id=update.message.chat.id

    Shop=InlineKeyboardButton(text="🛍 Shop",callback_data="Shop")
    Cart=InlineKeyboardButton(text="📦 Cart",callback_data="Cart")
    Contact=InlineKeyboardButton(text="📞 Contact",callback_data="Contact")
    About=InlineKeyboardButton(text="📝 About",callback_data="About")

    keyboard=InlineKeyboardMarkup([[Shop,Cart],[Contact,About]])


    bot.sendMessage(chat_id,text="Welcome to smartphone bot",reply_markup=keyboard)

def main_menu(update: Update, context: CallbackContext):
    query = update.callback_query

    Shop=InlineKeyboardButton(text="🛍 Shop",callback_data="Shop")
    Cart=InlineKeyboardButton(text="📦 Cart",callback_data="Cart")
    Contact=InlineKeyboardButton(text="📞 Contact",callback_data="Contact")
    About=InlineKeyboardButton(text="📝 About",callback_data="About")

    keyboard=InlineKeyboardMarkup([[Shop,Cart],[Contact,About]])
    query.edit_message_text(text="Smartphone shop",reply_markup=keyboard)

def product(update: Update, context: CallbackContext):
    query = update.callback_query
    
    buttons = []
    for name in db_py.get_tables():
        button = InlineKeyboardButton(text=name,callback_data=f"products_{name}")
        buttons.append([button])
    back = InlineKeyboardButton(text="⬅️ back",callback_data="main_menu")
    buttons.append([back])
    keyboard=InlineKeyboardMarkup(buttons)
    query.edit_message_text(text="Choose a brand",reply_markup=keyboard)


def products(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    text, brand = data.split('_')
    data = db_py.get_phone_list(brand)

    buttons=[]
    for i in data:
        button=InlineKeyboardButton(text=i['name'],callback_data=f"phone_{brand}_{i.doc_id}")
        buttons.append([button])

    back = InlineKeyboardButton(text="back",callback_data="Shop")
    before = InlineKeyboardButton(text="⬅️",callback_data="before")
    next = InlineKeyboardButton(text="➡️",callback_data="next")
    buttons.append([before,next])

    buttons.append([back])
    keyboard=InlineKeyboardMarkup(buttons)
    query.edit_message_text(text=brand,reply_markup=keyboard)

def phone(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat.id
    bot = context.bot
    data = query.data
    global brand
    global doc_id
    text, brand, doc_id = data.split('_')
    phone = db_py.get_phone(brand, doc_id)

    text=f"name: {phone['name']}\nprice: {phone['price']} $\ncolor: {phone['color']} "
    add_cart = InlineKeyboardButton(text='add 🛒', callback_data="add_cart")
    keyboard = InlineKeyboardMarkup([[add_cart]])

    bot.sendPhoto(chat_id, phone['img_url'], caption=text, reply_markup=keyboard)
    query.answer("Done!")

def add_cart(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id=query.message.chat.id
    data=query.data
    cart_py.add(brand,doc_id,chat_id)
    query.answer("add cart")

def cart(update: Update, context: CallbackContext):
    query = update.callback_query
    order = InlineKeyboardButton(text="order",callback_data="order")
    remove = InlineKeyboardButton(text="remove",callback_data="order")

    keyboard = InlineKeyboardMarkup([[order, remove]])

    query.edit_message_text(text="Cart menu",reply_markup=keyboard)

updater=Updater(token=TOKEN)
dp=updater.dispatcher

dp.add_handler(CommandHandler("start",start))
dp.add_handler(CallbackQueryHandler(product, pattern="Shop"))
dp.add_handler(CallbackQueryHandler(products, pattern="products"))
dp.add_handler(CallbackQueryHandler(phone, pattern="phone"))
dp.add_handler(CallbackQueryHandler(main_menu, pattern="main_menu"))
dp.add_handler(CallbackQueryHandler(add_cart, pattern="add_cart"))
dp.add_handler(CallbackQueryHandler(cart, pattern="Cart"))

updater.start_polling()
updater.idle()
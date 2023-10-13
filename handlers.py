from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from db import DB
from cart import Cart

cart_py=Cart("/home/backend2023I2/SmartphoneBot/cart.json")
db_py=DB("/home/backend2023I2/SmartphoneBot/data.json")

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
    for brand in db_py.get_tables():
        button = InlineKeyboardButton(text=brand,callback_data=f"products_{brand}")
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
    start = 0
    stop = 10

    buttons=[]
    for i in data[start:stop]:
        button=InlineKeyboardButton(text=i['name'],callback_data=f"phone_{brand}_{i.doc_id}")
        buttons.append([button])

    back = InlineKeyboardButton(text="back",callback_data="Shop")
    before = InlineKeyboardButton(text="⬅️",callback_data=f"before_{start}_{stop}_{brand}")
    nextb = InlineKeyboardButton(text="➡️",callback_data=f"next_{start}_{stop}_{brand}")
    buttons.append([before,nextb])

    buttons.append([back])
    keyboard=InlineKeyboardMarkup(buttons)
    query.edit_message_text(text=brand,reply_markup=keyboard)

def nextproduct(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    text, start, stop, brand = data.split('_')

    start = int(start) + 10
    stop = int(stop) + 10

    data = db_py.get_phone_list(brand)


    if len(data) <= start:
        start = 0
        stop = 10

    buttons=[]
    for i in data[start:stop]:
        button=InlineKeyboardButton(text=i['name'],callback_data=f"phone_{brand}_{i.doc_id}")
        buttons.append([button])

    back = InlineKeyboardButton(text="back",callback_data="Shop")
    before = InlineKeyboardButton(text="⬅️",callback_data=f"before_{start}_{stop}_{brand}")
    nextb = InlineKeyboardButton(text="➡️",callback_data=f"next_{start}_{stop}_{brand}")
    buttons.append([before,nextb])

    buttons.append([back])
    keyboard=InlineKeyboardMarkup(buttons)
    query.edit_message_text(text=f"{brand} {start}/{stop}",reply_markup=keyboard)

def befoceproduct(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    text, start, stop, brand = data.split('_')

    start = int(start)
    stop = int(stop)

    data = db_py.get_phone_list(brand)
    
    if start == 0:
        if len(data)%10 != 0:
            start = len(data)//10*10
            stop = len(data)
        else:
            stop = len(data)
            start = stop - 10
    
    else:
        stop = start
        start = start - 10

    buttons=[]
    for i in data[start:stop]:
        button=InlineKeyboardButton(text=i['name'],callback_data=f"phone_{brand}_{i.doc_id}")
        buttons.append([button])

    back = InlineKeyboardButton(text="back",callback_data="Shop")
    before = InlineKeyboardButton(text="⬅️",callback_data=f"before_{start}_{stop}_{brand}")
    nextb = InlineKeyboardButton(text="➡️",callback_data=f"next_{start}_{stop}_{brand}")
    buttons.append([before,nextb])

    buttons.append([back])
    keyboard=InlineKeyboardMarkup(buttons)
    query.edit_message_text(text=f"{brand} {start}/{stop}",reply_markup=keyboard)

def phone(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat.id
    bot = context.bot
    data = query.data
    text, brand, doc_id = data.split('_')

    text, brand, doc_id = data.split('_')
    phone = db_py.get_phone(brand, doc_id)

    text=f"name: {phone['name']}\nprice: {phone['price']} $\ncolor: {phone['color']} "
    add_cart = InlineKeyboardButton(text='add 🛒', callback_data=f"addcart_{brand}_{doc_id}")
    keyboard = InlineKeyboardMarkup([[add_cart]])

    bot.sendPhoto(chat_id, phone['img_url'], caption=text, reply_markup=keyboard)
    query.answer("Done!")

def add_cart(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id=query.message.chat.id
    data=query.data
    text, brand, doc_id = data.split("_")
    cart_py.add(brand,doc_id,chat_id)
    query.answer("add cart")

def cart(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat.id
    order = InlineKeyboardButton(text="order",callback_data="order")
    remove = InlineKeyboardButton(text="remove",callback_data="remove")
    button = InlineKeyboardButton(text="Main Menu",callback_data="main_menu")
    keyboard = InlineKeyboardMarkup([[order, remove],[button]])
    products = cart_py.get_cart(chat_id)
    text = ""

    for product in products:

        brand = product['brand']
        doc_id = product['doc_id']
        phone = db_py.get_phone(brand, doc_id)
        
        name = phone['name']
        price = phone['price']
        memory = phone['memory']
        ram = phone['RAM']
        color = phone['color']
        
        text += f"Name: {name} - {color}\nPrice: {price}\nMemory: {memory}/{ram}\n\n"

    if text == "":
        text = "Empty Cart!"

    query.edit_message_text(text=text,reply_markup=keyboard)

def remove(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat.id

    cart_py.remove(chat_id)

    button = InlineKeyboardButton(text="Main Menu",callback_data="main_menu")
    keyboard=InlineKeyboardMarkup([[button]])

    query.edit_message_text(text='removed cart!',reply_markup=keyboard)

    query.answer('removed cart!')
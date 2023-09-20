from pprint import pprint
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler
import os
from handlers import (
    start, 
    product,
    products,
    phone,
    add_cart,
    main_menu,
    cart
)

TOKEN="6662177620:AAH-dEI7vGQWh-v3_piDLmm0qRnxptBqF2U"


updater=Updater(token=TOKEN)
dp=updater.dispatcher

dp.add_handler(CommandHandler("start",start))
dp.add_handler(CallbackQueryHandler(product, pattern="Shop"))
dp.add_handler(CallbackQueryHandler(products, pattern="products"))
dp.add_handler(CallbackQueryHandler(phone, pattern="phone"))
dp.add_handler(CallbackQueryHandler(main_menu, pattern="main_menu"))
dp.add_handler(CallbackQueryHandler(add_cart, pattern="addcart"))
dp.add_handler(CallbackQueryHandler(cart, pattern="Cart"))

updater.start_polling()
updater.idle()
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
    cart,
    remove,
    nextproduct,
    befoceproduct
)

TOKEN="6534122111:AAGYTeibRsxEuQ6_GPC6QjsH2dEiRWSo-7Y"


updater=Updater(token=TOKEN)
dp=updater.dispatcher

dp.add_handler(CommandHandler("start",start))
dp.add_handler(CallbackQueryHandler(product, pattern="Shop"))
dp.add_handler(CallbackQueryHandler(products, pattern="products"))
dp.add_handler(CallbackQueryHandler(phone, pattern="phone"))
dp.add_handler(CallbackQueryHandler(main_menu, pattern="main_menu"))
dp.add_handler(CallbackQueryHandler(add_cart, pattern="addcart"))
dp.add_handler(CallbackQueryHandler(cart, pattern="Cart"))
dp.add_handler(CallbackQueryHandler(remove, pattern='remove'))
dp.add_handler(CallbackQueryHandler(nextproduct, pattern='next'))
dp.add_handler(CallbackQueryHandler(befoceproduct, pattern='before'))

updater.start_polling()
updater.idle()
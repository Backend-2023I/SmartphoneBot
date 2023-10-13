import os 
from flask import Flask, request
import telegram
from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

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

TOKEN='6631602228:AAGoRj0gPSHyGDXuLFeYTwZ7lfM-bwYclzI'

app = Flask(__name__)

@app.route('/')
def main():
    return "SmartphoneBot"

@app.route("/webhook/", methods=["POST", "GET"])
def webhook():

    if request.method == "POST":
        bot = telegram.Bot(TOKEN)
        dp = Dispatcher(bot,update_queue=None, workers=0)
        update = request.get_json()
        print(update)
        update = Update.de_json(update, bot)
        
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


        dp.process_update(update)
    else:
        return {"result": "Only post request"}

if __name__ == "__main__":
    app.run(debug=True)

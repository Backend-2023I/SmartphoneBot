import telegram
import os 
from flask import Flask, request

TOKEN="6534122111:AAGYTeibRsxEuQ6_GPC6QjsH2dEiRWSo-7Y"
bot = telegram.Bot(TOKEN)

url = "https://backend2023i2.pythonanywhere.com/webhook/"

print(bot.delete_webhook())
print(bot.set_webhook(url))

print(bot.get_webhook_info())

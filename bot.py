import asyncio
import logging
import sys
import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = "8908643798:AAH0Ts3blVRgcS444DgCQxEfWTNBRg4b0eE"

PRODUCTS_FILE = "products.json"

if not os.path.exists(PRODUCTS_FILE):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump([
            { "id": 1, "name": "Костюм детский", "category": "boys", "size": "110 см", "price": 120, "salePrice": "", "photo": "", "desc": "Удобный костюм", "inStock": True },
            { "id": 2, "name": "Платье для девочки", "category": "girls", "size": "100 см", "price": 95, "salePrice": 80, "photo": "", "desc": "Нарядное платье", "inStock": False }
        ], f, ensure_ascii=False, indent=4)

class ShopAPIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/get_products":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            if os.path.exists(PRODUCTS_FILE):
                with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
                    data = f.read()
                self.wfile.write(data.encode('utf-8'))
            else:
                self.wfile.write(json.dumps([]).encode('utf-8'))
        else:
            super().do_GET()

def run_server():
    server = HTTPServer(('localhost', 8000), ShopAPIHandler)
    server.serve_forever()

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = (
        "🇹🇯 <b>Тоҷикӣ</b>\n"
        "👋 Салом! Хуш омадед ба мағозаи кӯдаконаи <b>Hello Kids</b>!\n\n"
        "🇷🇺 <b>Русский</b>\n"
        "👋 Привет! Добро пожаловать в магазин детской одежды <b>Hello Kids</b>!\n\n"
        "🇬🇧 <b>English</b>\n"
        "👋 Hello! Welcome to <b>Hello Kids</b> children's store!"
    )
    
    # Внимание: для работы локального сайта через ngrok или временный хостинг 
    # здесь будет ссылка. Пока ставим заглушку на GitHub Pages, 
    # но сам файл index.html у нас теперь идеальный чистый!
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛍 Открыть каталог / Shop", 
                    web_app=WebAppInfo(url="https://muhrh13080-pixel.github.io/hello-kids/index.html")
                )
            ]
        ]
    )
    
    await message.answer(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def main() -> None:
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
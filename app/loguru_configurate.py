from loguru import logger
from telegram import Bot
import os
from dotenv import load_dotenv
from asyncio import run
from threading import Thread
import time
import traceback

PROJECT_NAME = "ANTIDOUBLES"

def configurate_loguru():
    load_dotenv()

    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_LOGGING_TOKEN")
    TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_LOGGING_CHAT_ID")

    if TELEGRAM_CHAT_ID is None or TELEGRAM_TOKEN is None:
        logger.error("Добавьте TELEGRAM_LOGGING_TOKEN и TELEGRAM_LOGGING_CHAT_ID в .env для логгирования ошибок в телеграм бота.")
        return

    def telegram_log_handler(message: str):
        def send_message():
            repo_path = os.getcwd()
            try:
                bot = Bot(token=TELEGRAM_TOKEN)
                message_parts = message.split("LogException=")
                error_message = f"🚨 Ошибка ({PROJECT_NAME}):\n\n{message_parts[0]}"
                with_trace_back = len(message_parts) == 2
                if with_trace_back:
                    os.makedirs("excs", exist_ok=True)
                    filename = f"excs/exc_{time.time()}.log"
                    with open(filename, "w+") as file:
                        file.write(message_parts[1])
                    run(bot.send_document(chat_id=TELEGRAM_CHAT_ID, document=filename, caption=error_message))
                else:
                    run(bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=error_message))
            except Exception as e:
                print(f"Ошибка при отправке в Telegram: {e}")
        
        Thread(target=send_message, daemon=True).start()
    
    logger.add(telegram_log_handler, level="ERROR")
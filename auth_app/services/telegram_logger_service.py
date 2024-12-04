from telegram import Bot
from asyncio import run
from utils import create_log_file
from strategies.log_strategy import AbstractLogger
from dotenv import load_dotenv
from loguru import logger
import os
from typing import Optional


class TelegramLoggerService(AbstractLogger):

    def __init__(self, token: str, chat_id: str, service_name: str):
        self.bot = Bot(token)
        self.chat_id = chat_id
        self.service_name = service_name

    @staticmethod
    def is_message_has_traceback(message: str) -> bool:
        return len(message.split("LogException=")) == 2
    
    @staticmethod
    def get_message_and_traceback(message: str) -> tuple[str, str]:
        parts = message.split("LogException=")
        return parts[0], parts[1]
    
    def get_error_message(self, message: str) -> str:
        return f"🚨 Ошибка ({self.service_name}):\n\n{message}"

    def send_log(self, message: str):
        try:
            if self.is_message_has_traceback(message):
                message, traceback = self.get_message_and_traceback(message)
                exc_log_file = create_log_file("excs", "exc", traceback)
                run(self.bot.send_document(chat_id=self.chat_id, document=exc_log_file, caption=self.get_error_message(message)))
            else: 
                run(self.bot.send_message(chat_id=self.chat_id, text=self.get_error_message(message)))
        except Exception as e:
                print(f"Ошибка при отправке в Telegram: {e}")

def create_telegram_logger_from_dotenv() -> Optional[TelegramLoggerService]:
    load_dotenv()

    telegram_token = os.environ.get("TELEGRAM_LOGGING_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_LOGGING_CHAT_ID")

    if telegram_token is None or telegram_chat_id is None:
        logger.error("Добавьте TELEGRAM_LOGGING_TOKEN и TELEGRAM_LOGGING_CHAT_ID в .env для логгирования ошибок в телеграм бота.")
        return None
    return TelegramLoggerService(token=telegram_token, chat_id=telegram_chat_id, service_name="auth")
    
from loguru import logger
from telegram import Bot
import os
from dotenv import load_dotenv
from asyncio import run
from threading import Thread
import time
import traceback
from strategies.log_strategy import AbstractLogger

PROJECT_NAME = "ANTIDOUBLES"

def configurate_loguru(loggers: list[AbstractLogger] = []):
    
    for logger_service in loggers:
        def logger_handler(message: str):
            
            Thread(target=logger_service.send_log, args=(message,), daemon=True).start()
        
        logger.add(logger_handler, level="ERROR")
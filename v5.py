import asyncio
import logging
from datetime import datetime, timedelta
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode
import re
import json
import os

# ==================== CONFIGURATION ====================
BOT_TOKEN = "8586468507:AAF6AqTYBiL2ucH4BmXxSZR64W1X5D-Vdfs"
DEFAULT_CHANNEL = "@botsignal007"

# ==================== LOGGING ====================
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== FILES ====================
HISTORY_FILE = "signal_history.json"

# ==================== STORAGE ====================
user_data = {}
processed_results = set()

# ==================== ALL SIGNALS ====================
USDBRL_SIGNALS = [
    "🧪 USDBRL-OTC ☞ 09:29 🦅 CALL","🧪 USDBRL-OTC ☞ 09:34 🦅 CALL","🧪 USDBRL-OTC ☞ 09:41 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 09:48 🦅 CALL","🧪 USDBRL-OTC ☞ 09:54 🦅 PUT","🧪 USDBRL-OTC ☞ 09:58 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 10:03 🦅 PUT","🧪 USDBRL-OTC ☞ 10:08 🦅 PUT","🧪 USDBRL-OTC ☞ 10:14 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 10:17 🦅 PUT","🧪 USDBRL-OTC ☞ 10:20 🦅 CALL","🧪 USDBRL-OTC ☞ 10:23 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 10:28 🦅 CALL","🧪 USDBRL-OTC ☞ 10:31 🦅 PUT","🧪 USDBRL-OTC ☞ 10:37 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 10:42 🦅 CALL","🧪 USDBRL-OTC ☞ 10:47 🦅 PUT","🧪 USDBRL-OTC ☞ 10:54 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 10:58 🦅 CALL","🧪 USDBRL-OTC ☞ 11:01 🦅 PUT","🧪 USDBRL-OTC ☞ 11:04 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 11:11 🦅 CALL","🧪 USDBRL-OTC ☞ 11:15 🦅 CALL","🧪 USDBRL-OTC ☞ 11:18 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 11:25 🦅 CALL","🧪 USDBRL-OTC ☞ 11:29 🦅 CALL","🧪 USDBRL-OTC ☞ 11:34 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 11:37 🦅 CALL","🧪 USDBRL-OTC ☞ 11:44 🦅 PUT","🧪 USDBRL-OTC ☞ 11:49 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 11:53 🦅 PUT","🧪 USDBRL-OTC ☞ 11:59 🦅 PUT","🧪 USDBRL-OTC ☞ 12:03 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 12:09 🦅 CALL","🧪 USDBRL-OTC ☞ 12:13 🦅 PUT","🧪 USDBRL-OTC ☞ 12:18 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 12:25 🦅 PUT","🧪 USDBRL-OTC ☞ 12:29 🦅 CALL","🧪 USDBRL-OTC ☞ 12:36 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 12:40 🦅 CALL","🧪 USDBRL-OTC ☞ 12:44 🦅 PUT","🧪 USDBRL-OTC ☞ 12:50 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 12:57 🦅 CALL","🧪 USDBRL-OTC ☞ 13:04 🦅 CALL","🧪 USDBRL-OTC ☞ 13:08 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 13:15 🦅 PUT","🧪 USDBRL-OTC ☞ 13:19 🦅 CALL","🧪 USDBRL-OTC ☞ 13:22 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 13:27 🦅 CALL","🧪 USDBRL-OTC ☞ 13:32 🦅 PUT","🧪 USDBRL-OTC ☞ 13:35 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 13:42 🦅 CALL","🧪 USDBRL-OTC ☞ 13:48 🦅 CALL","🧪 USDBRL-OTC ☞ 13:53 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 13:57 🦅 CALL","🧪 USDBRL-OTC ☞ 14:03 🦅 PUT","🧪 USDBRL-OTC ☞ 14:08 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 14:12 🦅 PUT","🧪 USDBRL-OTC ☞ 14:16 🦅 CALL","🧪 USDBRL-OTC ☞ 14:23 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 14:26 🦅 PUT","🧪 USDBRL-OTC ☞ 14:31 🦅 PUT","🧪 USDBRL-OTC ☞ 14:34 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 14:37 🦅 PUT","🧪 USDBRL-OTC ☞ 14:44 🦅 PUT","🧪 USDBRL-OTC ☞ 14:50 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 14:54 🦅 CALL","🧪 USDBRL-OTC ☞ 15:00 🦅 CALL","🧪 USDBRL-OTC ☞ 15:06 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 15:12 🦅 PUT","🧪 USDBRL-OTC ☞ 15:18 🦅 CALL","🧪 USDBRL-OTC ☞ 15:21 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 15:26 🦅 PUT","🧪 USDBRL-OTC ☞ 15:30 🦅 CALL","🧪 USDBRL-OTC ☞ 15:34 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 15:37 🦅 PUT","🧪 USDBRL-OTC ☞ 15:41 🦅 PUT","🧪 USDBRL-OTC ☞ 15:44 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 15:51 🦅 PUT","🧪 USDBRL-OTC ☞ 15:56 🦅 PUT","🧪 USDBRL-OTC ☞ 16:00 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 16:05 🦅 PUT","🧪 USDBRL-OTC ☞ 16:08 🦅 PUT","🧪 USDBRL-OTC ☞ 16:15 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 16:21 🦅 CALL","🧪 USDBRL-OTC ☞ 16:24 🦅 PUT","🧪 USDBRL-OTC ☞ 16:27 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 16:33 🦅 CALL","🧪 USDBRL-OTC ☞ 16:39 🦅 PUT","🧪 USDBRL-OTC ☞ 16:44 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 16:50 🦅 CALL","🧪 USDBRL-OTC ☞ 16:55 🦅 PUT","🧪 USDBRL-OTC ☞ 16:59 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 17:02 🦅 PUT","🧪 USDBRL-OTC ☞ 17:08 🦅 CALL","🧪 USDBRL-OTC ☞ 17:12 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 17:15 🦅 CALL","🧪 USDBRL-OTC ☞ 17:20 🦅 PUT","🧪 USDBRL-OTC ☞ 17:25 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 17:32 🦅 CALL","🧪 USDBRL-OTC ☞ 17:39 🦅 CALL","🧪 USDBRL-OTC ☞ 17:44 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 17:47 🦅 PUT","🧪 USDBRL-OTC ☞ 17:52 🦅 PUT","🧪 USDBRL-OTC ☞ 17:58 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 18:03 🦅 PUT","🧪 USDBRL-OTC ☞ 18:06 🦅 CALL","🧪 USDBRL-OTC ☞ 18:12 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 18:17 🦅 PUT","🧪 USDBRL-OTC ☞ 18:24 🦅 PUT","🧪 USDBRL-OTC ☞ 18:27 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 18:30 🦅 PUT","🧪 USDBRL-OTC ☞ 18:35 🦅 CALL","🧪 USDBRL-OTC ☞ 18:41 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 18:44 🦅 CALL","🧪 USDBRL-OTC ☞ 18:48 🦅 CALL","🧪 USDBRL-OTC ☞ 18:51 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 18:57 🦅 PUT","🧪 USDBRL-OTC ☞ 19:03 🦅 CALL","🧪 USDBRL-OTC ☞ 19:06 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 19:09 🦅 PUT","🧪 USDBRL-OTC ☞ 19:13 🦅 PUT","🧪 USDBRL-OTC ☞ 19:20 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 19:27 🦅 PUT","🧪 USDBRL-OTC ☞ 19:32 🦅 CALL","🧪 USDBRL-OTC ☞ 19:35 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 19:39 🦅 PUT","🧪 USDBRL-OTC ☞ 19:42 🦅 PUT","🧪 USDBRL-OTC ☞ 19:48 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 19:54 🦅 PUT","🧪 USDBRL-OTC ☞ 20:01 🦅 CALL","🧪 USDBRL-OTC ☞ 20:04 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 20:07 🦅 PUT","🧪 USDBRL-OTC ☞ 20:12 🦅 CALL","🧪 USDBRL-OTC ☞ 20:18 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 20:25 🦅 CALL","🧪 USDBRL-OTC ☞ 20:31 🦅 CALL","🧪 USDBRL-OTC ☞ 20:34 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 20:38 🦅 CALL","🧪 USDBRL-OTC ☞ 20:44 🦅 CALL","🧪 USDBRL-OTC ☞ 20:51 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 20:56 🦅 PUT","🧪 USDBRL-OTC ☞ 21:00 🦅 CALL","🧪 USDBRL-OTC ☞ 21:06 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 21:11 🦅 PUT","🧪 USDBRL-OTC ☞ 21:17 🦅 PUT","🧪 USDBRL-OTC ☞ 21:22 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 21:26 🦅 CALL","🧪 USDBRL-OTC ☞ 21:32 🦅 PUT","🧪 USDBRL-OTC ☞ 21:38 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 21:45 🦅 PUT","🧪 USDBRL-OTC ☞ 21:52 🦅 CALL","🧪 USDBRL-OTC ☞ 21:57 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 22:02 🦅 PUT","🧪 USDBRL-OTC ☞ 22:05 🦅 CALL","🧪 USDBRL-OTC ☞ 22:09 🦅 CALL",
    "🧪 USDBRL-OTC ☞ 22:13 🦅 PUT","🧪 USDBRL-OTC ☞ 22:20 🦅 CALL","🧪 USDBRL-OTC ☞ 22:25 🦅 PUT",
    "🧪 USDBRL-OTC ☞ 22:30 🦅 PUT",
]

USDCOP_SIGNALS = [
    "🧪 USDCOP-OTC ☞ 09:30 🦅 CALL","🧪 USDCOP-OTC ☞ 09:36 🦅 CALL","🧪 USDCOP-OTC ☞ 09:42 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 09:46 🦅 CALL","🧪 USDCOP-OTC ☞ 09:53 🦅 PUT","🧪 USDCOP-OTC ☞ 09:56 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 09:59 🦅 PUT","🧪 USDCOP-OTC ☞ 10:06 🦅 PUT","🧪 USDCOP-OTC ☞ 10:12 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 10:19 🦅 PUT","🧪 USDCOP-OTC ☞ 10:22 🦅 CALL","🧪 USDCOP-OTC ☞ 10:27 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 10:34 🦅 CALL","🧪 USDCOP-OTC ☞ 10:41 🦅 PUT","🧪 USDCOP-OTC ☞ 10:46 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 10:50 🦅 CALL","🧪 USDCOP-OTC ☞ 10:53 🦅 PUT","🧪 USDCOP-OTC ☞ 10:59 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 11:05 🦅 CALL","🧪 USDCOP-OTC ☞ 11:09 🦅 PUT","🧪 USDCOP-OTC ☞ 11:12 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 11:17 🦅 CALL","🧪 USDCOP-OTC ☞ 11:24 🦅 CALL","🧪 USDCOP-OTC ☞ 11:29 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 11:35 🦅 CALL","🧪 USDCOP-OTC ☞ 11:38 🦅 CALL","🧪 USDCOP-OTC ☞ 11:43 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 11:50 🦅 CALL","🧪 USDCOP-OTC ☞ 11:54 🦅 PUT","🧪 USDCOP-OTC ☞ 11:58 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 12:05 🦅 CALL","🧪 USDCOP-OTC ☞ 12:10 🦅 CALL","🧪 USDCOP-OTC ☞ 12:14 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 12:20 🦅 CALL","🧪 USDCOP-OTC ☞ 12:23 🦅 CALL","🧪 USDCOP-OTC ☞ 12:26 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 12:29 🦅 PUT","🧪 USDCOP-OTC ☞ 12:34 🦅 CALL","🧪 USDCOP-OTC ☞ 12:37 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 12:40 🦅 CALL","🧪 USDCOP-OTC ☞ 12:43 🦅 CALL","🧪 USDCOP-OTC ☞ 12:47 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 12:54 🦅 PUT","🧪 USDCOP-OTC ☞ 12:59 🦅 PUT","🧪 USDCOP-OTC ☞ 13:05 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 13:10 🦅 CALL","🧪 USDCOP-OTC ☞ 13:14 🦅 PUT","🧪 USDCOP-OTC ☞ 13:19 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 13:24 🦅 CALL","🧪 USDCOP-OTC ☞ 13:27 🦅 PUT","🧪 USDCOP-OTC ☞ 13:30 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 13:36 🦅 CALL","🧪 USDCOP-OTC ☞ 13:41 🦅 PUT","🧪 USDCOP-OTC ☞ 13:46 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 13:49 🦅 PUT","🧪 USDCOP-OTC ☞ 13:55 🦅 CALL","🧪 USDCOP-OTC ☞ 13:58 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 14:05 🦅 PUT","🧪 USDCOP-OTC ☞ 14:11 🦅 PUT","🧪 USDCOP-OTC ☞ 14:14 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 14:19 🦅 CALL","🧪 USDCOP-OTC ☞ 14:25 🦅 PUT","🧪 USDCOP-OTC ☞ 14:30 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 14:35 🦅 CALL","🧪 USDCOP-OTC ☞ 14:41 🦅 PUT","🧪 USDCOP-OTC ☞ 14:47 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 14:54 🦅 CALL","🧪 USDCOP-OTC ☞ 14:57 🦅 CALL","🧪 USDCOP-OTC ☞ 15:03 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 15:07 🦅 CALL","🧪 USDCOP-OTC ☞ 15:13 🦅 PUT","🧪 USDCOP-OTC ☞ 15:19 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 15:24 🦅 CALL","🧪 USDCOP-OTC ☞ 15:29 🦅 CALL","🧪 USDCOP-OTC ☞ 15:33 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 15:40 🦅 PUT","🧪 USDCOP-OTC ☞ 15:44 🦅 PUT","🧪 USDCOP-OTC ☞ 15:50 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 15:56 🦅 PUT","🧪 USDCOP-OTC ☞ 16:00 🦅 CALL","🧪 USDCOP-OTC ☞ 16:03 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 16:06 🦅 PUT","🧪 USDCOP-OTC ☞ 16:09 🦅 CALL","🧪 USDCOP-OTC ☞ 16:13 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 16:20 🦅 PUT","🧪 USDCOP-OTC ☞ 16:27 🦅 CALL","🧪 USDCOP-OTC ☞ 16:30 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 16:34 🦅 CALL","🧪 USDCOP-OTC ☞ 16:37 🦅 PUT","🧪 USDCOP-OTC ☞ 16:43 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 16:50 🦅 PUT","🧪 USDCOP-OTC ☞ 16:53 🦅 CALL","🧪 USDCOP-OTC ☞ 16:56 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 17:03 🦅 PUT","🧪 USDCOP-OTC ☞ 17:08 🦅 CALL","🧪 USDCOP-OTC ☞ 17:14 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 17:21 🦅 CALL","🧪 USDCOP-OTC ☞ 17:27 🦅 CALL","🧪 USDCOP-OTC ☞ 17:33 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 17:38 🦅 PUT","🧪 USDCOP-OTC ☞ 17:41 🦅 PUT","🧪 USDCOP-OTC ☞ 17:44 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 17:51 🦅 PUT","🧪 USDCOP-OTC ☞ 17:56 🦅 PUT","🧪 USDCOP-OTC ☞ 18:02 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 18:06 🦅 PUT","🧪 USDCOP-OTC ☞ 18:13 🦅 PUT","🧪 USDCOP-OTC ☞ 18:16 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 18:21 🦅 PUT","🧪 USDCOP-OTC ☞ 18:26 🦅 CALL","🧪 USDCOP-OTC ☞ 18:30 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 18:33 🦅 PUT","🧪 USDCOP-OTC ☞ 18:40 🦅 PUT","🧪 USDCOP-OTC ☞ 18:44 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 18:48 🦅 CALL","🧪 USDCOP-OTC ☞ 18:52 🦅 CALL","🧪 USDCOP-OTC ☞ 18:57 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 19:02 🦅 PUT","🧪 USDCOP-OTC ☞ 19:09 🦅 CALL","🧪 USDCOP-OTC ☞ 19:13 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 19:20 🦅 PUT","🧪 USDCOP-OTC ☞ 19:26 🦅 PUT","🧪 USDCOP-OTC ☞ 19:29 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 19:34 🦅 CALL","🧪 USDCOP-OTC ☞ 19:37 🦅 CALL","🧪 USDCOP-OTC ☞ 19:40 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 19:43 🦅 PUT","🧪 USDCOP-OTC ☞ 19:50 🦅 PUT","🧪 USDCOP-OTC ☞ 19:54 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 19:57 🦅 PUT","🧪 USDCOP-OTC ☞ 20:02 🦅 PUT","🧪 USDCOP-OTC ☞ 20:05 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 20:08 🦅 PUT","🧪 USDCOP-OTC ☞ 20:14 🦅 PUT","🧪 USDCOP-OTC ☞ 20:17 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 20:21 🦅 PUT","🧪 USDCOP-OTC ☞ 20:28 🦅 PUT","🧪 USDCOP-OTC ☞ 20:32 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 20:36 🦅 PUT","🧪 USDCOP-OTC ☞ 20:42 🦅 CALL","🧪 USDCOP-OTC ☞ 20:46 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 20:50 🦅 PUT","🧪 USDCOP-OTC ☞ 20:55 🦅 PUT","🧪 USDCOP-OTC ☞ 21:02 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 21:06 🦅 PUT","🧪 USDCOP-OTC ☞ 21:11 🦅 PUT","🧪 USDCOP-OTC ☞ 21:16 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 21:22 🦅 PUT","🧪 USDCOP-OTC ☞ 21:27 🦅 PUT","🧪 USDCOP-OTC ☞ 21:33 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 21:38 🦅 CALL","🧪 USDCOP-OTC ☞ 21:41 🦅 PUT","🧪 USDCOP-OTC ☞ 21:47 🦅 PUT",
    "🧪 USDCOP-OTC ☞ 21:52 🦅 CALL","🧪 USDCOP-OTC ☞ 21:56 🦅 CALL","🧪 USDCOP-OTC ☞ 22:03 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 22:08 🦅 PUT","🧪 USDCOP-OTC ☞ 22:11 🦅 PUT","🧪 USDCOP-OTC ☞ 22:18 🦅 CALL",
    "🧪 USDCOP-OTC ☞ 22:25 🦅 CALL","🧪 USDCOP-OTC ☞ 22:28 🦅 CALL","🧪 USDCOP-OTC ☞ 22:33 🦅 CALL",
]

USDEGP_SIGNALS = [
    "🧪 USDEGP-OTC ☞ 09:34 🦅 PUT","🧪 USDEGP-OTC ☞ 09:37 🦅 CALL","🧪 USDEGP-OTC ☞ 09:44 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 09:47 🦅 CALL","🧪 USDEGP-OTC ☞ 09:53 🦅 CALL","🧪 USDEGP-OTC ☞ 09:56 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 10:01 🦅 CALL","🧪 USDEGP-OTC ☞ 10:06 🦅 CALL","🧪 USDEGP-OTC ☞ 10:12 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 10:17 🦅 PUT","🧪 USDEGP-OTC ☞ 10:20 🦅 CALL","🧪 USDEGP-OTC ☞ 10:26 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 10:32 🦅 PUT","🧪 USDEGP-OTC ☞ 10:38 🦅 CALL","🧪 USDEGP-OTC ☞ 10:43 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 10:48 🦅 PUT","🧪 USDEGP-OTC ☞ 10:53 🦅 PUT","🧪 USDEGP-OTC ☞ 11:00 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 11:07 🦅 PUT","🧪 USDEGP-OTC ☞ 11:11 🦅 PUT","🧪 USDEGP-OTC ☞ 11:14 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 11:17 🦅 CALL","🧪 USDEGP-OTC ☞ 11:21 🦅 PUT","🧪 USDEGP-OTC ☞ 11:27 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 11:30 🦅 PUT","🧪 USDEGP-OTC ☞ 11:36 🦅 CALL","🧪 USDEGP-OTC ☞ 11:43 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 11:47 🦅 PUT","🧪 USDEGP-OTC ☞ 11:50 🦅 PUT","🧪 USDEGP-OTC ☞ 11:57 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 12:00 🦅 PUT","🧪 USDEGP-OTC ☞ 12:06 🦅 CALL","🧪 USDEGP-OTC ☞ 12:11 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 12:17 🦅 PUT","🧪 USDEGP-OTC ☞ 12:21 🦅 CALL","🧪 USDEGP-OTC ☞ 12:25 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 12:28 🦅 PUT","🧪 USDEGP-OTC ☞ 12:32 🦅 PUT","🧪 USDEGP-OTC ☞ 12:35 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 12:38 🦅 CALL","🧪 USDEGP-OTC ☞ 12:42 🦅 PUT","🧪 USDEGP-OTC ☞ 12:46 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 12:52 🦅 PUT","🧪 USDEGP-OTC ☞ 12:56 🦅 CALL","🧪 USDEGP-OTC ☞ 13:02 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 13:07 🦅 CALL","🧪 USDEGP-OTC ☞ 13:10 🦅 PUT","🧪 USDEGP-OTC ☞ 13:15 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 13:18 🦅 CALL","🧪 USDEGP-OTC ☞ 13:22 🦅 CALL","🧪 USDEGP-OTC ☞ 13:28 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 13:33 🦅 CALL","🧪 USDEGP-OTC ☞ 13:39 🦅 PUT","🧪 USDEGP-OTC ☞ 13:42 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 13:49 🦅 CALL","🧪 USDEGP-OTC ☞ 13:52 🦅 CALL","🧪 USDEGP-OTC ☞ 13:59 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 14:04 🦅 PUT","🧪 USDEGP-OTC ☞ 14:11 🦅 PUT","🧪 USDEGP-OTC ☞ 14:14 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 14:19 🦅 PUT","🧪 USDEGP-OTC ☞ 14:23 🦅 CALL","🧪 USDEGP-OTC ☞ 14:26 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 14:32 🦅 PUT","🧪 USDEGP-OTC ☞ 14:36 🦅 PUT","🧪 USDEGP-OTC ☞ 14:42 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 14:46 🦅 CALL","🧪 USDEGP-OTC ☞ 14:53 🦅 CALL","🧪 USDEGP-OTC ☞ 14:57 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 15:02 🦅 PUT","🧪 USDEGP-OTC ☞ 15:07 🦅 CALL","🧪 USDEGP-OTC ☞ 15:10 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 15:13 🦅 CALL","🧪 USDEGP-OTC ☞ 15:20 🦅 CALL","🧪 USDEGP-OTC ☞ 15:26 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 15:30 🦅 CALL","🧪 USDEGP-OTC ☞ 15:37 🦅 CALL","🧪 USDEGP-OTC ☞ 15:43 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 15:50 🦅 PUT","🧪 USDEGP-OTC ☞ 15:54 🦅 PUT","🧪 USDEGP-OTC ☞ 16:00 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 16:04 🦅 CALL","🧪 USDEGP-OTC ☞ 16:10 🦅 CALL","🧪 USDEGP-OTC ☞ 16:13 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 16:19 🦅 PUT","🧪 USDEGP-OTC ☞ 16:23 🦅 CALL","🧪 USDEGP-OTC ☞ 16:29 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 16:32 🦅 PUT","🧪 USDEGP-OTC ☞ 16:39 🦅 CALL","🧪 USDEGP-OTC ☞ 16:46 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 16:50 🦅 PUT","🧪 USDEGP-OTC ☞ 16:53 🦅 CALL","🧪 USDEGP-OTC ☞ 17:00 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 17:06 🦅 PUT","🧪 USDEGP-OTC ☞ 17:09 🦅 PUT","🧪 USDEGP-OTC ☞ 17:12 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 17:17 🦅 CALL","🧪 USDEGP-OTC ☞ 17:24 🦅 CALL","🧪 USDEGP-OTC ☞ 17:31 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 17:34 🦅 PUT","🧪 USDEGP-OTC ☞ 17:38 🦅 CALL","🧪 USDEGP-OTC ☞ 17:42 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 17:48 🦅 CALL","🧪 USDEGP-OTC ☞ 17:52 🦅 CALL","🧪 USDEGP-OTC ☞ 17:59 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 18:02 🦅 CALL","🧪 USDEGP-OTC ☞ 18:08 🦅 CALL","🧪 USDEGP-OTC ☞ 18:12 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 18:18 🦅 CALL","🧪 USDEGP-OTC ☞ 18:21 🦅 CALL","🧪 USDEGP-OTC ☞ 18:28 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 18:32 🦅 PUT","🧪 USDEGP-OTC ☞ 18:39 🦅 CALL","🧪 USDEGP-OTC ☞ 18:42 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 18:45 🦅 CALL","🧪 USDEGP-OTC ☞ 18:49 🦅 PUT","🧪 USDEGP-OTC ☞ 18:53 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 18:59 🦅 PUT","🧪 USDEGP-OTC ☞ 19:05 🦅 CALL","🧪 USDEGP-OTC ☞ 19:11 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 19:18 🦅 CALL","🧪 USDEGP-OTC ☞ 19:21 🦅 PUT","🧪 USDEGP-OTC ☞ 19:24 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 19:27 🦅 CALL","🧪 USDEGP-OTC ☞ 19:32 🦅 PUT","🧪 USDEGP-OTC ☞ 19:39 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 19:46 🦅 PUT","🧪 USDEGP-OTC ☞ 19:53 🦅 CALL","🧪 USDEGP-OTC ☞ 19:59 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 20:03 🦅 CALL","🧪 USDEGP-OTC ☞ 20:10 🦅 PUT","🧪 USDEGP-OTC ☞ 20:16 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 20:19 🦅 CALL","🧪 USDEGP-OTC ☞ 20:22 🦅 CALL","🧪 USDEGP-OTC ☞ 20:28 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 20:35 🦅 CALL","🧪 USDEGP-OTC ☞ 20:38 🦅 PUT","🧪 USDEGP-OTC ☞ 20:44 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 20:49 🦅 CALL","🧪 USDEGP-OTC ☞ 20:54 🦅 PUT","🧪 USDEGP-OTC ☞ 21:00 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 21:03 🦅 PUT","🧪 USDEGP-OTC ☞ 21:10 🦅 PUT","🧪 USDEGP-OTC ☞ 21:14 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 21:19 🦅 CALL","🧪 USDEGP-OTC ☞ 21:23 🦅 PUT","🧪 USDEGP-OTC ☞ 21:29 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 21:33 🦅 PUT","🧪 USDEGP-OTC ☞ 21:38 🦅 CALL","🧪 USDEGP-OTC ☞ 21:41 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 21:47 🦅 PUT","🧪 USDEGP-OTC ☞ 21:53 🦅 PUT","🧪 USDEGP-OTC ☞ 21:59 🦅 CALL",
    "🧪 USDEGP-OTC ☞ 22:06 🦅 PUT","🧪 USDEGP-OTC ☞ 22:13 🦅 PUT","🧪 USDEGP-OTC ☞ 22:18 🦅 PUT",
    "🧪 USDEGP-OTC ☞ 22:24 🦅 PUT","🧪 USDEGP-OTC ☞ 22:28 🦅 CALL","🧪 USDEGP-OTC ☞ 22:33 🦅 PUT",
]

# ==================== TRACKER ====================
class WinLossTracker:
    def __init__(self):
        self.stats = {'total': 0, 'wins': 0, 'losses': 0}
        self.history = []
    
    def add_result(self, signal_data, result, signal_id):
        if signal_id in processed_results: return
        processed_results.add(signal_id)
        if result == 'WIN': self.stats['wins'] += 1
        elif result == 'LOSS': self.stats['losses'] += 1
        self.stats['total'] += 1
        self.history.append({
            'asset': signal_data['asset'].replace('-OTC', ''),
            'time': signal_data['converted_time'],
            'direction': signal_data['direction'],
            'result': result,
            'date': datetime.now().strftime('%d/%m/%Y %I:%M %p')
        })
        if len(self.history) > 200: self.history = self.history[-200:]
        self.save()
    
    def get_rate(self):
        if self.stats['total'] == 0: return 0
        return (self.stats['wins'] / self.stats['total']) * 100
    
    def get_history_text(self, limit=30):
        if not self.history: return "📋 No history yet"
        recent = self.history[-limit:]
        text = "📊 SIGNAL HISTORY\n\nPAIR      TIME   DIR   RESULT\n" + "─"*35 + "\n"
        w = l = 0
        for sig in recent:
            pair = sig['asset'][:8]; time = sig['time']
            dir_short = 'CAL' if sig['direction'] == 'CALL' else 'PUT'
            if sig['result'] == 'WIN': res = '✅ WIN'; w += 1
            else: res = '❌ LOS'; l += 1
            text += f"{pair:<8}  {time}  {dir_short}   {res}\n"
        text += "─"*35 + f"\nTOT: {w+l} | W:{w} L:{l} | WR:{self.get_rate():.1f}%\n" + "─"*35
        return text
    
    def reset_stats(self):
        self.stats = {'total': 0, 'wins': 0, 'losses': 0}; self.history = []
        processed_results.clear()
        self.save()
        if os.path.exists(HISTORY_FILE): os.remove(HISTORY_FILE)
    
    def save(self):
        try:
            with open(HISTORY_FILE, 'w') as f: 
                json.dump({'stats': self.stats, 'history': self.history, 'processed': list(processed_results)}, f)
        except: pass
    
    def load(self):
        try:
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'r') as f:
                    data = json.load(f)
                self.stats = data.get('stats', {'total': 0, 'wins': 0, 'losses': 0})
                self.history = data.get('history', [])
                for sid in data.get('processed', []): processed_results.add(sid)
        except: pass

tracker = WinLossTracker()

# ==================== PER-USER DATA ====================
def get_ud(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            'scheduled_signals': {}, 'active_tasks': {}, 'pending_results': {},
            'martingale_step': {}, 'channels': [DEFAULT_CHANNEL], 'current_channel': DEFAULT_CHANNEL
        }
    return user_data[user_id]

# ==================== HELPERS ====================
def to_font(text):
    font_map = {
        'A':'𝘼','B':'𝘽','C':'𝘾','D':'𝘿','E':'𝙀','F':'𝙁','G':'𝙂','H':'𝙃','I':'𝙄','J':'𝙅','K':'𝙆','L':'𝙇','M':'𝙈',
        'N':'𝙉','O':'𝙊','P':'𝙋','Q':'𝙌','R':'𝙍','S':'𝙎','T':'𝙏','U':'𝙐','V':'𝙑','W':'𝙒','X':'𝙓','Y':'𝙔','Z':'𝙕',
        'a':'𝙖','b':'𝙗','c':'𝙘','d':'𝙙','e':'𝙚','f':'𝙛','g':'𝙜','h':'𝙝','i':'𝙞','j':'𝙟','k':'𝙠','l':'𝙡','m':'𝙢',
        'n':'𝙣','o':'𝙤','p':'𝙥','q':'𝙦','r':'𝙧','s':'𝙨','t':'𝙩','u':'𝙪','v':'𝙫','w':'𝙬','x':'𝙭','y':'𝙮','z':'𝙯',
        '0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵',
    }
    return ''.join(font_map.get(c, c) for c in str(text))

def parse_signals(text_or_list):
    signals = []
    lines = text_or_list if isinstance(text_or_list, list) else text_or_list.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line: continue
        clean = line.replace('🧪', '').replace('🦅', '').replace('🐻', '').replace('🦁', '').strip()
        match = re.search(r'([A-Za-z0-9-]+(?:-OTC)?)\s*☞\s*(\d{1,2}:\d{2})\s*(CALL|PUT)', clean, re.IGNORECASE)
        if not match: match = re.search(r'([A-Za-z0-9-]+(?:-OTC)?)\s+(\d{1,2}:\d{2})\s+(CALL|PUT)', clean, re.IGNORECASE)
        if match: signals.append({'asset': match.group(1).strip(), 'time': match.group(2).strip(), 'direction': match.group(3).upper()})
    return signals

def convert_time(time_str):
    try:
        h, m = map(int, time_str.split(':')); total = h * 60 + m - 30
        if total < 0: total += 1440
        return f"{(total//60)%24:02d}:{total%60:02d}"
    except: return time_str

def get_conf(): return random.randint(82, 98)

def get_mg_step(user_id, asset):
    ud = get_ud(user_id); ms = ud['martingale_step']
    if asset not in ms: ms[asset] = 1
    step = ms[asset]; ms[asset] = step + 1 if step < 3 else 1
    return step

# ==================== KEYBOARDS ====================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Load Signals", callback_data="load")],
        [InlineKeyboardButton("📊 Scheduled", callback_data="signals"), InlineKeyboardButton("📈 Stats", callback_data="stats")],
        [InlineKeyboardButton("📋 History", callback_data="history"), InlineKeyboardButton("📝 Pending", callback_data="pending")],
        [InlineKeyboardButton("📢 Channels", callback_data="channels"), InlineKeyboardButton("🔄 Reset", callback_data="reset")],
        [InlineKeyboardButton("🗑️ Clear", callback_data="clear")]
    ])

def asset_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇧🇷 USDBRL", callback_data="asset_USDBRL")],
        [InlineKeyboardButton("🇨🇴 USDCOP", callback_data="asset_USDCOP")],
        [InlineKeyboardButton("🇪🇬 USDEGP", callback_data="asset_USDEGP")],
        [InlineKeyboardButton("🔀 MIXED (No Duplicate Time)", callback_data="asset_MIXED")],
        [InlineKeyboardButton("🔙 Back", callback_data="start")]
    ])

def ch_kb(user_id):
    ud = get_ud(user_id); cur = ud['current_channel']
    btns = []
    for ch in ud['channels'][:6]:
        m = "🟢 " if ch == cur else ""
        btns.append([InlineKeyboardButton(f"{m}{ch}", callback_data=f"ch_{ch}")])
    btns.append([InlineKeyboardButton("➕ Add", callback_data="ch_new")])
    btns.append([InlineKeyboardButton("✅ Use Current", callback_data="ch_skip")])
    btns.append([InlineKeyboardButton("🔙 Back", callback_data="start")])
    return InlineKeyboardMarkup(btns)

def res_kb(sid):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ MTG1 WIN", callback_data=f"w_{sid}"), InlineKeyboardButton("❌ MTG1 LOSS", callback_data=f"l_{sid}")]
    ])

# ==================== FORMATTERS ====================
def fmt_signal(sig, sid, ch):
    a = sig['asset']; t = sig['converted_time']; d = sig['direction']; m = sig.get('martingale_step', 1)
    if d == 'CALL': de = "🟢"; di = "📈"; dl = "CALL / BUY"
    else: de = "🔴"; di = "📉"; dl = "PUT / SELL"
    return f"""
╔══════════════════════════════════╗
║     🎯 TRADING SIGNAL     ║
╚══════════════════════════════════╝

💎 ASSET
   └─ {to_font(a)}

⏰ TRADE TIME (UTC+5:30)
   └─ {to_font(t)}

📊 DIRECTION
   └─ {de} {dl} {di}

🔄 MTG1 STEP
   └─ Step {m} (1x)

╔══════════════════════════════════╗
║  ⚡ PREMIUM SIGNAL • ACTIVE ⚡  ║
║  📱 {ch}              ║
╚══════════════════════════════════╝

⚠️ MTG1 Step {m} • Use proper RM
"""

def fmt_result(sig, result, sid, ch):
    a = sig['asset']; t = sig['converted_time']; d = sig['direction']
    if result == 'WIN': ri = "✅"; rt = "WINNER"
    else: ri = "❌"; rt = "LOSS"
    p = a.replace('-OTC', '')
    return f"""
╔══════════════════════════════════╗
║    📊 SIGNAL RESULT     ║
╚══════════════════════════════════╝

{ri} {rt}

💎 {to_font(p)} | ⏰ {t} | {'🟢' if d == 'CALL' else '🔴'} {d}

📊 Stats: {tracker.stats['wins']}W/{tracker.stats['losses']}L | Rate: {tracker.get_rate():.1f}%

╔══════════════════════════════════╗
║  📱 {ch}              ║
╚══════════════════════════════════╝
"""

# ==================== CALLBACK HANDLER ====================
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; d = q.data; uid = q.from_user.id
    await q.answer()
    ud = get_ud(uid)
    
    # Results
    if d.startswith('w_') or d.startswith('l_'):
        sid = d[2:]; result = 'WIN' if d[0] == 'w' else 'LOSS'
        if sid in processed_results: await q.edit_message_text("⚠️ Already recorded!"); return
        if sid not in ud['pending_results']: await q.edit_message_text("⚠️ Not found"); return
        info = ud['pending_results'][sid]; sd = info['signal']
        tracker.add_result(sd, result, sid)
        ch = ud['current_channel']
        try: await context.bot.send_message(chat_id=ch, text=fmt_result(sd, result, sid, ch))
        except: pass
        e = "✅" if result == 'WIN' else "❌"; sh = sid[-4:] if len(sid) >= 4 else sid
        await q.edit_message_text(f"{e} MTG1 #{sh}\n📊 {sd['asset']}\n⏰ {sd['converted_time']}\n🎯 {result}\n📈 {tracker.get_rate():.1f}%")
        if sid in ud['pending_results']: del ud['pending_results'][sid]
        return
    
    # Asset selection
    if d.startswith('asset_'):
        asset = d[6:]
        context.user_data['selected_asset'] = asset
        await q.edit_message_text(f"📢 Select channel for {asset}:", reply_markup=ch_kb(uid))
        return
    
    # Channel select
    if d.startswith('ch_'):
        ch = d[3:]
        if ch == 'new':
            context.user_data['wait'] = True
            await q.edit_message_text("📝 Send username:\n@my_channel")
            return
        if ch == 'skip': sel = ud['current_channel']
        else: sel = ch; ud['current_channel'] = sel
        if sel not in ud['channels']: ud['channels'].insert(0, sel)
        
        asset = context.user_data.get('selected_asset', 'MIXED')
        act = context.user_data.get('pact', '')
        
        if act == 'history':
            hist = tracker.get_history_text(30)
            try:
                await context.bot.send_message(chat_id=sel, text=f"```\n{hist}\n```", parse_mode=ParseMode.MARKDOWN)
                await q.edit_message_text(f"✅ Posted to {sel}", reply_markup=main_menu())
            except: await q.edit_message_text("❌ Failed", reply_markup=main_menu())
        else:
            await q.edit_message_text(f"✅ {sel}\n⚙️ Loading {asset}...")
            await load_asset_signals(context.bot, uid, sel, asset)
        context.user_data['pact'] = ''
        return
    
    # Menu
    if d == "start":
        ch = ud['current_channel']
        txt = f"""
🤖 SIGNAL BOT v18 FINAL

👤 ID: {uid}
📊 Active: {len(ud['scheduled_signals'])} | Pending: {len(ud['pending_results'])}
📢 Channel: {ch}
📈 Wins: {tracker.stats['wins']} ✅ | Losses: {tracker.stats['losses']} ❌ | WR: {tracker.get_rate():.1f}%
👇 Select:
"""
        await q.edit_message_text(txt, reply_markup=main_menu())
        return
    
    if d == "load":
        await q.edit_message_text("📊 Select Asset:", reply_markup=asset_menu())
        return
    
    if d == "signals":
        if not ud['scheduled_signals']: await q.edit_message_text("📋 None", reply_markup=main_menu()); return
        ss = sorted(ud['scheduled_signals'].items(), key=lambda x: x[1]['scheduled_time'])
        now = datetime.utcnow() + timedelta(hours=5, minutes=30)
        txt = f"📊 YOURS ({len(ss)})\n\n"
        for i, (sid, sd) in enumerate(ss[:10], 1):
            sig = sd['signal']; df = sd['scheduled_time'] - now
            lf = f"{int(df.total_seconds()//60)}m" if df.total_seconds() > 0 else "Now"
            em = "🟢" if sig['direction'] == 'CALL' else "🔴"; sh = sid[-4:] if len(sid) >= 4 else sid
            txt += f"{i}. #{sh} ⏰ {sig['converted_time']} | {em} {sig['direction']} | M{sig.get('martingale_step',1)} | ⏳{lf}\n"
        if len(ss) > 10: txt += f"\n...{len(ss)-10} more"
        await q.edit_message_text(txt, reply_markup=main_menu())
        return
    
    if d == "stats":
        txt = f"📊 MTG1 STATS\n\n├─ Total: {tracker.stats['total']}\n├─ Wins: {tracker.stats['wins']} ✅\n├─ Losses: {tracker.stats['losses']} ❌\n└─ WR: {tracker.get_rate():.1f}%"
        await q.edit_message_text(txt, reply_markup=main_menu())
        return
    
    if d == "history":
        context.user_data['pact'] = 'history'
        await q.edit_message_text("📋 Select group:", reply_markup=ch_kb(uid))
        return
    
    if d == "pending":
        if not ud['pending_results']: await q.edit_message_text("📋 None", reply_markup=main_menu()); return
        for sid, info in list(ud['pending_results'].items())[:1]:
            sig = info['signal']; em = "🟢" if sig['direction'] == 'CALL' else "🔴"; sh = sid[-4:] if len(sid) >= 4 else sid
            await q.edit_message_text(f"📊 #{sh}\n💎 {sig['asset']}\n⏰ {sig['converted_time']}\n📈 {em} {sig['direction']}\n🔄 M{sig.get('martingale_step',1)}\n\nRecord:", reply_markup=res_kb(sid))
        for sid, info in list(ud['pending_results'].items())[1:6]:
            sig = info['signal']; em = "🟢" if sig['direction'] == 'CALL' else "🔴"; sh = sid[-4:] if len(sid) >= 4 else sid
            await q.message.reply_text(f"📊 #{sh}\n💎 {sig['asset']}\n⏰ {sig['converted_time']}\n📈 {em} {sig['direction']}\n🔄 M{sig.get('martingale_step',1)}\n\nRecord:", reply_markup=res_kb(sid))
        return
    
    if d == "channels":
        ch = ud['current_channel']; chs = ud['channels']
        txt = f"📢 CHANNELS\n\n🟢 {ch}\n\n"
        for i, c in enumerate(chs, 1): txt += f"{i}. {c}\n"
        await q.edit_message_text(txt, reply_markup=main_menu())
        return
    
    if d == "reset":
        tracker.reset_stats()
        await q.edit_message_text("✅ Stats & history reset!", reply_markup=main_menu())
        return
    
    if d == "clear":
        for t in list(ud['active_tasks'].values()):
            if not t.done(): t.cancel()
        sc = len(ud['scheduled_signals']); pc = len(ud['pending_results'])
        ud['active_tasks'].clear(); ud['scheduled_signals'].clear(); ud['pending_results'].clear()
        await q.edit_message_text(f"✅ {sc} signals & {pc} pending cleared", reply_markup=main_menu())
        return

# ==================== MESSAGE HANDLER ====================
async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; ud = get_ud(uid)
    
    if context.user_data.get('wait'):
        txt = update.message.text.strip()
        if not txt.startswith('@'): txt = '@' + txt
        ud['current_channel'] = txt
        if txt not in ud['channels']: ud['channels'].insert(0, txt)
        context.user_data['wait'] = False
        asset = context.user_data.get('selected_asset', 'MIXED')
        act = context.user_data.get('pact', '')
        if act == 'history':
            hist = tracker.get_history_text(30)
            try:
                await context.bot.send_message(chat_id=txt, text=f"```\n{hist}\n```", parse_mode=ParseMode.MARKDOWN)
                await update.message.reply_text(f"✅ Posted to {txt}", reply_markup=main_menu())
            except: await update.message.reply_text("❌ Failed", reply_markup=main_menu())
        else:
            await update.message.reply_text(f"✅ {txt}\n⚙️ Loading {asset}...")
            await load_asset_signals(context.bot, uid, txt, asset)
        return
    
    ch = ud['current_channel']
    txt = f"""
🤖 SIGNAL BOT v18 FINAL

👤 ID: {uid}
📊 Active: {len(ud['scheduled_signals'])} | Pending: {len(ud['pending_results'])}
📢 Channel: {ch}
📈 Wins: {tracker.stats['wins']} ✅ | Losses: {tracker.stats['losses']} ❌ | WR: {tracker.get_rate():.1f}%
👇 Select:
"""
    await update.message.reply_text(txt, reply_markup=main_menu())

# ==================== LOAD SIGNALS ====================
async def load_asset_signals(bot, uid, ch, asset):
    ud = get_ud(uid); ud['current_channel'] = ch
    
    if asset == 'USDBRL': signal_list = USDBRL_SIGNALS
    elif asset == 'USDCOP': signal_list = USDCOP_SIGNALS
    elif asset == 'USDEGP': signal_list = USDEGP_SIGNALS
    else: signal_list = USDBRL_SIGNALS + USDCOP_SIGNALS + USDEGP_SIGNALS
    
    parsed = parse_signals(signal_list)
    
    # MIXED: remove duplicate times
    if asset == 'MIXED':
        seen_times = set(); unique_signals = []
        for sig in parsed:
            if sig['time'] not in seen_times:
                seen_times.add(sig['time']); unique_signals.append(sig)
        parsed = unique_signals
    
    ok = 0; fl = 0
    for sig in parsed:
        ct = convert_time(sig['time']); cf = get_conf(); mg = get_mg_step(uid, sig['asset'])
        sd = {'asset': sig['asset'], 'time': sig['time'], 'original_time': sig['time'], 'converted_time': ct, 'direction': sig['direction'], 'confidence': cf, 'martingale_step': mg}
        o, sid = await sched(bot, uid, sd)
        if o: ok += 1
        else: fl += 1
    
    await bot.send_message(chat_id=uid, text=f"✅ {ok} {asset} signals!\n⚠️ {fl} failed\n📢 {ch}\n⏰ UTC+5:30", reply_markup=main_menu())

# ==================== SCHEDULING ====================
async def sched(bot, uid, sd):
    ud = get_ud(uid)
    try:
        h, m = map(int, sd['converted_time'].split(':'))
        now = datetime.utcnow() + timedelta(hours=5, minutes=30)
        tgt = now.replace(hour=h, minute=m, second=0, microsecond=0)
        pt = tgt - timedelta(minutes=1)
        if pt <= now: pt += timedelta(days=1)
        delay = (pt - now).total_seconds()
        if delay < 0: return False, None
        sid = f"{sd['asset']}_{sd['converted_time']}_{random.randint(10000,99999)}"
        ud['scheduled_signals'][sid] = {'signal': sd, 'scheduled_time': pt}
        task = asyncio.create_task(post(bot, uid, sid, sd, delay))
        ud['active_tasks'][sid] = task
        return True, sid
    except: return False, None

async def post(bot, uid, sid, sd, delay):
    ud = get_ud(uid)
    try:
        await asyncio.sleep(delay)
        if sid not in ud['scheduled_signals']: return
        ch = ud['current_channel']
        await bot.send_message(chat_id=ch, text=fmt_signal(sd, sid, ch))
        ud['pending_results'][sid] = {'signal': sd}
        em = "🟢" if sd['direction'] == 'CALL' else "🔴"; sh = sid[-4:] if len(sid) >= 4 else sid
        await bot.send_message(chat_id=uid, text=f"✅ #{sh}\n📊 {sd['asset']}\n⏰ {sd['converted_time']}\n📈 {em} {sd['direction']}\n🔄 M{sd.get('martingale_step',1)}\n📢 {ch}\n\nRecord:", reply_markup=res_kb(sid))
        if sid in ud['scheduled_signals']: del ud['scheduled_signals'][sid]
        if sid in ud['active_tasks']: del ud['active_tasks'][sid]
    except asyncio.CancelledError:
        if sid in ud['scheduled_signals']: del ud['scheduled_signals'][sid]
    except: pass

async def err(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error: {context.error}")

# ==================== MAIN ====================
def main():
    tracker.load()
    print(f"""
╔══════════════════════════════════╗
║  🤖 SIGNAL BOT v18 COMPLETE  ║
║  ALL LOGIC • 4 ASSETS      ║
╚══════════════════════════════════╝
📊 {tracker.stats['wins']}W/{tracker.stats['losses']}L | ✅ Ready!
""")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg))
    app.add_handler(CommandHandler("start", msg))
    app.add_error_handler(err)
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == '__main__':
    main()

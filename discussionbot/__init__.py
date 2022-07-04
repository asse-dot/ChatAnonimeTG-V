import logging
import os
from logging.handlers import TimedRotatingFileHandler
from configparser import ConfigParser
from pyrogram import Client

if not os.path.exists('log'):
    os.makedirs('log')

config = ConfigParser()
config.read('config.ini')

api_hash = config.get("pyrogram", "api_hash")
api_id = config.get("pyrogram", "api_id")
bot_token = config.get("pyrogram", "bot_token")

__version__ = '0.0.0'
__author__ = ""
parse_mode = 'html'
testing_mode = False

logging.basicConfig(
    format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level = logging.WARNING,
    handlers=[
        TimedRotatingFileHandler(
            "log/discussionbot.log",
            when="midnight",
            encoding=None,
            delay=False,
            backupCount=10,
        ),
        logging.StreamHandler(),
    ],
)


bot = Client("DiscussionEasy",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token,
             plugins=dict(root="discussionbot/plugins"))

LOGS = logging.getLogger(__name__)


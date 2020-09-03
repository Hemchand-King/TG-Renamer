#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import time

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import Client, Filters
from pyrogram import ForceReply

from helper_funcs.chat_base import TRChatBase
from helper_funcs.display_progress import progress_for_pyrogram

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
from database.database import *

TEXT = """**Now Send me the name of the new file with extension**\n
If you want to upload as file send in this format 
`New Name.Extention`
If you want to upload as video send the name in this format 
`video - New Name.extention`"""

@pyrogram.Client.on_message(pyrogram.Filters.document & pyrogram.Filters.incoming)
async def doc(bot, update):
 if update.document is not None:
           await bot.send_message(
                 chat_id=update.chat.id,
                 text="""**Now Send me the name of the new file with extension**\n
If you want to upload as file send in this format 
`New Name.Extention`
If you want to upload as video send the name in this format 
`video - New Name.extention`""",
                 parse_mode='Markdown',
                 reply_to_message_id=update.message_id,
                 reply_markup=ForceReply()
                )
           return
@pyrogram.Client.on_message(pyrogram.Filters.text)
async def rename_doc(bot, update):
 if update.reply_to_message.text == TEXT:
    await bot.send_message(
            chat_id=updage.message_id,
            text="welcome",
            )
 else:
       await bot.send_message(
            chat_id=updage.message_id,
            text="welcome",
            )

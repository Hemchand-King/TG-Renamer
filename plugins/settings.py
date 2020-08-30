import asyncio
from pyrogram import Client, Filters, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ForceReply
from utils import User
from info import PROCESSING_MSG

import logging
logger = logging.getLogger(__name__)

setting_text = "⚙️ <b>Here you can change bot settings</b>"

required_fields = {'screenshot': 1, 'stream_video': 1, 'receive_updates': 1, 'thumbnail': 1}


def make_setting_kb(user):

    def on_off(value):
        return 'ON' if value else 'OFF'

    buttons = []

    # screenshot
    buttons.append([InlineKeyboardButton(f'📸 Receive screenshots: {on_off(user.screenshot)}',
                                         callback_data=f'screenshot|{not user.screenshot}')])


    # streamable video
    buttons.append([InlineKeyboardButton(f'🎞 Upload as video: {on_off(user.stream_video)}',
                                         callback_data=f'stream_video|{not user.stream_video}')])

    # thumbnail
    thumbnail_text = '🏞 See custom thumbnail' if user.thumbnail else '🏞 Set custom thumbnail'
    buttons.append([InlineKeyboardButton(thumbnail_text,
                                         callback_data=f'thumbnail|{bool(user.thumbnail)}')])

    # receive updates
    buttons.append([InlineKeyboardButton(f'Receive bot updates: {on_off(user.receive_updates)}',
                                         callback_data=f'updates|{not user.receive_updates}')])

    return InlineKeyboardMarkup(buttons)


@Client.on_message(Filters.command('settings') & Filters.incoming)
async def settings(bot, message):

    logger.debug('settings command')
    msg = await message.reply(PROCESSING_MSG, quote=True)
    chat_id = message.chat.id
    try:

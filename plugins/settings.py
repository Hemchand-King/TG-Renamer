import asyncio
from pyrogram import Client, Filters, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ForceReply
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
        user = await get_userdata(chat_id, required_fields)
    except:
        logger.exception('Database error in bot settings')
        await msg.edit('**Something went wrong!**\n\nPlease report this issue on @botxSupport')
    else:
        markup = make_setting_kb(user)
        await msg.edit(setting_text, reply_markup=markup, parse_mode='html')



@Client.on_callback_query(Filters.regex(r'^updates\|(True|False)'))
async def bot_updates_setting(bot, update):

    chat_id = update.from_user.id
    receive_updates = True if 'True' in update.data else False
    user = await get_userdata(chat_id, required_fields)
    user.receive_updates = receive_updates
    if receive_updates:
        await update.answer()
    else:
        await update.answer('You will no longer receive bot updates (not recommended)',
                            show_alert=True)
        
    markup = make_setting_kb(user)
    await asyncio.gather(
        user.commit(),
        update.message.edit(setting_text, reply_markup=markup, parse_mode='html'))


@Client.on_callback_query(Filters.regex(r'^(stream_video|screenshot)\|(True|False)'))
async def change_setting(bot, update):

    await update.answer()
    chat_id = update.from_user.id
    key = update.data.split('|')[0]
    value = True if 'True' in update.data else False
    user = await get_userdata(chat_id, required_fields)
    user[key] = value
    markup = make_setting_kb(user)
    await asyncio.gather(
        user.commit(),
        update.message.edit(setting_text, reply_markup=markup, parse_mode='html'))


@Client.on_callback_query(Filters.regex(r'^thumbnail\|(True|False)'))
async def thumbnail_setting(bot, update):

    chat_id = update.from_user.id
    value = True if 'True' in update.data else False

    if not value:
        await update.answer(
            'Send photo or reply /set_thumbnail to any photo to set it as a custom thumbnail', 
            show_alert=True)
    else:
        user = await get_userdata(chat_id, required_fields)
        try:
            await asyncio.gather(
                update.answer(),
                bot.send_photo(chat_id, user.thumbnail, caption='👆 Custom thumbnail'))
        except:
            # logger.exception('Failed to send thumbnail')
            user.thumbnail = None
            await user.commit()
            markup = make_setting_kb(user)
            await asyncio.gather(
                update.answer('You have to set custom thumbnail again', show_alert=True),
                update.message.edit(setting_text, reply_markup=markup, parse_mode='html'))


async def get_userdata(chat_id, required_fields=None):

    fields = {} if required_fields is None else required_fields
    user = await User.find_one({'chat_id': chat_id}, fields)
    if not user:
        user = User(chat_id=chat_id)
        await user.commit()
    return user

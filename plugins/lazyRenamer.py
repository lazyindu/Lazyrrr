"""
Apache License 2.0
Copyright (c) 2023 @LazyDeveloper
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
Dev Channel Link : https://t.me/LazyDeveloper 
Repo Link : https://github.com/LazyDeveloperr/LazyPrincess
License Link : https://github.com/LazyDeveloperr/LazyPrincess/blob/main/LICENSE
# Removing this is strictly prohibited ! Don't remove this all without the 
permission of LazyDeveloperr
"""

from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
import humanize
from info import ADMINS , FLOOD, LAZY_MODE, LAZY_RENAMERS
import random



@Client.on_message(filters.private & (filters.document | filters.audio | filters.video) & filters.user(ADMINS))
async def rename_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size) 
    fileid = file.file_id
    try:
        text = f"""**__What do you want me to do with this file.?__**\n\n**🪬New Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
        buttons = [[ InlineKeyboardButton("📝✧✧ S𝚝ar𝚝 re𝚗aᗰi𝚗g ✧✧📝", callback_data="rename") ],
                   [ InlineKeyboardButton("⨳  C L Ф S Ξ  ⨳", callback_data="close_data") ]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
        await sleep(FLOOD)
    except FloodWait as e:
        await sleep(e.value)
        text = f"""**__What do you want me to do with this file.?__**\n\n**🪬New Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
        buttons = [[ InlineKeyboardButton("📝✧✧ S𝚝ar𝚝 re𝚗aᗰi𝚗g ✧✧📝", callback_data="rename") ],
                   [ InlineKeyboardButton("⨳  C L Ф S Ξ  ⨳", callback_data="close_data") ]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
    except:
        pass



@Client.on_message((filters.forwarded & filters.private & filters.user(LAZY_RENAMERS) (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text ))
async def lazyDev(bot, message):
  if message.from_user.id in LAZY_RENAMERS:
        if (LAZY_MODE==True):
            file = getattr(message, message.media.value)
            filename = file.file_name
            filesize = humanize.naturalsize(file.file_size) 
            buttons = [
                [
                    InlineKeyboardButton("📝✧✧ S𝚝ar𝚝 re𝚗aᗰi𝚗g ✧✧📝", callback_data="rename") 
                ],
                [
                    InlineKeyboardButton('⨳  C L Ф S Ξ  ⨳', callback_data='close_data'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            return await message.reply(
                f'I am currently in **Lazy_Mode**.\nHey **Sweet-Heart** - Please tell me what should i do with this file !\n\n🪬Chat ID/ Username: <code>{chat_id}</code>\nℹ️Last Message ID: <code>{last_msg_id}</code> \n\n🎞**File Name** :- `{filename}`\n\n⚙️**File Size** :- `{filesize}`',
                reply_to_message_id=message.id,
                reply_markup=reply_markup)
            

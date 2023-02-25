from database.lazy_utils import progress_for_pyrogram, convert, humanbytes
from pyrogram import Client, filters
from pyrogram.types import (ForceReply)
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from database.users_chats_db import db
from database.lazy_set import escape_invalid_curly_brackets
from database.lazy_ffmpeg import take_screen_shot, fix_thumb
from datetime import timedelta
import os 
import random
import humanize
from PIL import Image
import time


@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    date_fa = str(update.message.date)
    pattern = '%Y-%m-%d %H:%M:%S'
    date = int(time.mktime(time.strptime(date_fa, pattern)))
    chat_id = update.message.chat.id
    id = update.message.reply_to_message_id
    await update.message.delete()
    await update.message.reply_text(f"__Please enter the new filename...__\n\nNote:- Extension Not Required",
                                    reply_to_message_id=id,
                                    reply_markup=ForceReply(True))
	

@Client.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    type = update.data.split("_")[1]
    new_name = update.message.text
    name = new_name.split(":-")
    new_filename = os.path.basename(name[1])  # remove any directory path from new_filename
    dest_dir = "downloads"  # specify the directory to which the file should be moved after renaming
    file_path = os.path.join(dest_dir, new_filename)
    message = update.message.reply_to_message
    file = message.document or message.video or message.audio
    ms = await update.message.edit("⚠️__**Please wait...**__\n__Downloading file to my server...__")
    c_time = time.time()
    try:
        path = await bot.download_media(
            message=file,
            progress=progress_for_pyrogram,
            progress_args=("\n⚠️__**Please wait...**__\n\nRenaming in progress...**", ms, c_time)
        )
    except Exception as e:
        await ms.edit(e)
        return 
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name =f"downloads/{dow_file_name}"
    # Ensure that the destination directory exists before renaming the file
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    os.rename(old_file_name, file_path)
    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds
    
    user_id = int(update.message.chat.id) 
    ph_path = None 
    media = getattr(file, file.media.value)
    c_caption = await db.get_caption(update.message.chat.id)
    c_thumb = await db.get_thumbnail(update.message.chat.id)
    if c_caption:
        vid_list = ["filename", "filesize", "duration"]
        new_tex = escape_invalid_curly_brackets(c_caption, vid_list)
        caption = new_tex.format(filename=new_filename, filesize=humanbytes(
            file.file_size), duration=timedelta(seconds=duration))
    else:
        caption = f"**{new_filename}**"
    if (media.thumbs or c_thumb):
        if c_thumb:
           ph_path = await bot.download_media(c_thumb) 
        else:
           ph_path = await bot.download_media(media.thumbs[0].file_id)
           Image.open(ph_path).convert("RGB").save(ph_path)
           img = Image.open(ph_path)
           img.resize((320, 320))
           img.save(ph_path, "JPEG")
           c_time = time.time()
    else:
        try:
            ph_path_ = await take_screen_shot(file_path, os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
            width, height, ph_path = await fix_thumb(ph_path_)
        except Exception as e:
            ph_path = None
            print(e)

    await ms.edit("⚠️__**Please wait...**__\n__Processing file upload....__")
    c_time = time.time() 
    try:
       if type == "document":
          await bot.send_document(
	    update.message.chat.id,
                   document=file_path,
                   thumb=ph_path, 
                   caption=caption, 
                   progress=progress_for_pyrogram,
                   progress_args=( "⚠️__**Please wait...**__\n__Processing file upload....__",  ms, c_time   ))
       elif type == "video": 
           await bot.send_video(
	    update.message.chat.id,
	    video=file_path,
	    caption=caption,
	    thumb=ph_path,
	    duration=duration,
	    progress=progress_for_pyrogram,
	    progress_args=( "⚠️__**Please wait...**__\n__Processing file upload....__",  ms, c_time))
       elif type == "audio": 
           await bot.send_audio(
	    update.message.chat.id,
	    audio=file_path,
	    caption=caption,
	    thumb=ph_path,
	    duration=duration,
	    progress=progress_for_pyrogram,
	    progress_args=( "⚠️__**Please wait...**__\n__Processing file upload....__",  ms, c_time   )) 
    except Exception as e: 
        await ms.edit(f" Erro {e}") 
        os.remove(file_path)
        if ph_path:
          os.remove(ph_path)
        return 
    await ms.delete() 
    os.remove(file_path) 
    if ph_path:
       os.remove(ph_path) 



# @Client.on_callback_query(filters.regex("upload"))
# async def doc(bot, update):
#     type = update.data.split("_")[1]
#     new_name = update.message.text
#     name = new_name.split(":-")
#     new_filename = name[1]
#     file_path = f"downloads/{new_filename}"
#     message = update.message.reply_to_message
#     file = message.document or message.video or message.audio
#     ms = await update.message.edit("⚠️__**Please wait...**__\n__Downloading file to my server...__")
#     c_time = time.time()
#     try:
#         path = await bot.download_media(
#             message=file,
#             progress=progress_for_pyrogram,
#             progress_args=("\n⚠️__**Please wait...**__\n\nRenaming in progress...**", ms, c_time)
#         )
#     except Exception as e:
#         await ms.edit(e)
#         return 
#     splitpath = path.split("/downloads/")
#     dow_file_name = splitpath[1]
#     old_file_name =f"downloads/{dow_file_name}"
#     # Ensure that the destination directory exists before renaming the file
#     dest_dir = os.path.dirname(file_path)
#     if not os.path.exists(dest_dir):
#         os.makedirs(dest_dir)
#         os.rename(old_file_name, file_path)
#     duration = 0
#     metadata = extractMetadata(createParser(file_path))
#     if metadata.has("duration"):
#         duration = metadata.get('duration').seconds
    
#     user_id = int(update.message.chat.id) 
#     ph_path = None 
#     media = getattr(file, file.media.value)
#     c_caption = await db.get_caption(update.message.chat.id)
#     c_thumb = await db.get_thumbnail(update.message.chat.id)
#     if c_caption:
#         vid_list = ["filename", "filesize", "duration"]
#         new_tex = escape_invalid_curly_brackets(c_caption, vid_list)
#         caption = new_tex.format(filename=new_filename, filesize=humanbytes(
#             file.file_size), duration=timedelta(seconds=duration))
#     else:
#         caption = f"**{new_filename}**"
#     if (media.thumbs or c_thumb):
#         if c_thumb:
#            ph_path = await bot.download_media(c_thumb) 
#         else:
#            ph_path = await bot.download_media(media.thumbs[0].file_id)
#            Image.open(ph_path).convert("RGB").save(ph_path)
#            img = Image.open(ph_path)
#            img.resize((320, 320))
#            img.save(ph_path, "JPEG")
#            c_time = time.time()
#     else:
#         try:
#             ph_path_ = await take_screen_shot(file_path, os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
#             width, height, ph_path = await fix_thumb(ph_path_)
#         except Exception as e:
#             ph_path = None
#             print(e)

#     await ms.edit("⚠️__**Please wait...**__\n__Processing file upload....__")
#     c_time = time.time() 
#     try:
#        if type == "document":
#           await bot.send_document(
# 	    update.message.chat.id,
#                    document=file_path,
#                    thumb=ph_path, 
#                    caption=caption, 
#                    progress=progress_for_pyrogram,
#                    progress_args=( "⚠️__**Please wait...**__\n__Processing file upload....__",  ms, c_time   ))
#        elif type == "video": 
#            await bot.send_video(
# 	    update.message.chat.id,
# 	    video=file_path,
# 	    caption=caption,
# 	    thumb=ph_path,
# 	    duration=duration,
# 	    progress=progress_for_pyrogram,
# 	    progress_args=( "⚠️__**Please wait...**__\n__Processing file upload....__",  ms, c_time))
#        elif type == "audio": 
#            await bot.send_audio(
# 	    update.message.chat.id,
# 	    audio=file_path,
# 	    caption=caption,
# 	    thumb=ph_path,
# 	    duration=duration,
# 	    progress=progress_for_pyrogram,
# 	    progress_args=( "⚠️__**Please wait...**__\n__Processing file upload....__",  ms, c_time   )) 
#     except Exception as e: 
#         await ms.edit(f" Erro {e}") 
#         os.remove(file_path)
#         if ph_path:
#           os.remove(ph_path)
#         return 
#     await ms.delete() 
#     os.remove(file_path) 
#     if ph_path:
#        os.remove(ph_path) 

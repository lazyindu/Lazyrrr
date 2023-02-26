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
async def rename(bot,update):
	user_id = update.message.chat.id
	date = update.message.date
	await update.message.delete()
	await update.message.reply_text("__𝙿𝚕𝚎𝚊𝚜𝚎 𝙴𝚗𝚝𝚎𝚛 𝙽𝚎𝚠 𝙵𝚒𝚕𝚎𝙽𝚊𝚖𝚎...__",	
	reply_to_message_id=update.message.reply_to_message.id,  
	reply_markup=ForceReply(True))  


@Client.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    type = update.data.split("_")[1]
    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    file_path = f"downloads/{new_filename}"
    # if new_filename:
    #     await bot.send_message(text=f"Name updated: {new_filename}")
    # else:
    #     await bot.send_message(text=f"Name did'nt updatd")
    #     return
    # message = update.message.reply_to_message
    # file = message.document or message.video or message.audio
    file = update.message.reply_to_message
    ms = await update.message.edit("\n__Downloading file to my server...__")
    c_time = time.time()
    try:
        path = await bot.download_media(
                message=file,
                progress=progress_for_pyrogram,
                progress_args=("**__\n\nRenaming in progress...**", ms, c_time))
    except Exception as e:
        await ms.edit(e)
        return 
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name =f"downloads/{dow_file_name}"
    # Ensure that the destination directory exists before renaming the file
    # dest_dir = os.path.dirname(file_path)
    # if not os.path.exists(dest_dir):
    #     os.makedirs(dest_dir)
    os.rename(old_file_name, file_path)
    duration = 0
    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
           duration = metadata.get('duration').seconds
    except:
        pass
    user_id = int(update.message.chat.id) 
    ph_path = None 
    media = getattr(file, file.media.value)
    c_caption = await db.get_caption(update.message.chat.id)
    c_thumb = await db.get_thumbnail(update.message.from_user.id)
    if c_caption:
         try:
             caption = c_caption.format(filename=new_filename, filesize=humanize.naturalsize(media.file_size), duration=convert(duration))
         except Exception as e:
             await ms.edit(text=f"Your caption Error unexpected keyword ●> ({e})")
             return 
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
    await ms.edit("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....")
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
# async def doc(bot,update):
#      type = update.data.split("_")[1]
#      new_name = update.message.text
#      new_filename = new_name.split(":-")[1]
#      file_path = f"downloads/{new_filename}"
#      file = update.message.reply_to_message
#      ms = await update.message.edit("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳...")
#      c_time = time.time()
#      try:
#      	path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳....",  ms, c_time   ))
#      except Exception as e:
#      	await ms.edit(e)
#      	return 
#      splitpath = path.split("/downloads/")
#      dow_file_name = splitpath[1]
#      old_file_name =f"downloads/{dow_file_name}"
#      os.rename(old_file_name,file_path)
#      duration = 0
#      try:
#         metadata = extractMetadata(createParser(file_path))
#         if metadata.has("duration"):
#            duration = metadata.get('duration').seconds
#      except:
#         pass
#      user_id = int(update.message.chat.id) 
#      ph_path = None 
#      media = getattr(file, file.media.value)
#      c_caption = await db.get_caption(update.message.chat.id)
#      c_thumb = await db.get_thumbnail(update.message.chat.id)
#      if c_caption:
#          try:
#              caption = c_caption.format(filename=new_filename, filesize=humanize.naturalsize(media.file_size), duration=convert(duration))
#          except Exception as e:
#              await ms.edit(text=f"Your caption Error unexpected keyword ●> ({e})")
#              return 
#      else:
#          caption = f"**{new_filename}**"
#      if (media.thumbs or c_thumb):
#          if c_thumb:
#             ph_path = await bot.download_media(c_thumb) 
#          else:
#             ph_path = await bot.download_media(media.thumbs[0].file_id)
#          Image.open(ph_path).convert("RGB").save(ph_path)
#          img = Image.open(ph_path)
#          img.resize((320, 320))
#          img.save(ph_path, "JPEG")
#      await ms.edit("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....")
#      c_time = time.time() 
#      try:
#         if type == "document":
#            await bot.send_document(
# 		    update.message.chat.id,
#                     document=file_path,
#                     thumb=ph_path, 
#                     caption=caption, 
#                     progress=progress_for_pyrogram,
#                     progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....",  ms, c_time   ))
#         elif type == "video": 
#             await bot.send_video(
# 		    update.message.chat.id,
# 		    video=file_path,
# 		    caption=caption,
# 		    thumb=ph_path,
# 		    duration=duration,
# 		    progress=progress_for_pyrogram,
# 		    progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....",  ms, c_time))
#         elif type == "audio": 
#             await bot.send_audio(
# 		    update.message.chat.id,
# 		    audio=file_path,
# 		    caption=caption,
# 		    thumb=ph_path,
# 		    duration=duration,
# 		    progress=progress_for_pyrogram,
# 		    progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....",  ms, c_time   )) 
#      except Exception as e: 
#          await ms.edit(f" Erro {e}") 
#          os.remove(file_path)
#          if ph_path:
#            os.remove(ph_path)
#          return 
#      await ms.delete() 
#      os.remove(file_path) 
#      if ph_path:
#         os.remove(ph_path) 

	

# @Client.on_callback_query(filters.regex("upload"))
# async def doc(bot, update):
#     type = update.data.split("_")[1]
#     new_name = update.message.text
#     name = new_name.split(":-")
#     new_filename = name[1]
#     file_path = f"downloads/{new_filename}"
#     message = update.message.reply_to_message
    
#     # Check if update.message is not None before accessing its properties
#     if not message:
#         await update.answer("Please reply to a message to upload a file.")
#         return
    
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




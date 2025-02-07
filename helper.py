from pyrogram import Client as bot, filters
import os, sys, aiofiles, asyncio
from config import Config
import msg, io, master.key as key
from datetime import datetime, timedelta
import pytz, subprocess, shutil
from main import LOGGER
import requests, cloudscraper
from database import db, standarddb
from urllib.parse import unquote
scraper = cloudscraper.create_scraper()

thumb = "thumb.jpg" if subprocess.getstatusoutput(f"wget '{Config.THUMB_URL}' -O 'thumb.jpg'")[0] == 0 else None
IST = pytz.timezone('Asia/Kolkata')  

@bot.on_message(filters.command("status") & filters.private)
async def status_command(_, m):
    if m.chat.id not in Config.ADMIN_ID:
        await m.reply_text("You are not authorized to use this command.")
        return
    subscriber_count = await db.db_instance.get_subscription_count()
    await m.reply_text(f"Number of subscribers: {subscriber_count}")

@bot.on_message(filters.command("id"))
async def get_chat_id(_, m):
    await m.reply_text(f"<blockquote><b>The ID of this chat id is:</b></blockquote> `{m.chat.id}`")

@bot.on_message(filters.command("restart") & filters.private)
async def stop_handler(_, m):
    if m.chat.id not in Config.ADMIN_ID:
        return await m.reply_text("You are not authorized to use this command.")
    await m.reply_text("🚦**STOPPED**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("broadcast") & filters.private)
async def broadcast(bot, m):
    if m.chat.id not in Config.ADMIN_ID: 
        return await m.reply_text("You are not authorized to use this command.")
    
    parts = m.text.split(maxsplit=1)
    
    if len(parts) < 2:
        return await m.reply_text("Usage: /broadcast <message> or /broadcast -v for video broadcast")
    
    if parts[1] == "-v":
        await m.reply_text("Please send the video or photo with a caption that you want to broadcast.")
        media_message = await bot.listen(chat_id=m.chat.id)  
        media_file_id = None
        caption = media_message.caption or ""

        if media_message.video:
            media_file_id = media_message.video.file_id
            media_type = "video"
        elif media_message.photo:
            media_file_id = media_message.photo.file_id  # Highest quality photo
            media_type = "photo"

        if media_file_id:
            subscribers = await db.db_instance.get_subscribers_collections()
            async for subscriber in subscribers:
                try:
                    if media_type == "video":
                        await bot.send_video(subscriber['_id'], media_file_id, caption=caption)
                    elif media_type == "photo":
                        await bot.send_photo(subscriber['_id'], media_file_id, caption=caption)
                except Exception as e:
                    print(f"Failed to send {media_type} to user {subscriber['_id']}: {e}")
            return await m.reply_text(f"{media_type.capitalize()} broadcast completed.")
        else:
            return await m.reply_text("No video or photo found. Please try again.")
    
    message = parts[1]
    subscribers = await db.db_instance.get_subscribers_collections()
    async for subscriber in subscribers:
        try:
            await bot.send_message(subscriber['_id'], message)
        except Exception as e:
            LOGGER.error(f"Failed to send message to user {subscriber['_id']}: {e}")

    await m.reply_text("Broadcast completed.")




@bot.on_message(filters.command("removeallfiles") & filters.private)
async def remove_all_files_handler(_, m):
    if m.chat.id not in Config.ADMIN_ID:
        return await m.reply_text("You are not authorized to use this command.")
    await db.db_instance.remove_all_backup_files()
    await m.reply_text("All backup files have been removed.")

@bot.on_message(filters.command("myfiles") & filters.private)
async def myfiles_handler(bot, m):
    user_id = m.chat.id
    backup_files = await db.db_instance.get_backup_files(user_id)
    if not backup_files:
        await m.reply_text("You have no saved files.")
        return
    for file in backup_files:
        file_data = io.BytesIO(file['file_data'])
        file_name = file['file_name'] 
        async with aiofiles.open(file_name, 'wb') as f:
            await f.write(file_data.read())
        try:
            await bot.send_document(
                chat_id=m.chat.id,
                document=file_name,
                caption=file['caption']
            )
            await asyncio.sleep(1)
        finally:
            os.remove(file_name)

@bot.on_message(filters.command("allbackupfiles") & filters.private)
async def all_backup_files_handler(bot, m):
    if m.chat.id not in Config.ADMIN_ID:
        return await m.reply_text("You are not authorized to use this command.")
    all_files = await db.db_instance.get_all_backup_files()
    if not all_files:
        return await m.reply_text("No backup files found.")
    for file in all_files:
        file_data = io.BytesIO(file['file_data'])
        file_name = file['file_name'] 
        async with aiofiles.open(file_name, 'wb') as f:
            await f.write(file_data.read())
        try:
            await bot.send_document(chat_id=m.chat.id,document=file_name,caption=file['caption'])
        finally:
            os.remove(file_name)

@bot.on_message(filters.command("remove") & filters.private)
async def remove_command(bot, m):
    if m.chat.id not in Config.ADMIN_ID:
        return await m.reply_text("You are not authorized to use this command.")
    parts = m.text.split()
    if len(parts) != 2:
        return await m.reply_text("Usage: /remove user_id")
    user_id = int(parts[1])
    try:
        await db.db_instance.remove_user_from_premium(user_id)
        await bot.send_message(user_id, "<blockquote><b><i>Your account has been removed from Premium User<blockquote></b></i>.")
        await m.reply_text(f"User {user_id} has been removed.")
    except Exception as e:
        await m.reply_text(f"Error removing user: {e}")

@bot.on_message(filters.command("auth") & filters.private)
async def add_premium_command(bot, m):
    if m.chat.id not in Config.ADMIN_ID:
        return await m.reply_text("You are not authorized to use this command.")
    
    # Get the full message text and split it by lines (to handle multiple /auth commands)
    commands = m.text.strip().splitlines()

    # Process each command
    for command in commands:
        parts = command.split()
        
        # Check if the command has the correct format
        if len(parts) < 4 or parts[0] != "/auth":
            return await m.reply_text("<b>Usage: <u>/auth user_id days type</u></b>")
        
        try:
            user_id = int(parts[1])
            days = int(parts[2])
            subscription_type = parts[3]
            
            # Fetch the user details
            user = await bot.get_users(user_id)
            
            # Add premium status to the user in the database
            await db.db_instance.add_premium(user_id, days, subscription_type)
            
            # Create a description for the subscription type
            type_description = f"<blockquote>{getattr(msg, subscription_type)}</blockquote>"
            
            # Notify the user
            await bot.send_message(
                user_id, 
                msg.auth.format(user.first_name, user_id, type_description, days), 
                disable_web_page_preview=True
            )
            
            # Log the action to admin log channel
            try:
                await bot.send_message(
                    Config.AUTH_LOG, 
                    msg.auth.format(user.first_name, user_id, type_description, days), 
                    disable_web_page_preview=True
                )
            except Exception as e:
                await m.reply_text(f"Error logging premium status: {e}")
            
            # Confirm to the admin that the premium status has been added
            await m.reply_text(f"Premium status added for user {user_id}.")
        
        except Exception as e:
            # Send error message if there's an issue
            await m.reply_text(f"Error adding premium status for user {user_id}: {e}")


@bot.on_message(filters.command("myplan") & filters.private)
async def myplan_handler(_, m):
    user_id = m.from_user.id
    user_data = await db.db_instance.get_premium_user(user_id)
    if user_data:
        start_at = user_data.get('start_at')
        expires_at = user_data.get('expires_at')
        subscription_type = user_data.get('subscription_type')
        if start_at.tzinfo is None:
            start_at = IST.localize(start_at)
        if expires_at.tzinfo is None:
            expires_at = IST.localize(expires_at)
        now_ist = datetime.now(IST)
        plan_duration = expires_at - start_at if start_at and expires_at else timedelta(0)
        time_left = expires_at - now_ist if expires_at else timedelta(0)     
        response = (
            "<b>Plan Details</b>\n"
            f"<blockquote><b>{getattr(msg, subscription_type)}</blockquote></b>\n\n"
            f"<b>Join Date:</b> <i>{start_at.strftime('%Y-%m-%d %H:%M:%S')}</i>\n"
            f"<b>Expiry Date:</b> <i>{expires_at.strftime('%Y-%m-%d %H:%M:%S')}</i>\n"
            f"<b>Plan Duration:</b> <i>{plan_duration}</i>\n"
            f"<b>Time Remaining:</b> <i>{time_left} ⏳</i>\n\n"
            "<blockquote><b>Enjoy exclusive benefits and features! 🎉🚀</b></blockquote>"
        )
        await m.reply_text(response, disable_web_page_preview=True)
    else:
        await m.reply_text(msg.UPGRADE, reply_markup=key.contact())

@bot.on_message(filters.command("authlist") & filters.private)
async def authlist_handler(bot, m):
    if m.chat.id not in Config.ADMIN_ID:
        await m.reply_text("You are not authorized to use this command.")
        return
    premium_users_cursor = await db.db_instance.get_premium_collection()
    auth_list = []
    async for user in premium_users_cursor:
        user_id = int(user['_id'])
        try:
            user_info = await bot.get_users(user_id)
            first_name = user_info.first_name
        except:
            first_name = "Unknown"
        start_at = user.get('start_at')
        expires_at = user.get('expires_at')
        subscription_type = user.get('subscription_type', 'Unknown')
        if start_at and start_at.tzinfo is None:
            start_at = IST.localize(start_at)
        if expires_at and expires_at.tzinfo is None:
            expires_at = IST.localize(expires_at)
        start_at_str = start_at.strftime('%Y-%m-%d %H:%M:%S') if start_at else 'N/A'
        expires_at_str = expires_at.strftime('%Y-%m-%d %H:%M:%S') if expires_at else 'N/A'
        auth_list.append(
            f"User: [{first_name}](tg://openmessage?user_id={user_id})\n"
            f"Subscription Type: {subscription_type}\n"
            f"Start: {start_at_str}\n"
            f"Expires: {expires_at_str}\n"
        )
    if not auth_list:
        await m.reply_text("No any authorized users.")
    else:
        await m.reply_text("\n".join(auth_list))


async def clear_handler():
    extensions_to_clear = [".mp4", ".jpg", ".png", ".mkv", ".pdf", ".ts", ".m4a", ".mpd", ".m3u8", ".json", ".txt"]
    files_cleared = False
    directory = os.getcwd()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(tuple(extensions_to_clear)):
                os.remove(os.path.join(root, file))
                files_cleared = True
    temp_dir = os.path.join(directory, "temp")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        files_cleared = True 
    if files_cleared:
        LOGGER.info("✅**Files with specified extensions and temp directory cleared successfully!**✅")
    else:
        LOGGER.info("No files with specified extensions were found, and temp directory was not present.")

@bot.on_message(filters.command("stop") & filters.private)
async def stop_handler(_, m):
    user_id = m.from_user.id
    is_admin = user_id in Config.ADMIN_ID
    is_premium = await db.db_instance.get_premium_user(user_id)
    if not is_admin and not is_premium:
        await m.reply_text(msg.UPGRADE, reply_markup=key.contact())
        return
    await clear_handler()
    await m.reply_text("🚦**STOPPED**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command("saveapi") & filters.private)
async def saved_api_in_db(bot, m):
    user_id = int(m.chat.id)
    user = await bot.get_users(user_id)
    contact_link = f"[{user.first_name}](tg://openmessage?user_id={user_id})"
    has_access, _ = await db.db_instance.access_checking(user_id)
    if not has_access:
        await m.reply_text("<i>Betaa Tum log ke liye nhi hai... phle plan lo fir anguli kro</i>")
        return
    message1 = await m.reply_text("<b><i>Please send AppName:API or Website </b></i>(e.g., <blockquote>UC Live: https://ucliveapi.classx.co.in\nUC Live: https://uclive.co/</blockquote>)\n\n⚠️Warn: <b>शुद्ध हिंदी भाषा में...वही APK की API add करें जो apk list me add ना है अगर मुझे पता चला कि किसी ने गांड में उंगली की hai तो उसको अपने प्लान से लाट मारके निकाल दूंगा उसके बाद अपनी गांड में उंगली करना</b>", disable_web_page_preview=True)
    input1 = await bot.listen(chat_id=m.chat.id); await input1.delete()
    text1 = input1.text.strip()
    if ':' in text1:
        appname, api = text1.split(':', 1)
        appname = appname.strip()
        api = api.strip()
        if "api" in api:
            try:
                response = requests.get(api)
                if response.status_code == 200:
                    await standarddb.db_instance.insert_or_update_appx_api(appname, api)
                    await message1.edit_text(f"<i>API for <b>{appname}</b> saved successfully.</i>")
                    await bot.send_message(Config.OWNER, f"<i>API for <b>{appname}</b> saved successfully. And Saved by {contact_link}</i>")
                else:
                    await message1.edit_text("<b><i>Please reverify your API. It seems the API server is down.</b></i>")
            except requests.RequestException:
                await message1.edit_text("<b><i>Invalid API URL or unable to reach the server.</b></i>")
        else:
            response = scraper.get(api)
            cookie_parts = response.headers.get("Set-Cookie", "").split(";")
            api = ""
            for part in cookie_parts:
                if part.strip().startswith("base_url="):
                    api = unquote(part.strip()[9:])
                    break
            if api:
                await standarddb.db_instance.insert_or_update_appx_api(appname, api)
                await message1.edit_text(f"<i>API for <b>{appname}</b> saved successfully.</i>")
                await bot.send_message(Config.OWNER, f"<i>API for <b>{appname}</b> saved successfully. And Saved by {contact_link}</i>")
                LOGGER.info("Base URL: %s", api)
            else:
                LOGGER.info("Base URL not found in Set-Cookie header")
                await message1.edit("**Oopss... Please check your website this is not an appx website**\n\n**How to check appx url -** Tap on this website https://makeiteasy.classx.co.in/\n\n**If your webpage is looking like as similar then your website is appx website**")
                return
    else:
        await message1.edit_text("<b><i>Invalid format. Please use: AppName:API (e.g., UC Live: https://ucliveapi.classx.co.in)</b></i>")

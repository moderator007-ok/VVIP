from pyrogram import filters, Client as bot
from modules import (
    awadhfree, ifasfree, verbalfree, cdsfree, icsfree, pw, khan, kd, cp, neon,
    appx_master, testlivefree, utk, kaksha, pwfree, khanfree, iq,
    vision, nidhi, cpfree, allen, iqfree, ifas, pathfree,
    allenv2, abhinavfree, vajiram, qualityfree, jrffree, cw
)
import master.key as key, msg
from config import Config
from database import db
import buttom

@bot.on_message(filters.command("start") & filters.private)
async def start_msg(bot, m):
    user_id = int(m.chat.id)
    await db.db_instance.save_subscriber(user_id)
    if not await join_channel_if_needed(bot, m):
        return
    user_mention = m.from_user.mention
    await bot.send_photo(m.chat.id,photo=await key.send_random_photo(),caption=msg.START.format(user_mention),reply_markup=key.join_user())

@bot.on_message(filters.command("upgrade") & filters.private)
async def upgrade_msg(bot, m):
    if not await join_channel_if_needed(bot, m):
        return
    await bot.send_photo(m.chat.id,photo=await key.send_random_photo(), caption=msg.UPGRADE, reply_markup=key.contact())

@bot.on_message(filters.command("app"))
async def start_app(bot, m):
    if not await join_channel_if_needed(bot, m):
        return
    user_id = int(m.chat.id)
    await bot.send_photo(chat_id=user_id,photo=await key.send_random_photo(),caption=msg.APP,reply_markup=buttom.home())


@bot.on_callback_query()
async def callback_handler(bot, callback_query):
    if not await join_channel_if_needed(bot, callback_query.message):
        return
    data = callback_query.data
    call_msg = callback_query.message
    a = callback_query.answer
    if data == "home":
        await call_msg.edit_reply_markup(buttom.home())
    elif data == "close":
        await call_msg.delete()
    elif data.startswith("ack_page"):
        page = int(data.split("_")[-1]) - 1
        await call_msg.edit_reply_markup(buttom.gen_app_kb(page))
    elif data.startswith("page_"):
        page = int(data.split("_")[1])
        await call_msg.edit_reply_markup(buttom.gen_app_kb(page))
    elif data.startswith("ext_page"):
        page = int(data.split("_")[-1]) + 1
        await call_msg.edit_reply_markup(buttom.gen_app_kb(page))
    elif data == "abhinavfree":#1
        await a("You choose Abhinav Maths without Login", show_alert=True)
        await abhinavfree.abhinav_math_free(bot, call_msg)
    elif data == "cpfree":#2
        await a("⚠️ In Classplus: I can't extract the PDF URL but You can extract Video Url of Some Apk", show_alert=True)
        await cpfree.handle_cpfree_logic(bot, call_msg)
    elif data == "pathsalafree":#3
        await a("You choose My Pathsala without Login", show_alert=True)
        await pathfree.path_free(bot, call_msg)
    elif data == "awadhfree":#4
        await a("You choose Awadh Ojha Sir Without Login ", show_alert=True)
        await awadhfree.awadh_ojha_free(bot, call_msg)
    elif data == "pwfree":#5
        await a("⚠️ In Physics Wallah: I can't extract the PDF URL", show_alert=True)
        await pwfree.handle_pw_free_logic(bot, call_msg)
    elif data == "iqfree":#6
        await a("You choose Study Iq Without Login", show_alert=True)
        await iqfree.iqfree_logic(bot, call_msg)
    elif data == "khanfree":#7
        await a("You choose Khan Gs Without Login ", show_alert=True)
        await khanfree.handle_khan_free_logic(bot, call_msg)
    elif data == "cdsfree":#8
        await a("You choose Cds Journey Without Login ", show_alert=True)
        await cdsfree.handle_cds_logic(bot, call_msg)
    elif data == "testpaperlivefree":#9
        await a("You choose Test Paper Live Without Login", show_alert=True)
        await testlivefree.handle_test_logic(bot, call_msg)
    elif data == "icsfree":#10
        await a("You choose ICS Coaching Without Login", show_alert=True)
        await icsfree.handle_ics_logic(bot, call_msg)
    elif data == "careerwill":#10
        await a("You choose CareerWill", show_alert=True)
        await cw.handle_cw_logic(bot, call_msg)
    elif data == "sunyafree":#11
        await a("Please wait!... Work in progress", show_alert=True)
    elif data == "qualityfree":#12
        await a("You choose Quality Education ", show_alert=True)
        await qualityfree.handle_quality_logic(bot, call_msg)
    elif data == "appxfree":  # Line 11
        await a("Congrats! You Can extract all appx batches..", show_alert=True)
        markup, _, _ = await key.gen_apps_free_kb()
        await call_msg.edit_reply_markup(reply_markup=markup)
    elif data.startswith("free_"):
        await key.handle_app(bot, data, call_msg, a)
    elif data.startswith("forward_"):
        page = int(data.split('_')[1])
        await key.appx_page(call_msg, page)
    elif data.startswith("previous_"):
        page = int(data.split('_')[1])
        await key.appx_page(call_msg, page)
    elif data == "verbalfree":#12
        await a("Congrats! You Can extract all Verbal Maths batches..", show_alert=True)
        await verbalfree.verbal_math(bot, call_msg)
    elif data == "dsl":#12
        await a("Please wait!... Work in progress", show_alert=True)
    elif data == "ifasfree":#12
        await a("Congrats! You Can extract all IFAS Batches..", show_alert=True)
        await ifasfree.ifas_logic(bot, call_msg)
    elif data == "addafree":#13
        await a("Please wait!... Work in progress", show_alert=True)
        #await awadh.awadh_ojha_free(bot, call_msg)
    elif data == "testbookfree":#13
        await a("Please wait!... Work in progress", show_alert=True)
        #await awadh.awadh_ojha_free(bot, call_msg)
    elif data == "forumfree":#15
        await a("Please wait!... Work in progress or Contact Developer", show_alert=True)
        #await iqfree.iqfree_logic(bot, call_msg)

    elif data == "edukemy":#D
        await a("Work on Progress.....", show_alert=True)
    elif data == "jrffree":
        await a("You choose JRF Adda Free Extractor ", show_alert=True)
        await jrffree.jrf_adda_free(bot, call_msg)
    elif data == "vajiram":
        await a("You choose Vajiram IAS ", show_alert=True)
        await vajiram.vajiram_ias(bot, call_msg)
    elif data == "iq":
        await a("You choose Study Iq ", show_alert=True)
        await iq.handle_iq_logic(bot, call_msg)
    elif data == "ifas":
        await a("You choose IFAS Online ", show_alert=True)
        await ifas.ifas_logic(bot, call_msg)
    elif data == "vision":
        await a("You choose Vision IAS ", show_alert=True)
        await vision.handle_vision_logic(bot, call_msg)
    elif data == "nidhi":
        await a("You choose Nidhi Academy ", show_alert=True)
        await nidhi.handle_nidhi_logic(bot, call_msg)
    elif data == "master":
        await a("You choose Master AppxApi ", show_alert=True)
        await appx_master.handle_app_paid(bot,call_msg)
    elif data == "pw":#D
        await a("You choose Physics Wallah ", show_alert=True)
        await pw.handle_pw_logic(bot, call_msg)
    elif data == "cp":#D
        await a("You choose ClassPlus ", show_alert=True)
        await cp.handle_cp_logic(bot, call_msg)
    elif data == "allen":
        await a("You choose Allen Institute", show_alert=True)
        await allen.handle_allen_logic(bot, call_msg)
    elif data == "allenv2":
        await a("You choose Allen Institute", show_alert=True)
        await allenv2.handle_allenV2_logic(bot, call_msg)
    elif data == "khan":#D
        await a("You choose Khan Gs ", show_alert=True)
        await khan.handle_khan_logic(bot, call_msg)
    elif data == "kd":
        await a("You choose Kd Campus Live", show_alert=True)
        await kd.handle_kd_logic(bot, call_msg)
    elif data == "adda":
        await a("Please wait!... Work in progress", show_alert=True)
    elif data == "neon":
        await a("You choose Neon Classes", show_alert=True)
        await neon.handle_neon_logic(bot, call_msg)
    elif data == "utk":
        await a("You choose Utkarsh", show_alert=True)
        await utk.handle_utk_logic(bot, call_msg)
    elif data == "kaksha":
        await a("You choose Apni Kaksha", show_alert=True)
        await kaksha.handle_kaksha_logic(bot, call_msg)


async def check_channel_membership(bot, m):
    try:
        member = await bot.get_chat_member(Config.CHANNEL, m.chat.id)
        if member.status == "left" or member.status == "kicked":
            return False
    except:
        return False
    return True

async def join_channel_if_needed(bot, m):
    if not await check_channel_membership(bot, m):
        await m.reply_text("<b><u>Please join our channel to access this feature.</b></u>", reply_markup=key.join_user())
        return False
    return True

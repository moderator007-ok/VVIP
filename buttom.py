from pyrogram.types import InlineKeyboardButton as KB, InlineKeyboardMarkup as KM


def gen_app_kb(page):
    if page == 1:
        keyboard = [
            [KB("🌐 All Appx API APP [Web Url or API] 🌐", callback_data="master")],
            [KB("📱 All ClassPlus APK 📱", callback_data="cp")],
            [KB("🔑 ClassPlus Token Generator 🔑", callback_data="token")],
            [KB("📘 Edukemy 📘", callback_data="edukemy"), KB("📗 Apni Kaksha 📗", callback_data="kaksha")],
            [KB("📕 Khan GS 📕", callback_data="khan")],
            [KB("📙 Neon Classes 📙", callback_data="neon")],
            [KB("🎓 Nidhi Academy 🎓", callback_data="nidhi"), KB("🎥 KD LIVE 🎥", callback_data="kd")],
            [KB("📚 Physics Wallah 📚", callback_data="pw")],
            [KB("👨‍🏫 Tarun Grover Sir 👨‍🏫", callback_data="tarun")],
            [KB("🏫 My Pathsala 🏫", callback_data="path"), KB("📝 CareerWill 📝", callback_data="careerwill")],
            [KB("🌟 My Rising India 🌟", callback_data="rising")],
            [KB("🩺 Nursing Next 🩺", callback_data="nursing")],
            [KB("⏩ Next Page ➡️", callback_data="ext_page_1")]
        ]
    elif page == 2:
        keyboard = [
            [KB("🎯 Allen New V2 🎯", callback_data="allenv2")],
            [KB("🚀 Allen Institute 🚀", callback_data="allen")],
            [KB("🎓 IFAS Academy 🎓", callback_data="ifas"), KB("🧑‍🏫 ICS Coaching 🧑‍🏫", callback_data="ics")],
            [KB("🌟 Sanskriti IAS 🌟", callback_data="rising")],
            [KB("🩺 Nursing Next 🩺", callback_data="nursing")],
            [KB("💡 Study IQ 💡", callback_data="iq"), KB("🏆 Utkarsh 🏆", callback_data="utk")],
            [KB("📚 Forum IAS 📚", callback_data="forum")],
            [KB("🔍 Vision IAS 🔍", callback_data="vision")],
            [KB("💼 Insight IAS 💼", callback_data="insight"), KB("📝 Vajiram IAS 📝", callback_data="vajiram")],
            [KB("🔑 Sunya IAS 🔑", callback_data="sunya")],
            [KB("📈 Level UP IAS 📈", callback_data="level")],
            [KB("🏅 Next IAS 🏅", callback_data="next"), KB("🔧 MadeEasy 🔧", callback_data="madeeasy")],
            [KB("🌐 WebSankul 🌐", callback_data="webs")],
            [KB("💻 All Spayee Websites 💻", callback_data="spayee")],
            [KB("💻 DSL KrantiKari 💻", callback_data="dsl")],
            [KB("🔙 Back Page ⬅️", callback_data="ack_page_2"), KB("🏠 Home 🏠", callback_data="home"), KB("➡️ Next Page ➡️", callback_data="ext_page_2")]
        ]
    elif page == 3:
        keyboard = [
            [KB("🌐 Appx All API (Nothing Required) 🌐", callback_data="appxfree")],
            [KB("🎲 Adda 247 (Any Random Login) 🎲", callback_data="addafree")],
            [KB("📘 Abhinav Maths (Nothing Required) 📘", callback_data="abhinavfree")],
            [KB("🚀 CDS Journey (Any Random Login) 🚀", callback_data="cdsfree")],
            [KB("📱 ClassPlus (Org Code Required) 📱", callback_data="cpfree")],
            [KB("🎓 Awadh Ojha App (Nothing Required) 🎓", callback_data="awadhfree")],
            [KB("📕 Khan Sir (Nothing Required) 📕", callback_data="khanfree")],
            [KB("🧑‍🏫 ICS Coaching (Any Random Login) 🧑‍🏫", callback_data="icsfree")],
            [KB("🧑‍🏫 IFAS Academy (Any Random Login) 🧑‍🏫", callback_data="ifasfree")],
            [KB("📚 Forum IAS (Any Random Token) 📚", callback_data="forumfree")],
            [KB("📚 JRF Adda (Nothing Required) 📚", callback_data="jrffree")],
            [KB("🏫 My Pathsala (Nothing Required) 🏫", callback_data="pathsalafree")],
            [KB("🔑 Physics Wallah (Any Random Token) 🔑", callback_data="pwfree")],
            [KB("🎓 Quality Education (Nothing Required) 🎓", callback_data="qualityfree")],
            [KB("💡 Study IQ (Nothing Required) 💡", callback_data="iqfree")],
            [KB("📘 Sunya IAS (Nothing Required) 📘", callback_data="sunyafree")],
            [KB("📝 Test Paper (Nothing Required) 📝", callback_data="testpaperlivefree")],
            [KB("🎯 TestBook (Any Random Login) 🎯", callback_data="testbookfree")],
            [KB("🚀 Verbal Math (Nothing Required)🚀 ", callback_data="verbalfree")],
            [KB("🔙 Back Page ⬅️", callback_data="ack_page_3"), KB("❌ Close ❌", callback_data="close"), KB("🏠 Home 🏠", callback_data="home")]
        ]
    return KM(keyboard)


def home():
    keyboard = [
        [KB("🌟 VIP (Normal App) 🤖", callback_data="page_1"), KB("🚀 PRO (Special App) 🚀", callback_data="page_2")],
        [KB("⚡ Legend (No Login Required) ⚡", callback_data="page_3")],
        [KB("❌ Close ❌", callback_data="close")]
    ]
    return KM(keyboard)

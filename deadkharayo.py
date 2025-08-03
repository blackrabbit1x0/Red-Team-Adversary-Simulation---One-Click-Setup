# deadkharayo.py
import discord
from discord.ext import commands
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import os
import json
from flask import Flask, send_file
import threading
import asyncio

# Load config
with open('config.json') as f:
    config = json.load(f)

DISCORD_TOKEN = config['discord_token']
CHANNEL_ID = int(config['channel_id'])
SMTP_USER = config['smtp_user']
SMTP_PASS = config['smtp_pass']
TRACKING_PIXEL_URL = config['tracking_url']
SMTP_HOST = 'smtp-relay.brevo.com'
SMTP_PORT = 587
PIXEL_IMAGE_PATH = 'pixel.png'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
flask_app = Flask(__name__)

@flask_app.route('/pixel.png')
def track_email_open():
    asyncio.run_coroutine_threadsafe(notify_open(), bot.loop)
    return send_file(PIXEL_IMAGE_PATH, mimetype='image/png')

async def notify_open():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("📬 Someone **opened** the phishing email!")

def start_flask():
    flask_app.run(host='0.0.0.0', port=80)

@bot.event
async def on_ready():
    print(f"✅ DeadKharayo is online as {bot.user}")

@bot.command()
async def sendmail(ctx):
    def check(m): return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("📨 Enter recipient email:")
    recipient = (await bot.wait_for('message', check=check)).content

    await ctx.send("✉️ Enter email subject:")
    subject = (await bot.wait_for('message', check=check)).content

    await ctx.send("📝 Paste your **HTML code** for the email body below:")
    body = (await bot.wait_for('message', check=check)).content

    await ctx.send("📎 Do you want to attach a file? (yes/no)")
    attach = (await bot.wait_for('message', check=check)).content.lower()

    attachment = None
    file_path = ""
    if attach == "yes":
        await ctx.send("📁 Upload the file now:")
        file_msg = await bot.wait_for('message', check=check)
        if file_msg.attachments:
            attachment = file_msg.attachments[0]
            file_path = f"temp_{attachment.filename}"
            await attachment.save(file_path)
        else:
            await ctx.send("❌ No file uploaded.")
            return

    # Inject tracking pixel
    tracked_body = body + f'<img src="{TRACKING_PIXEL_URL}" width="1" height="1" style="display:none;">'

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(tracked_body, 'html'))

    if attachment:
        with open(file_path, 'rb') as f:
            part = MIMEText(f.read(), 'base64', 'utf-8')
            part.add_header('Content-Disposition', f'attachment; filename="{attachment.filename}"')
            msg.attach(part)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, recipient, msg.as_string())
        await ctx.send(f"✅ Email sent to `{recipient}` successfully.")
    except Exception as e:
        await ctx.send(f"❌ Failed to send email: `{e}`")
    finally:
        if attachment and os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    threading.Thread(target=start_flask).start()
    bot.run(DISCORD_TOKEN)

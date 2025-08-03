# 🛡️ Red Team Adversary Simulation - One Click Setup

## 👾 Overview

This is a **Red Team Adversary Simulation Lab** with a one-click CLI launcher, simulating a full-chain attack using techniques aligned with **MITRE ATT&CK Group G0130: Ajax Security Team**. It includes:

- ✅ **Hardwarica-C2**: A Discord-based Command & Control (C2) implant.
- ✅ **DeadKharayo**: A phishing delivery tool with email tracking and file delivery.
- ✅ **One-Click Launcher**: A CLI-based setup tool to deploy and control the simulation environment.

> Built for controlled labs, this toolkit demonstrates realistic adversary behavior from **Initial Access** to **Impact**, based on TTPs of G0130.

---

## 🧠 MITRE ATT&CK Profile: Ajax Security Team (G0130)

**Group G0130**, known as *Ajax Security Team*, is a threat actor group that has used phishing, custom implants, persistence, and credential access to target users across the Middle East and beyond.

This simulation implements several **real-world techniques used by G0130**, mapped to MITRE ATT&CK as follows:

| Technique                        | Tactic              | ID           | Tool Used            |
|----------------------------------|---------------------|--------------|----------------------|
| Phishing with Malicious Emails   | Initial Access      | T1566.001     | DeadKharayo          |
| Spearphishing Attachment         | Initial Access      | T1566.002     | DeadKharayo          |
| User Execution (File Opening)    | Execution           | T1204.002     | Hardwarica + Decoy   |
| Reverse Shell                    | Command & Control   | T1059.003     | Hardwarica-C2        |
| Registry Run Key Persistence     | Persistence         | T1547.001     | Hardwarica-C2        |
| Credential Access (Browser)      | Credential Access   | T1555.003     | Hardwarica-C2        |
| Keylogging                       | Credential Access   | T1056.001     | Hardwarica-C2        |
| Clipboard Data Collection        | Collection          | T1115         | Hardwarica-C2        |
| Screen Capture                   | Collection          | T1113         | Hardwarica-C2        |
| Webcam Capture                   | Collection          | T1125         | Hardwarica-C2        |
| File Transfer (Ingress/Egress)   | Command & Control   | T1105         | Hardwarica-C2        |
| Self-Destruct Mechanism          | Defense Evasion     | T1070.004     | Hardwarica-C2        |

---

## 🧰 Folder Structure

📁 redteam-lab/
├── launcher.py # One-click CLI launcher for the full simulation
├── hardwarica.py # Discord-based implant with all C2 features
├── deadkharayo.py # Phishing email tool with tracking
├── requirements.txt # Python packages needed
├── README.md # This documentation

---

## 🚀 One-Click Setup

> ⚠️ For use in **offline labs or test environments only**. Do not run on real systems.

### 🔧 Steps:

1. Unzip the folder.
2. Open terminal and run:

```bash
python3 launcher.py

Enter:

Your Discord Bot Token and Guild ID

Your Attacker IP (for reverse shell)

Use menu to:

Launch Hardwarica-C2

Start phishing tool DeadKharayo

Compile implant as .exe

Open Discord in browser

View help/instructions


💣 Hardwarica-C2 Features
📸 !screenshot — Take screenshot

🔑 !keylogger / !dumpkeys — Start keylogging and dump logs

📋 !clipboard — Grab clipboard contents

💻 !revshell — Launch reverse shell

📁 !upload / !download — Transfer files

🛠️ !persist — Add persistence via registry

🔒 !stealcreds — Extract saved browser credentials

📷 !webcam — Capture webcam snapshot

💥 !selfdestruct — Delete implant and clean up

🎣 DeadKharayo Features
Send realistic phishing emails via Discord

Embed tracking pixel to detect email open

Load .eml templates or custom HTML

Support for attachments (e.g., payloads)

Use Brevo SMTP or custom SMTP settings

Reports email opens live in Discord

📦 Requirements
Install via launcher or manually:

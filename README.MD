# 🛡️ Red Team Adversary Simulation - One Click Setup

## 👾 Overview

This project is a **Red Team Adversary Simulation Lab** featuring a one-click command-line interface (CLI) launcher. It simulates a full-chain cyberattack aligned with **MITRE ATT\&CK Group G0130: Ajax Security Team**, incorporating the following tools:

* ✅ **Hardwarica-C2**: A Discord-based Command & Control (C2) implant.
* ✅ **DeadKharayo**: A phishing delivery tool with email tracking and malicious file delivery.
* ✅ **One-Click Launcher**: A CLI tool to orchestrate the simulation environment.

> **Disclaimer**: This toolkit is designed strictly for educational purposes in offline labs and controlled environments. Do not deploy in live or production systems.

---

## 🧠 MITRE ATT\&CK Profile: Ajax Security Team (G0130)

The **Ajax Security Team (G0130)** is a threat actor group known for phishing, custom malware implants, persistence techniques, and credential theft, particularly targeting users in the Middle East.

The table below maps the simulation techniques to their respective MITRE ATT\&CK tactics and tools:

| Technique                      | Tactic            | ATT\&CK ID | Tool Used          |
| ------------------------------ | ----------------- | ---------- | ------------------ |
| Phishing with Malicious Emails | Initial Access    | T1566.001  | DeadKharayo        |
| Spearphishing Attachment       | Initial Access    | T1566.002  | DeadKharayo        |
| User Execution (File Opening)  | Execution         | T1204.002  | Hardwarica + Decoy |
| Reverse Shell                  | Command & Control | T1059.003  | Hardwarica-C2      |
| Registry Run Key Persistence   | Persistence       | T1547.001  | Hardwarica-C2      |
| Credential Access (Browser)    | Credential Access | T1555.003  | Hardwarica-C2      |
| Keylogging                     | Credential Access | T1056.001  | Hardwarica-C2      |
| Clipboard Data Collection      | Collection        | T1115      | Hardwarica-C2      |
| Screen Capture                 | Collection        | T1113      | Hardwarica-C2      |
| Webcam Capture                 | Collection        | T1125      | Hardwarica-C2      |
| File Transfer (Ingress/Egress) | Command & Control | T1105      | Hardwarica-C2      |
| Self-Destruct Mechanism        | Defense Evasion   | T1070.004  | Hardwarica-C2      |

---

## 🧪 Red Team Lab Toolkit

This lab includes the following core components:

* `hardwarica.py` — Discord-based C2 implant.
* `deadkharayo.py` — Phishing tool with embedded pixel tracking.
* `launcher.py` — One-click CLI launcher to manage and run the simulation.
* `requirements.txt` — List of all required Python dependencies.

---

## 🚀 One-Click Setup Guide

### ⚡ Requirements

* Python 3.8+
* Compatible with Linux, macOS, or Windows (for C2 .exe compilation)

### 🛠️ Installation Steps

1. **Extract the Project**

   * Unzip the `redteam-lab/` folder to your local system.

2. **Navigate to the Folder**

   ```bash
   cd redteam-lab
   ```

3. **Run the Launcher Script**

   ```bash
   python3 launcher.py
   ```

---

## 📜 Launcher Configuration Prompts

Upon running, `launcher.py` will prompt for:

* 🔐 **Discord Bot Token**
* 🔐 **Discord Guild ID**
* 🌐 **Attacker IP Address** (used for reverse shell callbacks)

---

## 📋 Launcher Menu Options

* ▶️ **Launch Hardwarica-C2** – Starts the implant and connects to Discord.
* 📧 **Launch DeadKharayo** – Phishing tool with email tracking and payload delivery.
* ⚙️ **Install Dependencies** – Automatically installs Python packages from `requirements.txt`.
* 🖥️ **Compile Implant to .exe** – Converts `hardwarica.py` into a stealthy Windows executable.
* 🖵️ **Open Discord in Browser** – Opens the Discord dashboard for bot and channel monitoring.
* ❓ **Help & Usage Guide** – Provides detailed usage instructions and command descriptions.

---

## ✅ Simulation Output & Results

After successful setup, you will be able to:

* 🌟 Simulate full-chain MITRE ATT\&CK TTPs.
* 📈 Observe live command/control and event logs in Discord.
* 🎯 Demonstrate adversary behavior from Initial Access to Impact.

---

## 📁 Folder Structure

```bash
redteam-lab/
├── launcher.py             # One-click CLI launcher for full simulation
├── hardwarica.py           # Discord-based implant with full C2 capabilities
├── deadkharayo.py          # Phishing email delivery tool with tracking pixel
├── requirements.txt        # Python package dependencies
└── README.md               # Project documentation
```

---

> ⚠️ Always use this toolkit in isolated, controlled environments only. Educational and ethical use only.

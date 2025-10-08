<p align="center">
  <img src="https://owo.whats-th.is/3sSfXgb.png" alt="Mira logo" width="120"/>
</p>

<h1 align="center">Mira</h1>

<p align="center">
  A modular text-to-speech Discord bot for Bay Area public transit systems.
  <br>
  Proudly serving the <a href="https://discord.gg/bayareatransit">Bay Area Transit Discord</a>.
</p>

---

# Supported Voices
- Bay Area Rapid Transit (BART)
  - George (Platform)
  - Gracie (Platform)
  - Sharon (Train)
  - Google (eBART Train)
- Valley Transportation Authority (VTA)
  - Samantha

# Setup
## Requirements
- Windows 10 (preferrably IoT Enterprise LTSC 2021 for minimal resource usage)
- [Python 3.13.7+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

Lucent SAPI4 voices (BART's George and Gracie) require:
- **Active Call Center 2.6.1 Enterprise** (filename: ACC260ESDSetup.exe, SHA-1 hash `6475dd35b48c09c073bd3e82059a822099f875c2`)
- A valid license for Active Call Center

Nuance SAPI5 voices (VTA's Samantha) require:
- **Nuance Vocalizer Expressive 5.2.3** (filename: VEX_ENU_Samantha.zip, SHA-1 hash `7f2a3bc5967ca4698f5a87ad579e76ae4a4cb4c2`)

Both Lucent and Nuance voices require:
- [balcon.exe (Balabolka Command Line Utility)](https://www.cross-plus-a.com/bconsole.htm)

## Installation
1. Install Active Call Center then activate it with a valid license. Install Nuance Vocalizer Expressive.
2. Download and extract balcon.exe to a good place.
3. Install Python and Git, making sure to add Python to PATH.
4. Clone the repository.
```bash
git clone https://github.com/burritosoftware/mira.git
```
5. Install/upgrade dependencies.
```bash
py -m pip install -U -r requirements.txt
```
6. Copy [.env.example](.env.example) to `.env` and fill it in with your Discord bot token and path to balcon.
7. Start the bot with optimizations.
```bash
py -O bot.py
```

# Disclaimer
This project is not affiliated with the San Francisco Bay Area Rapid Transit District or the Santa Clara Valley Transportation Authority.
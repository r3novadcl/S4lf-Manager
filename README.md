# S4lf Manager

A lightweight Discord Selfbot / RPC Manager written in Python.

S4lf Manager provides a command-based control panel for customizing Rich Presence, custom status, dynamic activities, AFK replies, voice-channel presence and text formatting.

> **Important:** This project uses a Discord user account session through `discord.py-self`. Self-bots/user-account automation are not officially supported by Discord and may result in account action. Use this project only for testing/research on an account where you accept that risk.

---

## Features

### RPC / Rich Presence Builder

Create and customize your Discord Rich Presence directly through commands.

Supported options include:

- Activity name
- Activity type
- Details
- State
- Application ID
- Large image
- Large image hover text
- Small image
- Small image hover text
- Up to 2 RPC buttons
- Button labels and URLs
- Start timestamp
- RPC preview/status panel

Example:

```text
.setname Visual Studio Code
.settype 0
.setdetails Editing Python
.setstate Working on a project
.setappid YOUR_APPLICATION_ID
.setlarge your_asset_key
.setlargetext Visual Studio Code
.setsmall python
.setsmalltext Python
.apply
```

### Ready-Made RPC Presets

The project includes predefined RPC presets for popular applications and games.

Available presets include:

- Visual Studio Code
- GitHub
- VALORANT
- Minecraft
- Genshin Impact
- League of Legends
- Fortnite
- Grand Theft Auto V
- Counter-Strike 2
- Roblox
- Apex Legends
- PUBG
- Spotify-style activity
- YouTube-style activity
- Netflix-style activity
- Crunchyroll-style activity

View all presets:

```text
.presets
```

Apply a preset:

```text
.preset valorant
```

---

## Dynamic RPC

Save multiple RPC configurations and automatically rotate between them.

Save the current RPC:

```text
.savedynamic
```

Start rotation:

```text
.dynamic start
```

Stop rotation:

```text
.dynamic stop
```

Clear saved RPCs:

```text
.dynamic clear
```

The manager changes between saved activities automatically.

---

## Custom Status

Set a custom Discord status:

```text
.cs Working on my project
```

Clear the custom status:

```text
.cs
```

### Rotating Custom Status

You can provide multiple statuses separated with `|`:

```text
.csrotate Coding | Gaming | Listening to music
```

The manager automatically cycles through them.

---

## Lyrics Status

Display rotating text as a custom status.

Example:

```text
.lyrics First line | Second line | Third line
```

Each line is displayed for a short period before moving to the next one.

---

## Online Status Control

Change the account presence status:

```text
.online online
.online idle
.online dnd
.online invisible
```

Supported modes:

- Online
- Idle
- Do Not Disturb
- Invisible

---

## Voice Channel Tools

Join a voice channel using its Guild ID and Channel ID:

```text
.vc GUILD_ID CHANNEL_ID
```

Leave voice:

```text
.leavevc
```

The manager connects muted and deafened.

---

## AFK System

Enable an automatic AFK response:

```text
.afk I'm currently away.
```

When someone mentions or replies to the account, the configured AFK message can be sent automatically.

Disable AFK:

```text
.noafk
```

The AFK system also keeps track of how long the account has been away.

---

## Text Font Converter

Convert text into several Unicode font styles.

```text
.font Hello World
```

Available styles:

- Bold
- Italic
- Monospace
- Small Caps

Useful for creating styled profile/status text without external websites.

---

## Profile Information

View basic account information and manager state:

```text
.profile
```

The profile panel displays information such as:

- Account name
- Account ID
- AFK status
- Number of saved dynamic RPCs

---

## Control Panel

View the complete command panel:

```text
.panel
```

The panel provides a quick overview of the available RPC, status, voice and utility commands.

---

## RPC Image Guide

Custom RPC images work best when they are uploaded as assets to a Discord application.

Recommended flow:

1. Create/open a Discord application.
2. Open its Rich Presence/Art Assets section.
3. Upload your desired image.
4. Give the asset a key.
5. Configure the matching Application ID in S4lf Manager.
6. Use the asset key with `.setlarge` or `.setsmall`.
7. Apply the RPC.

Example:

```text
.setappid YOUR_APPLICATION_ID
.setlarge my_logo
.setlargetext My Logo
.apply
```

Random external image URLs may not render correctly as Rich Presence assets.

---

## Command List

| Command | Description |
| --- | --- |
| `.panel` | Show the main control panel |
| `.rpc` | Open the RPC builder |
| `.setname <name>` | Set RPC name |
| `.settype <type>` | Set activity type |
| `.setdetails <text>` | Set RPC details |
| `.setstate <text>` | Set RPC state |
| `.setappid <id>` | Set application ID |
| `.setlarge <asset>` | Set large image |
| `.setlargetext <text>` | Set large image text |
| `.setsmall <asset>` | Set small image |
| `.setsmalltext <text>` | Set small image text |
| `.addbutton Label \| URL` | Add an RPC button |
| `.clearbuttons` | Remove RPC buttons |
| `.apply` | Apply current RPC |
| `.clearrpc` | Reset RPC builder |
| `.stoprpc` | Clear active RPC |
| `.presets` | List available presets |
| `.preset <name>` | Apply a preset |
| `.savedynamic` | Save current RPC |
| `.dynamic start` | Start RPC rotation |
| `.dynamic stop` | Stop RPC rotation |
| `.dynamic clear` | Delete saved RPCs |
| `.cs <text>` | Set custom status |
| `.csrotate a \| b \| c` | Rotate custom statuses |
| `.lyrics a \| b \| c` | Rotate lyric-style statuses |
| `.online <status>` | Change online status |
| `.vc <guild> <channel>` | Join a voice channel |
| `.leavevc` | Leave voice |
| `.afk <message>` | Enable AFK mode |
| `.noafk` | Disable AFK mode |
| `.font <text>` | Generate Unicode font variants |
| `.profile` | Show account/profile information |
| `.stopall` | Stop active systems |
| `.guide` | Show RPC image instructions |

---

## Quick Setup

### 1. Clone the Repository

```bash
git clone https://github.com/r3novadcl/S4lf-Manager.git
cd S4lf-manager
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

The project currently uses:

```text
discord.py-self
aiohttp
protobuf
```

### 3. Configure Your Credentials

Configure your Discord account session securely.
Add Your Account To4en in "main.py" or create a .env file.

```python
TOKEN = os.getenv("DISCORD_TOKEN")
```

Then configure the environment variable outside the repository.

### 4. Start the Manager

```bash
python main.py
```

After connecting, use:

```text
.panel
```

to open the command panel.

---

## Data Storage

S4lf Manager stores its configuration in:

```text
data.json
```

Saved information can include:

- Current RPC configuration
- Dynamic RPC presets
- AFK configuration

Keep local configuration and credentials out of public repositories.

---

## Discord Compatibility

This project relies on behavior provided by `discord.py-self` and Discord's user Gateway/presence infrastructure.

Discord can change its Gateway behavior, presence system or account policies at any time. Some features may therefore stop working without changes to the project.

This project does not guarantee that a particular RPC, image, button, status or presence will appear exactly as expected.

---

## Project Structure

```text
S4lf-manager/
├── main.py
├── requirements.txt
├── data.json
└── README.md
```

`main.py` contains the manager and command system.

`requirements.txt` contains the Python dependencies.

`data.json` stores the manager's local configuration after the first run.

---

## Credits

**Developer:** r3novadcl

**Development Team:** FX DEVELOPMENT

The project was created as an experimental Discord presence/RPC management utility.

---

## Disclaimer

This project is provided for educational, experimental and research purposes.

It is not affiliated with, endorsed by, or officially supported by Discord.

Self-bots and automated user accounts may violate Discord's policies and can result in account action.

You are responsible for complying with Discord's Terms of Service, Community Guidelines and other applicable policies when using this software.

**Use at your own risk.**

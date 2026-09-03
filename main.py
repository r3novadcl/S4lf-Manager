import discord
from discord.ext import commands
import asyncio
import json
import os
import time
import re

TOKEN = "YOUR_ACCOUNT_TOKEN_HERE"
PREFIX = "."
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"rpc": {}, "dynamic": [], "afk": None}

def save_data(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=4)

data = load_data()
bot = commands.Bot(command_prefix=PREFIX, self_bot=True)

custom_status_task = None
lyric_status_task = None
dynamic_rpc_task = None

RPC_PRESETS = {
    "vscode": {
        "name": "Visual Studio Code",
        "type": 0,
        "application_id": "383226320970055681",
        "details": "Editing main.py",
        "state": "Workspace: Selfbot",
        "large_image": "331398698032898050",
        "large_text": "Visual Studio Code",
        "small_image": "python",
        "small_text": "Python",
        "buttons": [
            {"label": "Open VS Code", "url": "https://code.visualstudio.com/"}
        ]
    },
    "github": {
        "name": "GitHub",
        "type": 0,
        "application_id": "383226320970055681",
        "details": "Contributing to open source",
        "state": "Pushing commits",
        "large_image": "331398698032898050",
        "large_text": "GitHub",
        "buttons": [
            {"label": "GitHub", "url": "https://github.com/r3novadcl"}
        ]
    },

    "valorant": {
        "name": "VALORANT",
        "type": 0,
        "application_id": "700136079562375258",
        "details": "Competitive",
        "state": "Ascent | 7-5",
        "large_text": "VALORANT"
    },
    "minecraft": {
        "name": "Minecraft",
        "type": 0,
        "application_id": "356875570916753438",
        "details": "Survival Mode",
        "state": "Playing on Hypixel",
        "large_text": "Minecraft"
    },
    "genshin": {
        "name": "Genshin Impact",
        "type": 0,
        "application_id": "762434991303950386",
        "details": "Exploring Teyvat",
        "state": "Adventure Rank 60",
        "large_text": "Genshin Impact"
    },
    "lol": {
        "name": "League of Legends",
        "type": 0,
        "application_id": "401518684763586560",
        "details": "Ranked Solo/Duo",
        "state": "In Game",
        "large_text": "League of Legends"
    },
    "fortnite": {
        "name": "Fortnite",
        "type": 0,
        "application_id": "432980957394370572",
        "details": "Battle Royale",
        "state": "In Lobby",
        "large_text": "Fortnite"
    },
    "gta": {
        "name": "Grand Theft Auto V",
        "type": 0,
        "application_id": "356876176465199104",
        "details": "GTA Online",
        "state": "Los Santos",
        "large_text": "GTA V"
    },
    "cs2": {
        "name": "Counter-Strike 2",
        "type": 0,
        "application_id": "356876590342340608",
        "details": "Competitive",
        "state": "Dust II",
        "large_text": "CS2"
    },
    "roblox": {
        "name": "Roblox",
        "type": 0,
        "application_id": "363397450228531200",
        "details": "Playing",
        "state": "In experience",
        "large_text": "Roblox"
    },
    "apex": {
        "name": "Apex Legends",
        "type": 0,
        "application_id": "740614701054345276",
        "details": "Battle Royale",
        "state": "In Match",
        "large_text": "Apex Legends"
    },
    "pubg": {
        "name": "PUBG: BATTLEGROUNDS",
        "type": 0,
        "application_id": "530196305138417685",
        "details": "Squad",
        "state": "Erangel",
        "large_text": "PUBG"
    },

    "music": {
        "name": "Spotify",
        "type": 2,
        "application_id": "383226320970055681",
        "details": "Blinding Lights",
        "state": "The Weeknd",
        "large_image": "331398698032898050",
        "large_text": "After Hours",
        "buttons": [
            {"label": "Open Spotify", "url": "https://open.spotify.com/"}
        ]
    },
    "youtube": {
        "name": "YouTube",
        "type": 3,
        "application_id": "383226320970055681",
        "details": "Watching a video",
        "state": "1080p HD",
        "large_image": "331398698032898050",
        "large_text": "YouTube",
        "buttons": [
            {"label": "YouTube", "url": "https://youtube.com/"}
        ]
    },
    "netflix": {
        "name": "Netflix",
        "type": 3,
        "application_id": "383226320970055681",
        "details": "Watching a show",
        "state": "Chill mode",
        "large_image": "331398698032898050",
        "large_text": "Netflix",
        "buttons": [
            {"label": "Netflix", "url": "https://netflix.com/"}
        ]
    },
    "anime": {
        "name": "Crunchyroll",
        "type": 3,
        "application_id": "383226320970055681",
        "details": "Watching Anime",
        "state": "One Piece",
        "large_image": "331398698032898050",
        "large_text": "Crunchyroll",
        "buttons": [
            {"label": "Crunchyroll", "url": "https://crunchyroll.com/"}
        ]
    }
}

FONT_MAP = {
    "bold": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"),
    "italic": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻"),
    "mono": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"),
    "smallcaps": str.maketrans("abcdefghijklmnopqrstuvwxyz", "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"),
}


def normalize_asset(value):
    
    if not value:
        return None
    v = str(value).strip()
    if v.startswith("mp:") or v.startswith("spotify:"):
        return v
    if v.startswith("http://") or v.startswith("https://"):
        clean = re.sub(r"^https?://", "", v)
        return f"mp:external/{clean}"
    return v


def build_activity_dict(d):
    activity = {
        "name": d.get("name", "Selfbot"),
        "type": int(d.get("type", 0)),
        "timestamps": {"start": int(time.time() * 1000)}
    }

    if d.get("details"):
        activity["details"] = str(d["details"])
    if d.get("state"):
        activity["state"] = str(d["state"])
    if d.get("url") and int(d.get("type", 0)) == 1:
        activity["url"] = d["url"]

    if d.get("application_id"):
        activity["application_id"] = str(d["application_id"])

    assets = {}
    large = normalize_asset(d.get("large_image") or d.get("large_image_url"))
    small = normalize_asset(d.get("small_image") or d.get("small_image_url"))
    if large:
        assets["large_image"] = large
    if d.get("large_text"):
        assets["large_text"] = str(d["large_text"])
    if small:
        assets["small_image"] = small
    if d.get("small_text"):
        assets["small_text"] = str(d["small_text"])
    if assets:
        activity["assets"] = assets

    buttons = d.get("buttons") or []
    if buttons:
        activity["buttons"] = [b["label"] for b in buttons[:2]]
        activity["metadata"] = {"button_urls": [b["url"] for b in buttons[:2]]}

    return activity


async def set_presence_raw(activities=None, status="online"):
    payload = {
        "op": 3,
        "d": {
            "since": 0,
            "activities": activities or [],
            "status": status,
            "afk": False
        }
    }
    await bot.ws.send_as_json(payload)


async def set_custom_status_raw(text, status="online"):
    activity = {
        "type": 4,
        "state": text,
        "name": "Custom Status",
        "id": "custom"
    }
    await set_presence_raw([activity], status)


def format_state():
    d = data.get("rpc", {})
    types = ["Playing", "Streaming", "Listening", "Watching", "Custom", "Competing"]
    t = int(d.get("type", 0) or 0)
    tname = types[t] if 0 <= t < len(types) else str(t)
    lines = [
        "```",
        "+--- RPC BUILDER ---+",
        f"| Name   : {d.get('name', '-')}",
        f"| Type   : {tname}",
        f"| AppID  : {d.get('application_id', '-')}",
        f"| Details: {d.get('details', '-')}",
        f"| State  : {d.get('state', '-')}",
        f"| Large  : {(str(d.get('large_image') or d.get('large_image_url') or '-'))[:40]}",
        f"| Small  : {(str(d.get('small_image') or d.get('small_image_url') or '-'))[:40]}",
        f"| Buttons: {len(d.get('buttons', []))}/2",
        "+-------------------+",
        "```"
    ]
    return "\n".join(lines)


async def send_panel(ctx, content):
    try:
        await ctx.message.edit(content=content)
    except Exception:
        await ctx.send(content)


@bot.event
async def on_ready():
    print("=====================================")
    print(f" Selfbot ready: {bot.user}")
    print(f" Prefix: {PREFIX}")
    print("=====================================")


@bot.command(name="panel")
async def panel(ctx):
    content = (
        "```\n"
        "+======================================+\n"
        "|         SELFBOT CONTROL PANEL        |\n"
        "+======================================+\n"
        "| RPC                                  |\n"
        "|  .rpc                 builder menu   |\n"
        "|  .presets             list presets   |\n"
        "|  .preset <name>       apply preset   |\n"
        "|  .apply               push RPC       |\n"
        "|  .stoprpc             clear RPC      |\n"
        "|  .dynamic             rotate RPCs    |\n"
        "|                                      |\n"
        "| STATUS                               |\n"
        "|  .cs <text>                          |\n"
        "|  .csrotate a | b | c                 |\n"
        "|  .lyrics a | b | c                   |\n"
        "|  .online online|idle|dnd|invisible   |\n"
        "|                                      |\n"
        "| VOICE / MISC                         |\n"
        "|  .vc <guild_id> <channel_id>         |\n"
        "|  .leavevc                            |\n"
        "|  .afk <msg>  /  .noafk               |\n"
        "|  .font <text>                        |\n"
        "|  .profile  /  .stopall  /  .guide    |\n"
        "+======================================+\n"
        "```"
    )
    await send_panel(ctx, content)


@bot.command(name="rpc")
async def rpc_menu(ctx):
    content = (
        "```\n"
        "+=========== RPC BUILDER ===========+\n"
        "| .setname <name>                   |\n"
        "| .settype 0/1/2/3/5                |\n"
        "| .setdetails <text>                |\n"
        "| .setstate <text>                  |\n"
        "| .setappid <application_id>        |\n"
        "| .setlarge <asset_key_or_id>       |\n"
        "| .setlargetext <text>              |\n"
        "| .setsmall <asset_key_or_id>       |\n"
        "| .setsmalltext <text>              |\n"
        "| .addbutton Label | https://url    |\n"
        "| .clearbuttons                     |\n"
        "| .apply / .clearrpc / .savedynamic |\n"
        "+===================================+\n"
        "| IMAGE RULE:                       |\n"
        "| Use asset KEY from Dev Portal     |\n"
        "| with matching .setappid           |\n"
        "| Random image links = black box    |\n"
        "+===================================+\n"
        "```\n" + format_state()
    )
    await send_panel(ctx, content)


@bot.command(name="setname")
async def setname(ctx, *, val):
    data.setdefault("rpc", {})["name"] = val
    save_data(data)
    await send_panel(ctx, f"```\n[OK] name = {val}\n```\n" + format_state())


@bot.command(name="settype")
async def settype(ctx, val: int):
    data.setdefault("rpc", {})["type"] = val
    save_data(data)
    await send_panel(ctx, f"```\n[OK] type = {val}\n```\n" + format_state())


@bot.command(name="setdetails")
async def setdetails(ctx, *, val):
    data.setdefault("rpc", {})["details"] = val
    save_data(data)
    await send_panel(ctx, "```\n[OK] details set\n```\n" + format_state())


@bot.command(name="setstate")
async def setstate(ctx, *, val):
    data.setdefault("rpc", {})["state"] = val
    save_data(data)
    await send_panel(ctx, "```\n[OK] state set\n```\n" + format_state())


@bot.command(name="setappid")
async def setappid(ctx, *, val):
    data.setdefault("rpc", {})["application_id"] = val.strip()
    save_data(data)
    await send_panel(ctx, f"```\n[OK] application_id = {val.strip()}\n```\n" + format_state())


@bot.command(name="setlarge")
async def setlarge(ctx, *, val):
    d = data.setdefault("rpc", {})
    d["large_image"] = val.strip()
    d.pop("large_image_url", None)
    save_data(data)
    await send_panel(ctx, "```\n[OK] large_image set (asset key/id preferred)\n```\n" + format_state())


@bot.command(name="setlargetext")
async def setlargetext(ctx, *, val):
    data.setdefault("rpc", {})["large_text"] = val
    save_data(data)
    await send_panel(ctx, "```\n[OK] large_text set\n```\n" + format_state())


@bot.command(name="setsmall")
async def setsmall(ctx, *, val):
    d = data.setdefault("rpc", {})
    d["small_image"] = val.strip()
    d.pop("small_image_url", None)
    save_data(data)
    await send_panel(ctx, "```\n[OK] small_image set\n```\n" + format_state())


@bot.command(name="setsmalltext")
async def setsmalltext(ctx, *, val):
    data.setdefault("rpc", {})["small_text"] = val
    save_data(data)
    await send_panel(ctx, "```\n[OK] small_text set\n```\n" + format_state())


@bot.command(name="addbutton")
async def addbutton(ctx, *, val):
    if "|" not in val:
        await send_panel(ctx, "```\n[ERR] .addbutton Label | https://url\n```")
        return
    label, url = [x.strip() for x in val.split("|", 1)]
    d = data.setdefault("rpc", {})
    d.setdefault("buttons", [])
    if len(d["buttons"]) >= 2:
        await send_panel(ctx, "```\n[ERR] max 2 buttons\n```")
        return
    d["buttons"].append({"label": label, "url": url})
    save_data(data)
    await send_panel(ctx, f"```\n[OK] button added: {label}\n```\n" + format_state())


@bot.command(name="clearbuttons")
async def clearbuttons(ctx):
    data.setdefault("rpc", {})["buttons"] = []
    save_data(data)
    await send_panel(ctx, "```\n[OK] buttons cleared\n```")


@bot.command(name="clearrpc")
async def clearrpc(ctx):
    data["rpc"] = {}
    save_data(data)
    await send_panel(ctx, "```\n[OK] builder reset\n```")


@bot.command(name="apply")
async def apply_rpc(ctx):
    d = data.get("rpc", {})
    if not d.get("name"):
        await send_panel(ctx, "```\n[ERR] set name first (.setname)\n```")
        return
    if d.get("large_image") and not d.get("application_id"):
        await send_panel(ctx, "```\n[WARN] Image without application_id usually shows BLACK.\nUse .setappid first, or .preset <name>\n```")
    try:
        await set_presence_raw([build_activity_dict(d)], "online")
        await send_panel(ctx, "```\n[OK] RPC pushed. Check profile in 5-15s\n```\n" + format_state())
    except Exception as e:
        await send_panel(ctx, f"```\n[ERR] {type(e).__name__}: {e}\n```")


@bot.command(name="stoprpc")
async def stoprpc(ctx):
    try:
        await set_presence_raw([], "online")
        await send_panel(ctx, "```\n[OK] RPC stopped\n```")
    except Exception as e:
        await send_panel(ctx, f"```\n[ERR] {e}\n```")


@bot.command(name="presets")
async def presets_cmd(ctx):
    names = sorted(RPC_PRESETS.keys())
    lines = ["```", "+====== READY PRESETS ======+"]
    for n in names:
        p = RPC_PRESETS[n]
        lines.append(f"| .preset {n:<12} | {p['name']}")
    lines.append("+===========================+")
    lines.append("| Games use real app IDs    |")
    lines.append("| Best chance for icons     |")
    lines.append("+===========================+")
    lines.append("```")
    await send_panel(ctx, "\n".join(lines))


@bot.command(name="preset")
async def preset_cmd(ctx, *, name):
    key = None
    for k in RPC_PRESETS:
        if k.lower() == name.lower() or RPC_PRESETS[k]["name"].lower() == name.lower():
            key = k
            break
    if not key:
        await send_panel(ctx, "```\n[ERR] unknown preset. Use .presets\n```")
        return

    p = dict(RPC_PRESETS[key])
    if "buttons" in p:
        p["buttons"] = [dict(x) for x in p["buttons"]]
    data["rpc"] = p
    save_data(data)

    try:
        await set_presence_raw([build_activity_dict(p)], "online")
        await send_panel(ctx, f"```\n[OK] preset applied: {key}\nAppID: {p.get('application_id')}\n```\n" + format_state())
    except Exception as e:
        await send_panel(ctx, f"```\n[ERR] {type(e).__name__}: {e}\n```")


@bot.command(name="savedynamic")
async def savedynamic(ctx):
    d = data.get("rpc", {})
    if not d.get("name"):
        await send_panel(ctx, "```\n[ERR] configure rpc first\n```")
        return
    data.setdefault("dynamic", []).append(dict(d))
    save_data(data)
    await send_panel(ctx, f"```\n[OK] saved. total={len(data['dynamic'])}\n```")


@bot.command(name="dynamic")
async def dynamic_cmd(ctx, action=None):
    global dynamic_rpc_task
    if action == "start":
        if len(data.get("dynamic", [])) < 2:
            await send_panel(ctx, "```\n[ERR] need 2+ .savedynamic first\n```")
            return
        if dynamic_rpc_task:
            dynamic_rpc_task.cancel()

        async def rotate():
            i = 0
            while True:
                d = data["dynamic"][i % len(data["dynamic"])]
                try:
                    await set_presence_raw([build_activity_dict(d)], "online")
                except Exception:
                    pass
                i += 1
                await asyncio.sleep(15)

        dynamic_rpc_task = asyncio.create_task(rotate())
        await send_panel(ctx, f"```\n[OK] rotating {len(data['dynamic'])} rpcs\n```")
    elif action == "stop":
        if dynamic_rpc_task:
            dynamic_rpc_task.cancel()
            dynamic_rpc_task = None
        await send_panel(ctx, "```\n[OK] dynamic stopped\n```")
    elif action == "clear":
        data["dynamic"] = []
        save_data(data)
        await send_panel(ctx, "```\n[OK] cleared\n```")
    else:
        await send_panel(ctx, f"```\n+-- DYNAMIC --+\n| saved: {len(data.get('dynamic', []))}\n| .dynamic start/stop/clear\n+-------------+\n```")


@bot.command(name="cs")
async def customstatus(ctx, *, text=""):
    try:
        if text:
            await set_custom_status_raw(text)
            await send_panel(ctx, f"```\n[OK] status: {text}\n```")
        else:
            await set_presence_raw([], "online")
            await send_panel(ctx, "```\n[OK] cleared\n```")
    except Exception as e:
        await send_panel(ctx, f"```\n[ERR] {e}\n```")


@bot.command(name="csrotate")
async def csrotate(ctx, *, texts=""):
    global custom_status_task
    if not texts:
        await send_panel(ctx, "```\n[Usage] .csrotate a | b | c\n```")
        return
    lst = [x.strip() for x in texts.split("|") if x.strip()]
    if custom_status_task:
        custom_status_task.cancel()

    async def rotate():
        i = 0
        while True:
            try:
                await set_custom_status_raw(lst[i % len(lst)])
            except Exception:
                pass
            i += 1
            await asyncio.sleep(10)

    custom_status_task = asyncio.create_task(rotate())
    await send_panel(ctx, f"```\n[OK] rotating {len(lst)} statuses\n```")


@bot.command(name="lyrics")
async def lyrics_cmd(ctx, *, text=""):
    global lyric_status_task
    if not text:
        await send_panel(ctx, "```\n[Usage] .lyrics line1 | line2 | line3\n```")
        return
    lines = [x.strip() for x in text.split("|") if x.strip()]
    if lyric_status_task:
        lyric_status_task.cancel()

    async def rotate():
        i = 0
        while True:
            try:
                await set_custom_status_raw(f"♪ {lines[i % len(lines)]}")
            except Exception:
                pass
            i += 1
            await asyncio.sleep(8)

    lyric_status_task = asyncio.create_task(rotate())
    await send_panel(ctx, f"```\n[OK] lyrics rotating ({len(lines)})\n```")


@bot.command(name="online")
async def online_cmd(ctx, status="online"):
    if status not in ("online", "idle", "dnd", "invisible"):
        await send_panel(ctx, "```\n[Usage] .online online|idle|dnd|invisible\n```")
        return
    try:
        await set_presence_raw([], status)
        await send_panel(ctx, f"```\n[OK] {status}\n```")
    except Exception as e:
        await send_panel(ctx, f"```\n[ERR] {e}\n```")


@bot.command(name="vc")
async def vc_cmd(ctx, guild_id: int, channel_id: int):
    try:
        guild = bot.get_guild(guild_id)
        if not guild:
            await send_panel(ctx, "```\n[ERR] guild not found\n```")
            return
        channel = guild.get_channel(channel_id)
        if not channel:
            await send_panel(ctx, "```\n[ERR] channel not found\n```")
            return
        await channel.connect(self_mute=True, self_deaf=True)
        await send_panel(ctx, f"```\n[OK] joined {channel.name}\n```")
    except Exception as e:
        await send_panel(ctx, f"```\n[ERR] {e}\n```")


@bot.command(name="leavevc")
async def leavevc(ctx):
    try:
        for vc in bot.voice_clients:
            await vc.disconnect()
        await send_panel(ctx, "```\n[OK] left voice\n```")
    except Exception as e:
        await send_panel(ctx, f"```\n[ERR] {e}\n```")


@bot.command(name="afk")
async def afk_cmd(ctx, *, message):
    data["afk"] = {"message": message, "since": time.time()}
    save_data(data)
    await send_panel(ctx, f"```\n[OK] AFK on: {message}\n```")


@bot.command(name="noafk")
async def noafk(ctx):
    data["afk"] = None
    save_data(data)
    await send_panel(ctx, "```\n[OK] AFK off\n```")


@bot.command(name="font")
async def font_cmd(ctx, *, text):
    lines = ["```"]
    for n, tr in FONT_MAP.items():
        lines.append(f"[{n:10}] {text.translate(tr)}")
    lines.append("```")
    await send_panel(ctx, "\n".join(lines))


@bot.command(name="profile")
async def profile_cmd(ctx):
    u = bot.user
    await send_panel(ctx, (
        "```\n"
        "+== PROFILE ==+\n"
        f"| {u.name}\n"
        f"| ID {u.id}\n"
        f"| AFK {'ON' if data.get('afk') else 'OFF'}\n"
        f"| Dynamic {len(data.get('dynamic', []))}\n"
        "+=============+\n"
        "```"
    ))


@bot.command(name="stopall")
async def stopall(ctx):
    global custom_status_task, lyric_status_task, dynamic_rpc_task
    for t in (custom_status_task, lyric_status_task, dynamic_rpc_task):
        if t:
            t.cancel()
    custom_status_task = lyric_status_task = dynamic_rpc_task = None
    try:
        await set_presence_raw([], "online")
        for vc in bot.voice_clients:
            await vc.disconnect()
    except Exception:
        pass
    data["afk"] = None
    save_data(data)
    await send_panel(ctx, "```\n[OK] all stopped\n```")


@bot.command(name="guide")
async def guide_cmd(ctx):
    await send_panel(ctx, (
        "```\n"
        "+================ RPC IMAGE TRUTH ================+\n"
        "|1) Random imgur/png links mostly show BLACK      |\n"
        "|2) Working way: application_id + asset key/id    |\n"
        "|3) Easiest: .preset valorant / minecraft / etc   |\n"
        "|4) Custom image steps:                           |\n"
        "|   - discord.com/developers/applications         |\n"
        "|   - your app -> Rich Presence -> Art Assets     |\n"
        "|   - upload image, set name e.g. cover           |\n"
        "|   - Save Changes                                |\n"
        "|   - .setappid YOUR_APP_ID                       |\n"
        "|   - .setlarge cover                             |\n"
        "|   - .apply                                      |\n"
        "|5) Buttons need application_id too               |\n"
        "|6) Real Spotify progress UI needs Spotify link   |\n"
        "|   (custom RPC can only look similar)            |\n"
        "+=================================================+\n"
        "```"
    ))


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        await bot.process_commands(message)
        return
    if not data.get("afk"):
        return
    hit = bot.user in message.mentions
    if message.reference and message.reference.resolved:
        try:
            hit = hit or message.reference.resolved.author.id == bot.user.id
        except Exception:
            pass
    if hit:
        try:
            afk = data["afk"]
            mins = int(time.time() - afk["since"]) // 60
            await message.channel.send(f"**AFK:** {afk['message']}\n*Away for {mins} min*")
        except Exception:
            pass


bot.run(TOKEN)

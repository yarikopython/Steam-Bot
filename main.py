import discord
import os
import requests
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

steam_key = os.environ.get("STEAM_KEY")
bot_token = os.environ.get("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)


## API ##


def format_unixtime(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def achieve_percent(appid):
    link = f"http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={appid}&format=json"
    response = requests.get(url=link)
    return response.json()


def get_friend_list(steamid):
    link = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={steam_key}&steamid={steamid}&relationship=friend"
    response = requests.get(url=link)
    return response.json()


def get_player_summaries(steamid):
    link = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_key}&steamids={steamid}"
    response = requests.get(url=link)
    return response.json()


def get_player_achieve(steamid, appid):
    link = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={steam_key}&steamid={steamid}"
    response = requests.get(url=link)
    return response.json()


def get_player_recently_games(steamid, count):
    link = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={steam_key}&steamid={steamid}&count={count}&format=json"
    response = requests.get(url=link)
    return response.json()


def get_owned_games(steamid):
    link = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steam_key}&steamid={steamid}&format=json"
    response = requests.get(url=link)
    return response.json()


def get_user_stats_for_game(steamid):
    link = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steam_key}&steamid={steamid}&format=json"
    response = requests.get(url=link)
    return response.json()


def get_app_details(appid):
    link = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url=link)
    return response.json()


####

## BOT ##


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"
        )
    )
    await bot.tree.sync()


@bot.tree.command(name="friends", description="Information about friends of the user")
@app_commands.describe(steamid="User Steam ID")
async def friends(interaction: discord.Interaction, steamid: str):
    steamid = int(steamid)
    data = get_friend_list(steamid)
    name = get_player_summaries(steamid)["response"]["players"][0]["personaname"]
    text = ""
    for friend in data["friendslist"]["friends"]:
        friendid = friend["steamid"]
        friend_name = get_player_summaries(friendid)["response"]["players"][0][
            "personaname"
        ]
        text += f"**{friendid}** - **[{friend_name}](https://steamcommunity.com/profiles/{friendid})** \n"

    embed = discord.Embed(
        color=discord.Color.dark_theme(),
        title=f"Friend of {name}",
        description=text,
    )

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="summaries", description="Information about the user")
async def summaries(interaction: discord.Interaction, steamid: str):
    steamid = int(steamid)
    statuses = {
        0: "Offline",
        1: "Online",
        2: "Busy",
        3: "Away",
        4: "Snooze",
        5: "Looking to trade",
        6: "Looking to play",
    }

    data = get_player_summaries(steamid)

    player = data["response"]["players"]

    displayname = player[0]["personaname"]

    steam_id = player[0]["steamid"]

    status = player[0]["personastate"]

    avatar = player[0]["avatar"]

    info = f"""
    **Displayname**: {displayname}
    **Steamid**: {steam_id}
    **Status**: {statuses[status]}
    **Profile Picture**: [Click Here]({avatar})
    """
    embed = discord.Embed(
        title="Player Summaries",
        url=f"https://steamcommunity.com/profiles/{steamid}",
        description=info,
        color=discord.Color.dark_theme(),
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(
    name="get_achieve", description="Get users achievements from a specific game"
)
async def achieve(interaction: discord.Interaction, steamid: str, appid: str):
    steamid, appid = int(steamid), int(appid)
    data = get_player_achieve(steamid, appid)

    achieved = {0: "No", 1: "Yes"}

    text = ""

    print(data)

    for achieve in data["playerstats"]["achievements"]:
        print(achieve)
        text += f"Name - {achieve['apiname']} - Achieved - {achieved[achieve['achieved']]}\n"

    embed = discord.Embed(
        color=discord.Color.dark_theme(), title="Achievements", description=text
    )

    with open("message.txt", "w") as file:
        file.write(text)

    await interaction.response.send_message(file=discord.File("message.txt"))


@bot.tree.command(name="owned_games", description="Information about users owned games")
async def owned_games(interaction: discord.Interaction, steamid: str):
    steamid = int(steamid)

    data = get_owned_games(steamid)

    games = data["response"]["games"]

    details = {}

    display_name = get_player_summaries(steamid)["response"]["players"][0][
        "personaname"
    ]

    for game in games:
        appid = game["appid"]

        detail = get_app_details(appid)

        game_data = detail.get(str(appid), {})

        if game_data.get("success") and "data" in game_data:
            details[appid] = detail[str(appid)]["data"]["name"]
        else:
            continue

    description_text = ""
    for key, value in details.items():
        description_text += f"{key} - {value}\n"

    embed = discord.Embed(
        color=discord.Color.dark_theme(),
        title=f"**Owned Games of {display_name}**",
        description=description_text,
        url=f"https://steamcommunity.com/profiles/{steamid}",
    )

    await interaction.response.send_message(embed=embed)


####


bot.run(token=bot_token)

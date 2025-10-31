import discord, os, requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

steam_key = os.environ.get("STEAM_KEY")
bot_token = os.environ.get("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)

def achieve_percent(appid):
    link = f"http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={appid}&format=json"
    response = requests.get(url=link)
    return response.json()


def get_friend_list(key, steamid):
    link =  f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid={steamid}&relationship=friend"
    response = requests.get(url=link)
    return  response.json()


def get_player_summaries(key, steamid):
    link = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steamid}"
    response = requests.get(url=link)
    return response.json()


def get_player_achieve(key, steamid, appid):
    link = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={key}&steamid={steamid}"
    response = requests.get(url=link)
    return response.json()


def get_player_recently_games(key, steamid, count):
    link = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={steamid}&count={count}&format=json"
    response = requests.get(url=link)
    return response.json()


def get_owned_games(key, steamid):
    link = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steam_id}&format=json"
    response = requests.get(url=link)
    return response.json()

def get_user_stats_for_game(key, steamid):
    link = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamid}&format=json"
    response = requests.get(url=link)
    return response.json()


def get_app_details(appid):
    link = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url=link)
    return response.json()


@bot.command()
async def friends(ctx, key, steamid):
    data = get_friend_list(key, steamid)
    for friend in data["friendslist"]["friends"]:
        await ctx.send(friend["steamid"])


@bot.command()
async def summaries(ctx, key, steamid):
    data = get_player_summaries(key, steamid)
    player = data["response"]["players"]
    name = player[0]["personaname"]
    steam_id = player[0]["steamid"]
    info = f"""
    name: {name}
    steamid: {steam_id}"""
    embed = discord.Embed(title="Player Summaries",
                          url="https://realdrewdata.medium.com/",
                          description=info, color=0xFF5733)
    await ctx.send(embed=embed)


@bot.command()
async def achieve(ctx, key, steamid, appid):
    data = get_player_achieve(key, steamid, appid)


@bot.command()
async def owned_games(ctx, key, steamid):
    data = get_owned_games(key, steamid)
    
    games = data["response"]["games"]
    games_count = data["response"]["game_count"]
    details = []
    for x in range(int(games_count)):
        details.append(get_app_details(games[x][])["data"]["name"])

    ctx.send(details)

@bot.command()
async def percent_of_achieve(ctx, appid, achieve_num):
    data = achieve_percent(appid)
    ctx.send(data["achievements"][achieve_num]["percent"])


bot.run(token=bot_token)
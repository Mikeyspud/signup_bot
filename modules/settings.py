'''
Holds global variables that must be accessed throughout the project
To use:
    import settings
Example:
    settings.operation_dict
'''

import pymongo                          # mongodb API
import discord                          # discord API


def init():

    # token
    global token
    token = open("/home/user/Documents/signup_bot/token.txt", "r").readline()

    # application id
    global app_id
    app_id = "793212453286182922"

    # guild id
    global guild_id
    guild_id = "406492955629715456"

    # discord global url
    global discord_url_global
    discord_url_global = f"https://discord.com/api/v8/applications/{app_id}/commands"

    # discord url
    global discord_url
    discord_url = f"https://discord.com/api/v8/applications/{app_id}/guilds/{guild_id}/commands"

    # mongodb variables
    global mongo_client
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

    global squad_collection
    squad_db = mongo_client["squad_template"]
    squad_collection = squad_db["template"]

    global op_collection
    op_db = mongo_client["operation_template"]
    op_collection = op_db["template"]

    global alias_collection
    alias_db = mongo_client["alias"]
    alias_collection = alias_db["alias"]

    # General Global Variables
    # Holds the discord channel id's where operations have been started
    global operation_dict
    operation_dict = {}

    # Nested dict that holds the message id's for each squad and its embedded
    # messages
    global embed_dict
    embed_dict = {}

    # History dict that holds the command history for each channel id
    global history_dict
    history_dict = {}

    # Alias dict stores the alias names for roles
    global alias_dict
    alias_dict = {}

    # Server Name
    global server_name
    server_name = "BJay"

    # Outfit Name
    global outfit_name
    outfit_name = "Get off my base peasants"

    # Outfit Tag
    global outfit_tag
    outfit_tag = "[BJay]"

    # Outfit Icon Url
    global outfit_icon
    outfit_icon = "https://www.outfit-tracker.com/usercontent/outfits/logo/37573720558810750.png"


def help_embed():

    embed = discord.Embed(
        title="BJay Signup Bot",
        description="Help Message",
        color=0x2117db)
    embed.set_author(name=f"{outfit_tag} {outfit_name}", icon_url=outfit_icon)

    return embed


def debug_embed():

    embed = discord.Embed(
        title="BJay Signup Bot",
        description="Debug Message",
        color=0xebc20a)
    embed.set_author(
        name=f"{outfit_tag} {outfit_name}",
        icon_url="https://www.outfit-tracker.com/usercontent/outfits/logo/37573720558810750.png")
    embed.set_footer(
        text="Message \"[BJay] 3rdPartyAimAssist\" if you think this errors shouldnt happen")

    return embed

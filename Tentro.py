# Import Discord Package

import discord, datetime, os, random
from discord import *
from discord.ext import commands
from pathlib import Path
import lib.database as db
from discord_components import *
from discord_components import DiscordComponents, Button, ButtonStyle, component, InteractionEventType
intents = discord.Intents.all()

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

# Bot

owners = [668423998777982997, 391936025598885891, 620690744897699841, 804970459561066537, 216260005827969024, 671791003065384987] # Allows us to run commands with the @commands.is_owner() decorator.
bot = commands.Bot(command_prefix = "t!", owner_ids = owners, intents = intents, case_insensitive = True)
print(f"Tentro is connecting..\n-----")
print("Tentro Database setting up.. please hold.\n-----")
db.setup()
print(f'Tentro has connected successfully.')

# le status

@bot.remove_command("help")
@bot.event
async def on_ready():
    
    DiscordComponents(bot)
    general_channel = bot.get_channel(745925853229350975)
    await general_channel.send("Bot is online!")
    await bot.change_presence(activity=discord.Game(name="t!help for Help!"))

@bot.event
async def on_message(message):

    if message.content =="!t":
        await message.channel.send("This is the default prefix")
    

    await bot.process_commands(message)
         

# C O M M A N D S

for file in os.listdir(cwd+"/cogs"):
    if file.endswith(".py") and not file.startswith("_"):
        bot.load_extension(f"cogs.{file[:-3]}")

with open("token.0", "r", encoding="utf-8") as f:
    TOKEN = f.read()

bot.run(TOKEN)

# Import Discord Package

import discord, datetime
from discord import *
from discord.ext import commands
import os, random
from pathlib import Path
import sqlite3, json, asyncio
import lib.database as db

intents = discord.Intents.all()

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

# Bot

owners = [668423998777982997, 391936025598885891, 620690744897699841, 804970459561066537, 216260005827969024, 671791003065384987] # Allows us to run commands with the @commands.is_owner() decorator.
bot = commands.Bot(command_prefix = "t!", owner_ids = owners, intents = intents)
print(f"Tentro is connecting..\n-----")
print("Tentro Database setting up.. please hold.\n-----")
db.setup()
print(f'Tentro has connected successfully.')


# le status

@bot.event
async def on_ready():
    

    general_channel = bot.get_channel(745925853229350975)
    await general_channel.send("Bot is online!")
    await bot.change_presence(activity=discord.Game(name="t!help for Help!"))

@bot.event
async def on_message(message):

    if message.content =="!t":
        await message.channel.send("This is the default prefix")
    

    await bot.process_commands(message)
         

# C O M M A N D S

@bot.remove_command("help")



@bot.command(name="invite", aliases=["inv"])
async def _Invite(ctx):
    embed = discord.Embed(title="Invite Tentro", description="Click [here](https://discord.com/oauth2/authorize?client_id=861919315506495508&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3D861919315506495508%26scope%3Dbot%26permissions%3D8589934591&scope=bot) to invite Tentro to your server!", colour=0xff0000)
    await ctx.channel.send(embed=embed)




for file in os.listdir(cwd+"/cogs"):
    if file.endswith(".py") and not file.startswith("_"):
        bot.load_extension(f"cogs.{file[:-3]}")

with open("token.0", "r", encoding="utf-8") as f:
    TOKEN = f.read()

bot.run(TOKEN)

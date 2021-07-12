# Import Discord Package

import discord, datetime
from discord import *
from discord.ext import commands
import os, random
from pathlib import Path

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

# Bot

bot = commands.Bot(command_prefix="t!")
print('Officially working!')

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
    elif message.content == "hi":
        await message.channel.send("Hello There")

    await bot.process_commands(message)

# C O M M A N D S

@bot.remove_command("help")

@bot.command(name="8ball")
async def _8ball(ctx, *, question=None):
    responses = ["Definitely.", "It is certain", "Does 2 + 2 equal to 4?", "I don't think so chief.",
                "Perhaps.",
                "Maybe, ehhh don't take my word for it.",
                "Ask again.",
                "How do you not know this.", "I don't know, im just a discord bot.",
                "No clue bro.",
                "Uhhh Not sure about the answer to that one.", "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful.", "My sources say yes."]

    if question == None:
        await ctx.send("Please ask a question.", delete_after=5)
    else:
        embed = discord.Embed(title=f"**Question:**\n", description = f"{question}", color=0xff0000)
        embed.add_field(name = f"**8ball:**\n" ,value = f"{random.choice(responses)}")
        await ctx.send(embed=embed)



@bot.command(name="activate_premium", aliases=["ap"])
async def _ActivatePremium(ctx):
    embed = discord.Embed(title="Premium", description="Click here [https://discord.com/oauth2/authorize?bot_id=861919315506495508&scope=bot&permissions=8589934591](https://tenor.com/view/stick-bug-stick-bugged-bug-dancing-bug-dancing-gif-18059923) to activate premium! You will get redirected to invite the premium version of the bot. Don't forget to give it the perms!", colour=discord.Color(0xff0000))
    await ctx.channel.send(embed=embed)

@bot.command(name="invite", aliases=["inv"])
async def _Invite(ctx):
    embed = discord.Embed(title="Invite Tentro", description="Click [here](https://discord.com/oauth2/authorize?bot_id=861919315506495508&scope=bot&permissions=8589934591) to invite Tentro to your server!", colour=0xff0000)
    await ctx.channel.send(embed=embed)





for file in os.listdir(cwd+"/cogs"):
    if file.endswith(".py") and not file.startswith("_"):
        bot.load_extension(f"cogs.{file[:-3]}")

with open("token.0", "r", encoding="utf-8") as f:
    TOKEN = f.read()

bot.run(TOKEN)

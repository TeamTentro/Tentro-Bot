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
print('ok')

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

bot.remove_command("help")
@bot.command(name="help")
async def _Help(ctx):

    embed = discord.Embed(title="These are all the commands", color=0xFF0000)
    embed.add_field(name="Available commands:", value="!tclear, !tban, !tkick, !tmute, !tunban, !tunmute, !tping, !tserver", inline=False)
    embed.add_field(name="Bot version:", value="v1.0", inline=False)
    embed.add_field(name="Date released:", value="July 6th", inline=False)
    embed.set_footer(text="Still in progress!")
    embed.set_author(name=ctx.author.name)
    embed.timestamp = ctx.message.created_at

    await ctx.send(embed=embed)

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

@bot.command(name="slowmode", aliases=["sm"])
async def _Slowmode(ctx, seconds : int):
  if ctx.author.guild_permissions.manage_messages:
      await ctx.channel.edit(slowmode_delay=seconds)
      embed = discord.Embed(title=f"Slowmode set to {seconds}s.", colour=0xff0000)
      await ctx.send(embed=embed)
  else:
      embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
      await ctx.send(embed=embed, delete_after=5)

@bot.command(name="createchannel", aliases=["createch"])
async def _CreateChannel(ctx, name=None):
    guild = ctx.message.guild
    if ctx.author.guild_permissions.administrator:
        await guild.create_text_channel(name=name)
        embed = discord.Embed(title=f"Channel {name} has been created!")
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
        await ctx.send(embed=embed, delete_after=5)


@bot.command(name="slowmodecheck", aliases=["checksm"])
async def _SlowmodeCheck(ctx):
    seconds = ctx.channel.slowmode_delay
    if ctx.author.guild_permissions.manage_messages:
        embed = discord.Embed(title=f"Slowmode is {seconds}s.", colour=0xff0000)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"You do not have the required permissions to do that!", color=0xff0000)
        await ctx.send(embed=embed, delete_after=4)

@bot.command(name="avatar", aliases=["av"])
async def _Avatar(ctx, *, member: discord.Member=None):
    member = ctx.author if not member else member
    embed = discord.Embed(title = f"{member.name}", color = (0xff0000), timestamp = ctx.message.created_at)
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"Requested by : {ctx.author}",icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command(name="giverole", aliases=["gr"])
async def _GiveRole(ctx, user : discord.Member, *, role : discord.Role):
    if ctx.author.guild_permissions.manage_messages or ctx.author.guild_permissions.administrator:
        await user.add_roles(role)
        embed = discord.Embed(title="Success!", description=f"Given {role.mention} to {user.mention}.", colour=0xff0000)
        embed.set_footer(text="Role Given")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="You do not have the required permissions to do that!", colour=0xff0000)
        await ctx.send(embed=embed, delete_after=5)

@bot.command(name="takerole", aliases=["tr"])
async def _TakeRole(ctx, user : discord.Member, *, role : discord.Role):
    if ctx.author.guild_permissions.manage_messages or ctx.author.guild_permissions.administrator:
        await user.remove_roles(role)
        embed = discord.Embed(title="Success!", description=f"Taken {role.mention} from {user.mention}.", colour=0xff0000)
        embed.set_footer(text="Role Taken")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="You do not have the required permissions to do that!", colour=0xff0000)
        await ctx.send(embed=embed, delete_after=5)

@bot.command(name="clear", aliases=["cl"])
@commands.has_permissions(manage_messages=True)
async def _Clear(ctx, amount: int):
    await ctx.channel.purge(limit = amount+1)
    embed = discord.Embed(title = "Messages purged", description=f"{ctx.author.mention}, purged {amount} message(s)", colour=0xff0000)
    await ctx.send(embed=embed, delete_after=5)

@bot.command(name="resetslowmode", aliases=["rsm"])
async def _ResetSlowmode(ctx):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.edit(slowmode_delay=0)
        embed = discord.Embed(title=f"Slowmode reset.", colour=0xff0000)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
        await ctx.send(embed=embed, delete_after=5)

@bot.command(name="nickname", aliases=["nick"])
async def _Nickname(ctx, member: discord.Member, *,nick):
    await member.edit(nick=nick)
    embed = discord.Embed(title=f"Name changed", description=f"Succesfully changed {member.mention}'s name.", colour=0xff0000)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def _Ping(ctx):
    embed = discord.Embed(title=f"Pong!", description=f"bot latency: {round(bot.latency * 1000)}ms" , colour=0xff0000)
    await ctx.send(embed=embed)

@bot.command(name="server")
async def _Server(ctx):
    embed = discord.Embed(title="Our amazing server", description = "Click [here](https://www.youtube.com/watch?v=dQw4w9WgXcQ) to join our server!", colour=0xff0000)
    await ctx.channel.send(embed=embed)

@bot.command(name="activate_premium", aliases=["ap"])
async def _ActivatePremium(ctx):
    embed = discord.Embed(title="Premium", description="Click here [https://discord.com/oauth2/authorize?bot_id=861919315506495508&scope=bot&permissions=8589934591](https://tenor.com/view/stick-bug-stick-bugged-bug-dancing-bug-dancing-gif-18059923) to activate premium! You will get redirected to invite the premium version of the bot. Don't forget to give it the perms!", colour=discord.Color(0xff0000))
    await ctx.channel.send(embed=embed)

@bot.command(name="invite", aliases=["inv"])
async def _Invite(ctx):
    embed = discord.Embed(title="Invite Tentro", description="Click [here](https://discord.com/oauth2/authorize?bot_id=861919315506495508&scope=bot&permissions=8589934591) to invite Tentro to your server!", colour=0xff0000)
    await ctx.channel.send(embed=embed)

@bot.command(name="servername", aliases=["sn"])
async def _ServerName(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", colour=0xff0000)
    embed.timestamp = ctx.message.created_at
    await ctx.send(embed=embed)

@bot.command(name="lockdown", aliases=["ld"])
async def _Lockdown(ctx):
    channel = ctx.channel
    default_role = ctx.guild.default_role
    if ctx.author.guild_permissions.administrator:
        await channel.set_permissions(target=default_role, speak=False, send_messages=False, read_message_history=True, read_messages=True)
        embed = discord.Embed(title=f"Sucessfully locked down {channel}!")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
        await ctx.send(embed=embed, delete_after=5)

for file in os.listdir(cwd+"/cogs"):
    if file.endswith(".py") and not file.startswith("_"):
        bot.load_extension(f"cogs.{file[:-3]}")

with open("token.0", "r", encoding="utf-8") as f:
    TOKEN = f.read()

bot.run(TOKEN)

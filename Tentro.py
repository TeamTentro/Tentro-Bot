# Import Discord Package

import discord, asyncio, datetime
from discord import *
from discord.ext import commands
import os
from pathlib import Path

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

#Client

client = commands.Bot(command_prefix='t!')
client.remove_command('help')




#C O M M A N D S

@client.event
async def on_ready():

    general_channel = client.get_channel(745925853229350975)

    await general_channel.send('Bot is online!')
    await client.change_presence(activity=discord.Game(name='t!help for Help!'))

@client.event
async def on_message(message):
    if message.content == 't!help':
      
      myEmbed = discord.Embed(title="These are all the commands", color=0xFF0000)
      myEmbed.add_field(name="Available commands:", value="!tclear, !tban, !tkick, !tmute, !tunban, !tunmute, !tping, !tserver", inline=False)
      myEmbed.add_field(name="Bot version:", value="v1.0", inline=False)
      myEmbed.add_field(name="Date released:", value="July 6th", inline=False)
      myEmbed.set_footer(text="Still in progress!")
      myEmbed.set_author(name=message.author.name)
      myEmbed.timestamp = message.created_at
       
      await message.channel.send(embed=myEmbed)
      
    elif message.content =='!t':
     
     await message.channel.send('This is the default prefix')


    if message.content == "hi": 
      
      await message.channel.send("Hello There")   
    await client.process_commands(message)

@client.command(name='ban')
async def ban(ctx, member : discord.Member, *, reason=None):
  guild = ctx.guild
  if ctx.author.guild_permissions.manage_messages:
   await member.ban(reason=reason)
   embed = discord.Embed(title="Banned", description=f"{member.mention} has been banned from the server.", colour=discord.Colour(0xff0000))
   embed.add_field(name="Reason:", value=reason, inline=False)
   embed.set_footer(text='Ban')
   embed.timestamp = datetime.datetime.now()
   await ctx.send(embed=embed)
   embed = discord.Embed(title = (f"You have been banned from: {guild.name}.\n**Reason:** {reason}."), colour=discord.Color(0xff0000))
   await member.send(embed=embed)
  else:
    embed = discord.Embed(title='You do not have the required permissions to do that!', colour=discord.Color(0xff0000))
    await ctx.send(embed=embed, delete_after=5)
     

@client.command(name='gr')
@commands.has_permissions(administrator=True) 
async def role(ctx, user : discord.Member, *, role : discord.Role):
      await user.add_roles(role)
      embed = discord.Embed(title='Success!', description=f"Given {role.mention} to {user.mention}.", colour=discord.Color(0xff0000))
      embed.set_footer(text='Role Given')
      embed.timestamp = datetime.datetime.now()
      await ctx.send(embed=embed)


@client.command(name='kick')
async def kick(ctx, member : discord.Member, *, reason=None):
  guild = ctx.guild
  if ctx.author.guild_permissions.kick_members:
    await member.kick(reason=reason)
    embed = discord.Embed(title="Kicked", description=f"{member.mention} has been kicked from the server.", colour=discord.Colour(0xff0000))
    embed.add_field(name="Reason:", value=reason, inline=False)
    embed.set_footer(text='Kick')
    embed.timestamp = datetime.datetime.now()
    await ctx.send(embed=embed)
    embed = discord.Embed(title = (f"You have been kicked from: {guild.name}.\n**Reason:** {reason}."), colour=discord.Color(0xff0000))
    await member.send(embed=embed)

  else: 
    embed = discord.Embed(title='You do not have the required permissions to do that!', colour=discord.Color(0xff0000))
    await ctx.send(embed=embed, delete_after=5)


@client.command(name="m") 
async def mute(ctx, member: discord.Member, *, reason=None):
  guild = ctx.guild

  mutedRole = discord.utils.get(guild.roles, name="Muted")
  if ctx.message.author.guild_permissions.kick_members or ctx.message.author.guild_permissions.administrator:

    if not mutedRole:
      mutedRole = await guild.create_role(name="Muted", colour=0x34eb40)

    for channel in guild.channels:
       await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)

    embed = discord.Embed(title="Muted", description=f"{member.mention} has been muted indefinitely.", colour=0xff0000)
    embed.add_field(name="Reason:", value=reason, inline=False)
    embed.set_footer(text="Mute")
    embed.timestamp = datetime.datetime.now()
    await ctx.send(embed=embed)

    embed = discord.Embed(title = (f"You have been muted in: {guild.name}.\n**Reason:** {reason}."), colour=0xff0000)
    await member.send(embed=embed)

  else: 
    embed = discord.Embed(title="You do not have the required permissions to do that!", colour=0xff0000)
    await ctx.send(embed=embed, delete_after=5)


@client.command(name='clear')
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount: int):
  await ctx.channel.purge(limit = amount+1)
  embed = discord.Embed(title = 'Messages purged', description=f"{ctx.author.mention}, purged {amount} message(s)", colour=discord.Color(0xff0000))
  await ctx.send(embed=embed, delete_after=5)

@client.command(description="Unmutes a specified user.")
async def unmute(ctx, member: discord.Member):
   guild = ctx.guild
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
   if ctx.author.guild_permissions.manage_messages:
    await member.remove_roles(mutedRole)
    embed = discord.Embed(title="Unmuted", description=f"{member.mention} has been unmuted.",colour=discord.Colour(0xff0000))
    embed.set_footer(text='Unmute')
    embed.timestamp = datetime.datetime.now()
    await ctx.send(embed=embed)
    embed = discord.Embed(title = (f"**You have been unmuted in: {guild.name}.**"), colour=discord.Color(0xff0000))
    await member.send(embed=embed)
   else:
     await ctx.channel.send("You dont have the required permissions to do that!", delete_after=5)

@client.command(name='ping')
async def ping(ctx, arg=None):
  embed = discord.Embed(title=f'Pong!', description = f"Client latency: {round(client.latency * 1000)}ms" , colour=discord.Colour(0xff0000))
  await ctx.send(embed=embed)

@client.command()
async def unban(ctx, *, user: discord.User):
    guild = ctx.guild
    embed = discord.Embed(title='Sucess!', description = f"{user} has been sucessfully unbanned!", colour=discord.Colour(0xff0000))
    
    if ctx.author.guild_permissions.administrator:
      await ctx.send(embed=embed)
      await guild.unban(user=user)
    else:
      embed = discord.Embed(title='You do not have the required permissions to do that!', colour=discord.Color(0xff0000))
      await ctx.send(embed=embed, delete_after=5)

@client.command(name='server')
async def server(ctx, arg=None):
  embed = discord.Embed(title='Our amazing server', description = "Click [here](https://www.youtube.com/watch?v=dQw4w9WgXcQ) to join our server!", colour=discord.Color(0xff0000))
  await ctx.channel.send(embed=embed)

@client.command(name='mutetimer')
async def mute(ctx, member: discord.Member,time):
  guild = ctx.guild
  if ctx.author.guild_permissions.manage_messages:
    muted_role=discord.utils.get(ctx.guild.roles, name="Muted")
    time_convert = {"s":1, "m":60, "h":3600,"d":86400}
    tempmute = float(time[0]) * time_convert[time[-1]] 
    await member.add_roles(muted_role)
    embed = discord.Embed(description= f"**{member.mention} has been muted for {time}**", color=discord.Color(0xff0000))
    await ctx.send(embed=embed)
    embed = discord.Embed(title = (f"You have been muted in: {guild.name}.\n**Time period:** {time}."), colour=discord.Color(0xff0000))
    await member.send(embed=embed)
    await asyncio.sleep(tempmute)
    await member.remove_roles(muted_role)
    embed = discord.Embed(title = (f"You have been unmuted in: {guild.name}."), colour=discord.Color(0xff0000))
    await member.send(embed=embed)
  else:
    await ctx.channel.send("You dont have the required permissions to do that!", delete_after=5)


if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")
    # This is a simple way to load cogs. Under the cogs folder you can make files (EG: moderation.py, util.py. In moderation there might be the ban command, unban command and other
    # moderation commands. In the util there might be ping, help, invite, etc. It's a fancy way of organising your commands!)

with open("token.0", "r", encoding="utf-8") as f:
  bottoken = f.read()

  client.run(bottoken)

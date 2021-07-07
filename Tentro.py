
# Import Discord Package

import discord, asyncio, datetime
from discord import colour
from discord.ext import commands


#Client

client = commands.Bot(command_prefix='!t')
client.remove_command('help')

#C O M M A N D S
 


@client.event
async def on_ready():

    general_channel = client.get_channel(745925853229350975)

    await general_channel.send('Bot is online!')
    




@client.event
async def on_message(message):
    if message.content == '!thelp':
      
      myEmbed = discord.Embed(title="These are all the commands", color=0xFF0000)
      myEmbed.add_field(name="Available commands:", value="!tclear, !tban, !tkick, !tmute", inline=False)
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
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *, reason=None):
  guild = ctx.guild
  await member.ban(reason=reason)
  embed = discord.Embed(title="Banned", description=f"{member.mention} has been banned from the server.", colour=discord.Colour(0xff0000))
  embed.add_field(name="Reason:", value=reason, inline=False)
  embed.set_footer(text='Ban')
  embed.timestamp = datetime.datetime.now()
  await ctx.send(embed=embed)
  embed = discord.Embed(title = (f"You have been banned from: {guild.name}.\n**Reason:** {reason}."), colour=discord.Color(0xff0000))
  await member.send(embed=embed)
  
  

  

@client.command(name='kick')
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, *, reason=None):
  guild = ctx.guild
  await member.kick(reason=reason)
  embed = discord.Embed(title="Kicked", description=f"{member.mention} has been kicked from the server.", colour=discord.Colour(0xff0000))
  embed.add_field(name="Reason:", value=reason, inline=False)
  embed.set_footer(text='Kick')
  embed.timestamp = datetime.datetime.now()
  await ctx.send(embed=embed)
  embed = discord.Embed(title = (f"You have been kicked from: {guild.name}.\n**Reason:** {reason}."), colour=discord.Color(0xff0000))
  await member.send(embed=embed)
    
@client.command(name='mute')   
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted", colour=discord.Colour(0x34eb40))

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="Muted", description=f"{member.mention} has been muted.", colour=discord.Colour(0xff0000))
    embed.add_field(name="Reason:", value=reason, inline=False)
    embed.set_footer(text="Mute")
    embed.timestamp = datetime.datetime.now()
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    embed = discord.Embed(title = (f"You have been muted in: {guild.name}.\n**Reason:** {reason}."), colour=discord.Color(0xff0000))
    await member.send(embed=embed)
    
    
@client.command(name='clear')
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount: int):
  await ctx.channel.purge(limit = amount+1)
  await ctx.send(f"{ctx.author.mention}, purged {amount} message(s)")


@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   guild = ctx.guild
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   embed = discord.Embed(title="Unmuted", description=f"{member.mention} has been unmuted.",colour=discord.Colour(0xff0000))
   embed.set_footer(text='Unmute')
   embed.timestamp = datetime.datetime.now()
   await ctx.send(embed=embed)
   embed = discord.Embed(title = (f"**You have been unmuted in: {guild.name}.**"), colour=discord.Color(0xff0000))
   await member.send(embed=embed)


@client.command(name='ping')
async def ping(ctx, arg=None):
  embed = discord.Embed(title=f'My ping is: {round(client.latency * 1000)}ms.', colour=discord.Colour(0xff0000))
  await ctx.send(embed=embed)


@client.command()
async def unban(ctx, *, user: discord.User,):
    guild = ctx.guild
    embed = discord.Embed(title='Sucess!', description = f"{user} has been sucessfully unbanned!", colour=discord.Colour(0xff0000))
    
    if ctx.author.guild_permissions.administrator:
      await ctx.send(embed=embed)
      await guild.unban(user=user)
    else:
      await ctx.send("You dont have the required permissions to do that!")




  


with open("token.0", "r", encoding="utf-8") as f:
  bottoken = f.read()

  client.run(bottoken)

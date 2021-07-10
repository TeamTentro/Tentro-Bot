from discord.ext import commands
from discord import *
import discord, asyncio, datetime


class AdministrationCommands(commands.Cog):
    def __innit__(self, client):
        self.client = client

def setup(client):
    client.add_cog(AdministrationCommands(client))

@commands.command(name='timedmute', aliases=['tm'])
async def mute(self, ctx, member: discord.Member,time, *,reason=None):
  guild = ctx.guild
  if ctx.author.guild_permissions.manage_messages:
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if not mutedRole:
      mutedRole = await guild.cireate_role(name="Muted", colour=0x34eb40)

      for channel in guild.channels:
         await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    else:
      await member.add_roles(mutedRole, reason=reason)
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



@commands.command(aliases=['ub'])
async def unban(self, ctx, *, user: discord.User):
    guild = ctx.guild
    embed = discord.Embed(title='Sucess!', description = f"{user} has been sucessfully unbanned!", colour=discord.Colour(0xff0000))
    
    if ctx.author.guild_permissions.administrator:
      await ctx.send(embed=embed)
      await guild.unban(user=user)
    else:
      embed = discord.Embed(title='You do not have the required permissions to do that!', colour=discord.Color(0xff0000))
      await ctx.send(embed=embed, delete_after=5)


@commands.command(description="Unmutes a specified user.")
async def unmute(self, ctx, member: discord.Member):
   guild = ctx.guild
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
   if ctx.author.guild_permissions.manage_messages:
    await member.remove_roles(mutedRole)
    embed = discord.Embed(title="Unmuted", description=f"{member.mention} has been unmuted.",colour=discord.Colour(0xff0000))
    embed.set_footer(text='Unmute')
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)
    embed = discord.Embed(title = (f"**You have been unmuted in: {guild.name}.**"), colour=discord.Color(0xff0000))
    await member.send(embed=embed)
   else:
     await ctx.channel.send("You dont have the required permissions to do that!", delete_after=5)

@commands.command(name="mute", aliases=['m']) 
async def mute(self, ctx, member: discord.Member, *, reason=None):
  guild = ctx.guild

  mutedRole = discord.utils.get(guild.roles, name="Muted")
  if ctx.message.author.guild_permissions.kick_members or ctx.message.author.guild_permissions.administrator:

    if not mutedRole:
      mutedRole = await guild.cireate_role(name="Muted", colour=0x34eb40)

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


@commands.command(name='clear', aliases=['cl'])
@commands.has_permissions(manage_messages = True)
async def purge(self, ctx, amount: int):
  await ctx.channel.purge(limit = amount+1)
  embed = discord.Embed(title = 'Messages purged', description=f"{ctx.author.mention}, purged {amount} message(s)", colour=discord.Color(0xff0000))
  await ctx.send(embed=embed, delete_after=5)

@commands.command(name='kick', aliases=['k'])
async def kick(self, ctx, member : discord.Member, *, reason=None):
  guild = ctx.guild
  if ctx.author.guild_permissions.kick_members:
    await member.kick(reason=reason)
    embed = discord.Embed(title="Kicked", description=f"{member.mention} has been kicked from the server.", colour=discord.Colour(0xff0000))
    embed.add_field(name="Reason:", value=reason, inline=False)
    embed.set_footer(text='Kick')
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)
    embed = discord.Embed(title = (f"You have been kicked from: {guild.name}.\n**Reason:** {reason}."), colour=discord.Color(0xff0000))
    await member.send(embed=embed)

  else: 
    embed = discord.Embed(title='You do not have the required permissions to do that!', colour=discord.Color(0xff0000))
    await ctx.send(embed=embed, delete_after=5)

@commands.command(name='ban', aliases=['b'])
async def ban(self, ctx, member : discord.Member, *, reason=None):
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

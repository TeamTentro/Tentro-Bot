from discord.ext import commands
from discord import Embed, Member, User, member, utils
import asyncio
import discord
from discord.ext.commands import bot
import time
import datetime

red = 0xff0000
green = 0x34eb40
start_time = time.time()

class info(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot

    


    
    
    @commands.command(name="servername", aliases=["sn"])
    async def ServerName(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}", colour=0xff0000)
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)

    @commands.command(name="avatar", aliases=["av"])
    async def Avatar(self, ctx, *, member: discord.Member=None):
        member = ctx.author if not member else member
        embed = discord.Embed(title = f"{member.name}", color = (0xff0000), timestamp = ctx.message.created_at)
        embed.set_image(url=member.avatar_url)
        embed.set_footer(text=f"Requested by : {ctx.author}",icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def _Ping(self, ctx):
        embed = discord.Embed(title=f"Pong!", description=f"Client latency: {round(self.bot.latency * 1000)}ms" , colour=0xff0000)
        await ctx.send(embed=embed)

    @commands.command(name="server")
    async def _Server(self, ctx):
        embed = discord.Embed(title="Our amazing server", description = "Click [here](https://discord.gg/86g5WPjF) to join our server!", colour=0xff0000)
        await ctx.channel.send(embed=embed)
    

    
    @commands.command(name="uptime", aliases=["ut"])
    async def _Uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(title="Uptime", description=f"Tentro has been running for {text}" ,colour=red)
       
       
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            uptime = Embed(title="Uptime", description=f"Tentro has been running for {text}", colour=red)
            await ctx.send(embed=uptime)


    @commands.command(name="help")
    async def _Help(self, ctx, dm = None):
        author = ctx.author
        if dm == None or dm != "-dm":
          embed = discord.Embed(title="These are all the commands", color=0xFF0000)
          embed.add_field(name="Moderation", value="`t!clear, t!ban, t!kick, t!mutet, !timedmute, t!unmute, t!ban, t!unban, t!slowmode, t!slowmodecheck, t!slowmodereset, t!createchannel, t!deletechannel, t!giverole, t!takerole, t!nickname, t!lockdown`", inline=False)
          embed.add_field(name="Information", value="`avatar, servername`", inline=False)
          embed.add_field(name="Misc", value="`8ball`", inline=False)
          embed.add_field(name="System", value="`help, ping, invite, server`", inline=False)
          embed.add_field(name="Bot version:", value="v1.0", inline=False)
          embed.add_field(name="Date released:", value="July 6th, 2021", inline=False)
          embed.set_footer(text="Still in progress!")
          embed.set_author(name=ctx.author.name)
          embed.timestamp = ctx.message.created_at

          await ctx.send(embed=embed)
        elif dm == "-dm":
          embed1 = discord.Embed(title="These are all the commands", color=0xFF0000)
          embed1.add_field(name="Moderation", value="`t!clear, t!ban, t!kick, t!mute, !timedmute, t!unmute, t!ban, t!unban, t!slowmode, t!slowmodecheck, t!slowmodereset, t!createchannel, t!deletechannel, t!giverole, t!takerole, t!nickname, t!lockdown`", inline=False)
          embed1.add_field(name="Information", value="`avatar, servername`", inline=False)
          embed1.add_field(name="Misc", value="`8ball`", inline=False)
          embed1.add_field(name="System", value="`help, ping, invite, server`", inline=False)
          embed1.add_field(name="Bot version:", value="v1.0", inline=False)
          embed1.add_field(name="Date released:", value="July 6th, 2021", inline=False)
          embed1.set_footer(text="Still in progress!")
          embed1.set_author(name=ctx.author.name)
          embed1.timestamp = ctx.message.created_at
          await author.send(embed=embed1)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        members = len(list(guild.members))
        #value: '\u200B'

        channelservers = self.bot.get_channel(871434839323213844)
        embed = Embed(title="Tentro has been added to a new server!", color=red)
        embed.set_thumbnail(url=f"{guild.icon_url}")
        embed.add_field(name=f"Server Name: ", value=f"{guild.name}", inline=False)
        embed.add_field(name=f"Server ID: ", value=f"{guild.id}", inline=False)
        embed.add_field(name=f"Members: ", value=f"{members}", inline=False)
        await channelservers.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        members = len(list(guild.members))
        #value: '\u200B'

        channelservers = self.bot.get_channel(871434839323213844)
        embed = Embed(title="Tentro has been removed from a server!", color=red)
        embed.set_thumbnail(url=f"{guild.icon_url}")
        embed.add_field(name=f"Server Name: ", value=f"{guild.name}", inline=False)
        embed.add_field(name=f"Server ID: ", value=f"{guild.id}", inline=False)
        embed.add_field(name=f"Members: ", value=f"{members}", inline=False)
        await channelservers.send(embed=embed)

  

 


def setup(bot):
    bot.add_cog(info(bot))

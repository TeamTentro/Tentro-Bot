from discord.ext import commands
from discord import Embed, Member, User, utils
import asyncio
import discord
from discord.ext.commands import bot


class Info(commands.Cog):

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
        embed = discord.Embed(title="Our amazing server", description = "Click [here](https://www.youtube.com/watch?v=dQw4w9WgXcQ) to join our server!", colour=0xff0000)
        await ctx.channel.send(embed=embed)


    @commands.command(name="help")
    async def _Help(self, ctx):

        embed = discord.Embed(title="These are all the commands", color=0xFF0000)
        embed.add_field(name="Available commands:", value="t!clear, t!ban, t!kick, t!mute, t!unban, t!unmute, t!ping, t!server, t!servername, t!timedmute, t!avatar, t!8ball, t!slowmode, t!slowmodecheck, t!slowmodereset, t!createchannel, t!deletechannel, t!giverole, t!takerole, t!nickname, t!invite, t!lockdown", inline=False)
        embed.add_field(name="Bot version:", value="v1.0", inline=False)
        embed.add_field(name="Date released:", value="July 6th", inline=False)
        embed.set_footer(text="Still in progress!")
        embed.set_author(name=ctx.author.name)
        embed.timestamp = ctx.message.created_at

        await ctx.send(embed=embed)

  

 


def setup(bot):
    bot.add_cog(Info(bot))

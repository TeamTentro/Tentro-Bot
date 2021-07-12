from discord.ext import commands
from discord import Embed, Member, User, client, utils
import asyncio
import discord

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

  

 


def setup(bot):
    bot.add_cog(Info(bot))
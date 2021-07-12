from discord.ext import commands
from discord import Embed, Member, User, utils
import asyncio, discord

class Channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="createchannel", aliases=["createch"])
    async def _CreateChannel(self, ctx, name=None):
        guild = ctx.message.guild
        if ctx.author.guild_permissions.administrator:
            await guild.create_text_channel(name=name)
            embed = discord.Embed(title=f"Channel {name} has been created!")
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
            await ctx.send(embed=embed, delete_after=5)

    
    @commands.command(name="lockdown", aliases=["ld"])       ## Needs fixing!
    async def _Lockdown(self, ctx):
        channel = ctx.channel
        default_role = ctx.guild.default_role
        if ctx.author.guild_permissions.administrator:
            await channel.set_permissions(target=default_role, speak=False, send_messages=False, read_message_history=True, read_messages=True)
            embed = discord.Embed(title=f"Sucessfully locked down {channel}!")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
            await ctx.send(embed=embed, delete_after=5)


    @commands.command(name="clear", aliases=["cl"])
    @commands.has_permissions(manage_messages=True)
    async def _Clear(self, ctx, amount: int):
        await ctx.channel.purge(limit = amount+1)
        embed = discord.Embed(title = "Messages purged", description=f"{ctx.author.mention}, purged {amount} message(s)", colour=0xff0000)
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name="resetslowmode", aliases=["rsm"])
    async def _ResetSlowmode(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            await ctx.channel.edit(slowmode_delay=0)
            embed = discord.Embed(title=f"Slowmode reset.", colour=0xff0000)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
            await ctx.send(embed=embed, delete_after=5)


    @commands.command(name="slowmode", aliases=["sm"])
    async def _Slowmode(self, ctx, seconds : int):
        if ctx.author.guild_permissions.manage_messages:
            await ctx.channel.edit(slowmode_delay=seconds)
            embed = discord.Embed(title=f"Slowmode set to {seconds}s.", colour=0xff0000)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
            await ctx.send(embed=embed, delete_after=5)

    @commands.command(name="slowmodecheck", aliases=["checksm"])
    async def _SlowmodeCheck(self, ctx):
        seconds = ctx.channel.slowmode_delay
        if ctx.author.guild_permissions.manage_messages:
            embed = discord.Embed(title=f"Slowmode is {seconds}s.", colour=0xff0000)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You do not have the required permissions to do that!", color=0xff0000)
            await ctx.send(embed=embed, delete_after=4)














def setup(bot):
    bot.add_cog(Channel(bot)) 
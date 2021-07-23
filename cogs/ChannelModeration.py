from discord.ext import commands
from discord import Embed, Member, User, channel, utils
import asyncio, discord
red = 0xff0000
green = 0x34eb40

class Channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(name="show", aliases=["s"])
    async def _show(self, ctx, member: Member):
        if ctx.author.guild_permissions.manage_messages:
           channel = ctx.channel
           guild = ctx.message.guild
           await channel.set_permissions(target=member, view_channel = True)
           embed = Embed(title='Success!', description=f"Revealed {channel.mention} to {member.mention}. ", colour=red)
           await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
            await ctx.send(embed=embed, delete_after=5)
    
    
    @commands.command(name="hide", aliases=["h"])
    async def _hide(self, ctx, member: Member):
        if ctx.author.guild_permissions.manage_messages:
           channel = ctx.channel
           guild = ctx.message.guild
           await channel.set_permissions(target=member, view_channel = False)
           embed = Embed(title='Success!', description=f"Hid {channel.mention} from {member.mention}. ", colour=red)
           await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
            await ctx.send(embed=embed, delete_after=5)

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
    async def _Slowmode(self, ctx, seconds : int = None):
        smtime = ctx.channel.slowmode_delay
        if ctx.author.guild_permissions.manage_messages:
            if seconds == None:
               embed = discord.Embed(title=f"The current slowmode is {smtime}s.", colour=0xff0000)
               await ctx.send(embed=embed)
            else:
               await ctx.channel.edit(slowmode_delay=seconds)
               embed = discord.Embed(title=f"Slowmode set to {seconds}s.", colour=0xff0000)
               await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
            await ctx.send(embed=embed, delete_after=5)
            if int == 0:
               embed = discord.Embed(title=f"Slowmode succesfully reset.", colour=0xff0000)
               await ctx.send(embed=embed)
   


def setup(bot):
    bot.add_cog(Channel(bot)) 
from discord.ext import commands
from discord import Embed, Member, User, client, utils
import asyncio
import discord
from discord.ext.commands import bot
red = 0xff0000
green = 0x34eb40

class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


  

    @commands.command(name="nickname", aliases=["nick"])
    async def _Nickname(self, ctx, member: discord.Member, *,nick):
        await member.edit(nick=nick)
        embed = discord.Embed(title=f"Name changed", description=f"Succesfully changed {member.mention}'s name.", colour=0xff0000)
        await ctx.send(embed=embed)
    

    @commands.command(name="giverole", aliases=["gr"])
    async def _GiveRole(self, ctx, user : discord.Member, *, role : discord.Role):
        if ctx.author.guild_permissions.manage_messages or ctx.author.guild_permissions.administrator:
            await user.add_roles(role)
            embed = discord.Embed(title="Success!", description=f"Given {role.mention} to {user.mention}.", colour=0xff0000)
            embed.set_footer(text="Role Given")
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="You do not have the required permissions to do that!", colour=0xff0000)
            await ctx.send(embed=embed, delete_after=5)


    @commands.command(name="takerole", aliases=["tr"])
    async def _TakeRole(self, ctx, user : discord.Member, *, role : discord.Role):
        if ctx.author.guild_permissions.manage_messages or ctx.author.guild_permissions.administrator:
            await user.remove_roles(role)
            embed = discord.Embed(title="Success!", description=f"Taken {role.mention} from {user.mention}.", colour=0xff0000)
            embed.set_footer(text="Role Taken")
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="You do not have the required permissions to do that!", colour=0xff0000)
            await ctx.send(embed=embed, delete_after=5)
    


def setup(bot):
    bot.add_cog(User(bot))
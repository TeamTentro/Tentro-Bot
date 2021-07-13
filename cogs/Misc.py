from discord.ext import commands
from discord import Embed, Member, User, utils
import asyncio
import discord, random
from discord.ext.commands import bot
import discord, datetime
from discord import *
from discord.ext import commands
import os, random
from pathlib import Path


class Misc(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot

   

    

        
    

    @commands.command(name='welcome')
    async def welcome(self, ctx):
        guild = ctx.guild
        member_join = discord.on.member_join
        welcome_channel = bot.get_channel("Welcome")
        if ctx.author.has_permissions.administrator:
            await guild.create_text_channel("Welcome")
            embed = discord.Embed(title=f"Channel  has been created! Members who join will now be welcomed there.")
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)

        else:
            embed = Embed(title="You do not have the required permissions to do that!", colour=(0xff0000))
            await ctx.send(embed=embed, delete_after=5)

        if member_join:
            embed = discord.Embed(title=f"{member.mention} has joined the server!")
            await welcome_channel.send(embed=embed)
    
            

        











def setup(bot):
    bot.add_cog(Misc(bot))

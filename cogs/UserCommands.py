from discord.ext import commands
from discord import Embed, Member, User, client, utils
import asyncio
import discord
from discord.ext.commands import bot

class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    












def setup(bot):
    bot.add_cog(User(bot))
from discord.ext import commands
from discord import *
import discord, asyncio, datetime
import os


class InfoCommands(commands.Cog):
    def __innit__(self, client):
        self.client = client

def setup(client):
    client.add_cog(InfoCommands(client))

@commands.command(name="servername", aliases=["sn"])
async def _ServerName(self, ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", colour=0xff0000)
    embed.timestamp = ctx.message.created_at
    await ctx.send(embed=embed)

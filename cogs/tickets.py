from operator import is_not, not_
from discord import Embed, Member, User, channel, client, colour, guild, message, user, utils

from discord.ext import commands
import asyncio, discord
from discord.ext.commands import bot
from discord.ext.commands.errors import MissingPermissions
import random
from typing import Dict, List, Pattern, Set, Tuple, Union
import re, unicodedata
import cmath as math, sqlite3
from typing import List

from typing import Dict, List, Tuple, Union



class tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="help_tickets")
    async def help_ticket(self, ctx):
        embed = Embed(title="Tickets", description="ticket_add: Creates a ticket channel and category\nticket_remove: Deletes the ticket channel and category\nticket_addrole: Adds a role that will be able to see the tickets\nticket_removerole: Removes the role's permissions  to view tickets", colour=0xff0000)
        await ctx.send(embed=embed)



    @commands.command(name="tickets_add")
    async def tickets_add(self, ctx):
        cat = ctx.channel.category
        await ctx.guild.create_text_channel(name="tickets", category=cat)
        ticketchannel = discord.utils.get(ctx.guild.text_channels, name="tickets")
        default_role = ctx.guild.default_role
        await ticketchannel.set_permissions(target=default_role, speak=False, send_messages=False, read_message_history=True, read_messages=True)
        embedticketchannel = Embed(title="react to open le tivket", color=0xff000)
        ticketmsg = await ticketchannel.send(embed=embedticketchannel)
        await ticketmsg.add_reaction("🎫")
        await ctx.guild.create_category(name="🎫-Tickets")


    






def setup(bot):
    bot.add_cog(tickets(bot))
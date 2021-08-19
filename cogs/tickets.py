
from discord import Embed
from discord.ext import commands
import discord.utils


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
    @commands.is_owner()
    async def tickets_add(self, ctx):

        # Check if the category already exists
        ticketcat_e = discord.utils.get(ctx.guild.categories, name="🎫-Tickets")
        if ticketcat_e:
            return await ctx.send("Ticket category already exists, setup aborted.")
        else:
            ticketcat = await ctx.guild.create_category(name="🎫-Tickets")

        # Check if the text channel already exists
        ticketchannel_e = discord.utils.get(ctx.guild.text_channels, name="tickets")
        if ticketchannel_e:
            return await ctx.send("Ticket channel already exists, setup aborted.")
        else:
            ticketchannel = await ctx.guild.create_text_channel(name="tickets", category=ticketcat)

        default_role = ctx.guild.default_role
        await ticketchannel.set_permissions(target=default_role, speak=False, send_messages=False, read_message_history=True, read_messages=True, add_reactions=False)

        embedticketchannel = Embed(title=f"Tickets for {ctx.guild.name}", description="React to this message with '🎫' to open a ticket. Use tickets wisely and don't open them for dumb reasons.", color=0xc4f21d)
        ticketmsg = await ticketchannel.send(embed=embedticketchannel)
        await ticketmsg.add_reaction("🎫")

        addedembed = Embed(title="✅| Succesfully added the Tentro ticket system to this server. Run t!help_tickets for more info.", colour = 0x00ff00)
        await ctx.reply(embed=addedembed)

      


    @commands.command(name="tickets_remove")
    @commands.is_owner()
    async def tickets_remove(self, ctx):
        
        ticketcategory = discord.utils.get(ctx.guild.categories, name="🎫-Tickets")
        ticketchannel = discord.utils.get(ctx.guild.text_channels, name="tickets")
        if ticketcategory == None or ticketchannel == None:
            embed = Embed(title="✅| There are no ticket utils", colour = 0x00ff00)
            await ctx.reply(embed=embed)
        
        else:
          await ticketcategory.delete()
          await ticketchannel.delete()
          embed = Embed(title="✅| Successfully removed the ticket utilities from this server", colour = 0x00ff00)
          await ctx.reply(embed=embed)



    
   


    

def setup(bot):
    bot.add_cog(tickets(bot))

    
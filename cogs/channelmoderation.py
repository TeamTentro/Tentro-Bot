
from discord.ext import commands
from discord import Embed, Member, User, channel, utils
import asyncio, discord
from typing import Dict, List, Pattern, Set, Tuple, Union

from googlesearch import search

red = 0xff0000
green = 0x34eb40


class channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="google", aliases=["g"])
    async def google(self, ctx, *, text):
        if ctx.author.guild_permissions.manage_messages or ctx.author.guild_permissions.administrator:
            searchContent = f"{text}"
            searchContent = searchContent + text

            for j in search(f"{text}", tld="co.in", num=1, stop=1, pause=2):
                
                await ctx.channel.send(f"{j}")


   
  


   
    
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
    async def _CreateChannel(self, ctx, *, name=None):
        guild = ctx.message.guild
        if ctx.author.guild_permissions.administrator:
            cat = ctx.channel.category     
            discord.utils.get(ctx.guild.categories, id=cat)

            await guild.create_text_channel(name=name, category=cat)
            embed = discord.Embed(title=f"Channel {name} has been created!", colour=red)
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"You do not have the required permissions to do that!", colour=0xff0000)
            await ctx.send(embed=embed, delete_after=5)

    @commands.command(name="deletechannel", aliases=["deletech"])
    async def _DeleteChannel(self, ctx, textchannel: discord.TextChannel):
        guild = ctx.message.guild
        if ctx.author.guild_permissions.administrator:
            await textchannel.delete()
            embed = discord.Embed(title=f"Channel {textchannel} has been deleted!", colour=red)
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
        embedticketchannel = Embed(title="react to open le tivket", color=red)
        await ticketchannel.send(embed=embedticketchannel)
        await self.bot.add_reaction(embedticketchannel, "✅")


def setup(bot):
    bot.add_cog(channel(bot))
            

    


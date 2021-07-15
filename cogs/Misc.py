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
red = 0xff0000
green = 0x34eb40


class Misc(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot




    @commands.command(name="8ball")
    async def _8ball(self, ctx, *, question=None):
        responses = ["Definitely.", "It is certain", "Does 2 + 2 equal to 4?", "I don't think so chief.",
                "Perhaps.",
                "Maybe, ehhh don't take my word for it.",
                "Ask again.",
                "How do you not know this.", "I don't know, im just a discord bot.",
                "No clue bro.",
                "Uhhh Not sure about the answer to that one.", "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful.", "My sources say yes."]

        if question == None:
            await ctx.send("Please ask a question.", delete_after=5)
        else:
            embed = discord.Embed(title=f"Question:\n", description = f"{question}", color=0xff0000)
            embed.add_field(name = f"8ball:\n" ,value = f"{random.choice(responses)}")
            await ctx.send(embed=embed)

    @commands.command(name='say')
    async def say(self, ctx, *, text):
        if ctx.author.guild_permissions.administrator:
        
            message = ctx.message
            await message.delete()           
            await ctx.send(text)
        else:
            embed = Embed(title="You do not have the required permissions to do that!", colour=(0xff0000))
            await ctx.send(embed=embed, delete_after=5)


        
        


    @commands.command(name='rule')
    async def rule(self, ctx, *, text):
        if ctx.author.guild_permissions.administrator:
            message = ctx.message
            await message.delete()

            
            embed = Embed(title=f"     Rules", description=f"{text}", color=red)
            await ctx.send(embed=embed)
        

   

    

        
    

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

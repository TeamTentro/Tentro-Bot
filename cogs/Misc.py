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
import sqlite3

red = 0xff0000
green = 0x34eb40

intents = discord.Intents.default()

intents.members = True

class Misc(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        db = sqlite3.connect('tentro.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM tentro WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()
        
        if result is None:
            return
        else:
            cursor.execute(f"SELECT msg FROM tentro WHERE guild_id = {member.guild.id}")
            result1 = cursor.fetchone()
            members = len(list(member.guild.members))
            mention = member.mention
            user = member.name
            guild = member.guild
            

            embed = Embed(color=red, description=str(result1[0]).format(members=members, mention=mention, user=user, guild=guild))
            embed.set_thumbnail(url=f"{member.avatar_url}")  
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")          
            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")  
            embed.timestamp = datetime.datetime.now()                        ## F I X  T I M E S T A M P ! !
            

            channel = self.bot.get_channel(id=int(result[0]))

            await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_leave(self, member):
        print('This works?!')
        db = sqlite3.connect('leavecmd.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM leavecmd WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()
        
        
        if result is None:
            return
        else:
            cursor.execute(f"SELECT msg FROM tentro WHERE guild_id = {member.guild.id}")
            result1 = cursor.fetchone()
            members = len(list(member.guild.members))
            mention = member.mention
            user = member.name
            guild = member.guild

        

            embed = Embed(color=red, description=str(result1[0]).format(members=members, mention=mention, user=user, guild=guild))
            embed.set_thumbnail(url=f"{member.avatar_url}")  
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")          
            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")  
            embed.timestamp = datetime.datetime.now()                        ## F I X  T I M E S T A M P ! !
            

            channel = self.bot.get_channel(id=int(result[0]))

            await channel.send(embed=embed)




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
        

    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx):
        await ctx.send('Setup commands:\nwelcome channel <channel>\nwelcome text <message>')


    @welcome.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        if ctx.message.author.guild_permissions.administrator:
            db = sqlite3.connect('tentro.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM tentro WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO tentro(guild_id, channel_id) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Channel has been set to {channel.mention}")
            elif result is not None:
                sql = ("UPDATE tentro SET channel_id = ? WHERE guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"Channel has been updated to {channel.mention}") 
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @welcome.command()
    async def text(self, ctx, *, text):
        if ctx.message.author.guild_permissions.administrator:
            db = sqlite3.connect('tentro.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT msg FROM tentro WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO tentro(guild_id, msg) VALUES(?,?)")
                val = (ctx.guild.id, text)
                await ctx.send(f"Message has been set to {text}")
            elif result is not None:
                sql = ("UPDATE tentro SET msg = ? WHERE guild_id = ?")
                val = (text, ctx.guild.id)
                await ctx.send(f"Message has been updated to {text}") 
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()



    @commands.group(invoke_without_command=True)
    async def leave(self, ctx):
        await ctx.send('Setup commands:\nleave channel <channel>\nleave text <message>')


    @leave.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        if ctx.message.author.guild_permissions.administrator:
            db = sqlite3.connect('leavecmd.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM leavecmd WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO leavecmd(guild_id, channel_id) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Channel has been set to {channel.mention}")
            elif result is not None:
                sql = ("UPDATE leavecmd SET channel_id = ? WHERE guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"Channel has been updated to {channel.mention}") 
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            print('hi world')

    @leave.command()
    async def text(self, ctx, *, text):
        if ctx.message.author.guild_permissions.administrator:
            db = sqlite3.connect('leavecmd.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT msg FROM leavecmd WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO leavecmd(guild_id, msg) VALUES(?,?)")
                val = (ctx.guild.id, text)
                await ctx.send(f"Message has been set to {text}")
            elif result is not None:
                sql = ("UPDATE leavecmd SET msg = ? WHERE guild_id = ?")
                val = (text, ctx.guild.id)
                await ctx.send(f"Message has been updated to {text}") 
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            print('hello world')

    
            

        











def setup(bot):
    bot.add_cog(Misc(bot))

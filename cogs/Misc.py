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
from random import randint
sussy = "<:susimpostor:863852686600699904>"
time_convert = {"s":1, "m":60, "h":3600,"d":86400}

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
    async def on_member_remove(self, member):
        db = sqlite3.connect('tentro.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM leavecmd WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()
        
        
        if result is None:
            return
        else:
            cursor.execute(f"SELECT msg FROM leavecmd WHERE guild_id = {member.guild.id}")
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



    @commands.command(name="sus")
    async def sus(self, ctx, member: discord.Member = None):
        sus_precentage = randint(1,101)
        if member == None:
           embed = Embed(title=f"{ctx.author.name} is {sus_precentage}% sus.", colour = red)
           await ctx.send(embed = embed)
        else:
           embed = Embed(title=f"{member.name} is {sus_precentage}% sus.", colour = red)
           await ctx.send(embed = embed)

    @commands.command(name='say')
    async def say(self, ctx, *, text):
        if ctx.author.guild_permissions.kick_members:
        
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
        await ctx.send('Setup commands:\nwelcome channel <channel>\nwelcome message <message>')


    @welcome.command(name='channel')
    async def _channel(self, ctx, channel: discord.TextChannel):
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
    async def message(self, ctx, *, text):
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
            db = sqlite3.connect('tentro.sqlite')
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
            db = sqlite3.connect('tentro.sqlite')
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




    @commands.command(name="giveaway", aliases=["gw"])
    async def _Giveaway(self, ctx, time, *, prize):
        if ctx.author.guild_permissions.administrator:
          channel = ctx.channel
          author = ctx.author
          embed = Embed(title="🎉Giveaway🎉", description = f"{author.mention} is giving away ``{prize}``! The giveaway will end in {time}. To participate react to the message with 🎉", color = green)
          embed.set_footer(text="🍀Good luck🍀")
          embed.timestamp = ctx.message.created_at
          msg = await ctx.send(embed=embed)
          await msg.add_reaction('🎉')
          await msg.pin()
          duration = float(time[0: -1]) * time_convert[time[-1]]
          await asyncio.sleep(duration)
          new_msg = await channel.fetch_message(msg.id)
          users = await new_msg.reactions[0].users().flatten()
          try:
              users.pop(users.index(ctx.message.author.id))
          except ValueError:
              pass
       
          for user in users:
             if user.bot:
               users.remove(user)
          winner = random.choice(users)
        
          #anounces the winner
          embedwin = Embed(title = f"🎉Winner🎉", description = f"{winner.mention} has won the giveaway!", color = green)
          await ctx.send(embed=embedwin)
          #edits the old message
          await msg.unpin()
          afterembed = Embed(title="🎉Giveaway🎉", color = green)
          afterembed.add_field(name=f"Winner:", value=f"{winner.mention}", inline=False)
          afterembed.add_field(name=f"Hosted by:", value=f"{author.mention}", inline=False)
          afterembed.set_footer(text="The giveaway has ended")
          afterembed.timestamp = ctx.message.created_at
          await msg.edit(embed=afterembed)
          #dms the winner
          winnerdm = Embed(title = f"🎉Congratulations🎉", description =  f"You won a giveaway in {ctx.guild.name}! Your prize is: ``{prize}``. Contact {ctx.author} for more info.", color = green)
          await winner.send(embed = winnerdm)
        else:
            embed = Embed(title="You do not have the required permissions to do that!", colour=red)
            await ctx.send(embed=embed, delete_after=5)

    @commands.command(name='emoji', aliases=['em'])
    async def emoji(self, ctx, emoji: Emoji):
        discord.utils.get(emoji)
        await ctx.send(emoji.url)


    


    
            

        



def setup(bot):
    bot.add_cog(Misc(bot))

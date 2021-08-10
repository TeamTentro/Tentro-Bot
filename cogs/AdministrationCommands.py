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
import lib as mod
from typing import Dict, List, Tuple, Union



red = 0xff0000
green = 0x34eb40

time_convert = {"s":1, "m":60, "h":3600,"d":86400}

__MINUTES = 60
__HOURS = __MINUTES * 60
__DAYS = __HOURS * 24


class Command:
    __arguments: Dict[str, Union[str, int]]


    def get_value_of(self, name: str) -> Union[None, str, int]:
        if name in self.__arguments:
            return self.__arguments[name]
        return None

    def get_content(self) -> Union[None, str]:
        if "content" in self.__arguments:
            return self.__arguments["content"]
        return None


def get_time(command: Command) -> Union[None, int]:
    seconds: int = 0
    time_given: bool = False
    for (name, ratio) in _RATIOS:
        time: Union[str, int] = command.get_value_of(name)
        if time is not None and isinstance(time, int):
            time_given = True
            seconds += time * ratio
    if time_given:
        return seconds
    return None

def eligible(member: Member) -> bool:
    return member.guild_permissions.administrator or member.guild_permissions.manage_messages

class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    


   
    
   

    @commands.command(name="mute", aliases=["m"])
    async def _Mute(self, ctx,  member: Member, time=None, *, reason=None):
#this is where the shit mute command is
        
        if not eligible(ctx.author):
            await ctx.send("You dont have the required permissions to do that!", delete_after=5)
            return

        guild = ctx.guild
        mutedRole = utils.get(guild.roles, name="Muted")## this gets a role named muted if there is one
        if time is None:  # if there is no time it will do:
            guild = ctx.guild
            mutedRole = utils.get(guild.roles, name="Muted") #this gets a role named muted if there is one
            if not mutedRole: #if there is no mutedrole
                mutedRole = await guild.create_role(name="Muted", colour=green)
                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, read_messages=False) #it will set permissions to this
            else:
                await member.add_roles(mutedRole, reason=reason) #adds muted role to user
                muted_role = utils.get(ctx.guild.roles, name="Muted") 
                await member.add_roles(muted_role)

                embed = Embed(description=f"**{member.mention} has been muted indefinitely.\nReason:{reason}**", color=red) #embed of the information
                embed.timestamp = ctx.message.created_at
                await ctx.send(embed=embed)

                embed = Embed(title=f"You have been muted in: {guild.name}.\n**Time period:** indefinitely.\n**Reason:**{reason}", colour=red)
                await member.send(embed=embed)

        elif time is not None and not mutedRole: # if there is time specified and there is not mutedrole
            mutedRole = await guild.create_role(name="Muted", colour=green) #creates mutedrole
            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, read_messages=False) #sets permissions
        else:
            await member.add_roles(mutedRole, reason=reason)
            muted_role = utils.get(ctx.guild.roles, name="Muted")
            await member.add_roles(muted_role) #adds it to user

            embed = Embed(description=f"**{member.mention} has been muted for {time}.\nReason:{reason}**", color=red)
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)  
                 #aall this here is info in embed

            embed = Embed(title=f"You have been muted in: {guild.name}.\n**Time period:** {time}.\n**Reason:**{reason}", colour=red) 
            await member.send(embed=embed)

            duration = float(time[0: -1]) * time_convert[time[-1]]  #now this is the time cmd
            await asyncio.sleep(duration) # asyncio.sleep duration = specified time
            await member.remove_roles(muted_role) #after time is over remove user's roles

            embed = Embed(title=f"You have been unmuted in: {guild.name}.", colour=red)
            await member.send(embed=embed)                     #more info
      
      
  


  
       
    @commands.command(name="unban", aliases=["ub", "bebis4u"])
    async def _Unban(self, ctx, *, user: User):
        member = Member

        if ctx.author.guild_permissions.administrator:
            await ctx.guild.unban(user=user)
            embed = Embed(title="Success!", description=f"{user} has been sucessfully unbanned!", colour=red)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title="You do not have the required permissions to do that!", colour=red)
            await ctx.send(embed=embed, delete_after=5)

    @commands.command(description="Unmutes a specified user.")
    async def unmute(self, ctx, member: Member):

        if ctx.author.guild_permissions.manage_messages or ctx.author.guild_permissions.administrator and ctx.member.guild_permissions!=ctx.author.guild_permissions:
            mutedRole = utils.get(ctx.guild.roles, name="Muted")
            await member.remove_roles(mutedRole)

            embed = Embed(title="Unmuted", description=f"{member.mention} has been unmuted.",colour=red)
            embed.set_footer(text="Unmute") # Inconsistant use of footers and timestamps
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)

            embed = Embed(title = (f"You have been unmuted in: **{ctx.guild.name}.**"), colour=red)
            await member.send(embed=embed)
        else:
            embed = Embed(title="You do not have the required permissions to do that!", colour=red)
            await ctx.send(embed=embed, delete_after=5)

    @commands.command(name="warn")
    async def warn(self, ctx, member: Member, *, reason=None):
        if ctx.author.guild_permissions.manage_messages or ctx.author.guild_permissions.administrator and ctx.author.guild_permissions!=ctx.member.guild_permissions:
            embed = Embed(title="Warn", description=f"{member.mention} has been succesfully warned.", color=red )
            embed.set_footer(text="Warn")
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
            embed = Embed(title=f"You have been warned in {ctx.guild.name}. Reason: {reason}.", color=red )
            try:              
               await member.send(embed=embed)
            except:
                pass
        else:
            embed = Embed(title="You do not have the required permissions to do that!", colour=red)
            await ctx.send(embed=embed, delete_after=5)
    

    
    @commands.command(name="kick", aliases=["k", "yeet"])
    async def kick(self, ctx, member: Member, *, reason=None):
        guild = ctx.guild
        if ctx.author.guild_permissions.kick_members or ctx.author.guild_permissions.administrator:
            
            await member.kick(reason=reason)
            embed = Embed(title="Kicked", description=f"{member.mention} has been kicked from the server.", colour=red)
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.set_footer(text="Kick")
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
            embed = discord.Embed(title=f"You have been kicked from {guild.name}\nReason: {reason}", colour=red)
            try:
                await member.send(embed=embed)
            except:
                pass
            

        
            

            # Not needed
            #embed = Embed(title = (f"You have been kicked from: {ctx.guild.name}.\n**Reason:** {reason}."), colour=red)
            #await member.send(embed=embed)
      
            

    @commands.command(name="ban", aliases=["b", "nobebis4u"])
    async def ban(self, ctx, member: Member, *,time=None, reason=None):
        guild = ctx.guild
        user = User

        if ctx.author.guild_permissions.ban_members or ctx.author.guild_permissions.administrator and ctx.author.guild_permissions!=ctx.member.guild_permissions:

        
            if time==None: 
                await member.ban(reason=reason) 
                embed = Embed(title="Banned", description=f"{member.mention} has been banned from the server indefinitely.", colour=red)
                embed.add_field(name="Reason:", value=reason, inline=False)
                embed.set_footer(text="Ban")
                embed.timestamp = ctx.message.created_at
                await ctx.send(embed=embed)  
                embed = discord.Embed(title=f"You have been banned from {guild.name}\nReason: {reason}\nTime period: indefinitely", colour=red)
                try: 
                    await member.send(embed=embed)
                except:
                    pass
        


            
            else:     ## IF TIME IS WRITTEN
                await member.ban(reason=reason)
                embed = Embed(title="Banned", description=f"{member.mention} has been banned from the server.", colour=red)
                embed.add_field(name="Reason:", value=reason, inline=False)
                embed.add_field(name=f"Time period:", value=time)
                embed.set_footer(text="Ban")
                embed.timestamp = ctx.message.created_at
                await ctx.send(embed=embed)               
                embed = discord.Embed(title=f"You have been banned from {guild.name}\nReason: {reason}\nTime period:{time}", colour=red)
                try:
                    await member.send(embed=embed)
                except:
             
                    await ctx.send("Member is not in any mutual server or has dm's blocked!", delete_after=4)

                
                duration = int(time[0: -1]) * time_convert[time[-1]]
                await asyncio.sleep(duration)
                await ctx.guild.unban(user=member)
        else:
            embed = Embed(title="You do not have the required permissions to do that!", colour=red)
            await ctx.send(embed=embed, delete_after=5)

        
           # Not needed
            #embed = Embed(title = (f"You have been banned from: {ctx.guild.name}.\n**Reason:** {reason}."), colour=red)
            #await member.send(embed=embed)


__MINUTES = 60
__HOURS = __MINUTES * 60
__DAYS = __HOURS * 24


_TYPES: List[Tuple[str, str]] = [
    ("seconds", "s"), ("minutes", "m"), ("hours", "h"), ("days", "d")]
_RATIOS: List[Tuple[str, int]] = [
    ("seconds", 1), ("minutes", __MINUTES), ("hours", __HOURS), ("days", __DAYS)]



















        

def setup(bot):
    bot.add_cog(admin(bot)) 
    
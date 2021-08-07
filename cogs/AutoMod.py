from cogs.ChannelModeration import Channel
from operator import is_not, not_
from discord.ext import commands
from discord import Embed, Member, User, channel, client, colour, guild, message, user, utils
import asyncio, discord
from discord.ext.commands import bot
from discord.ext.commands.errors import MissingPermissions
import random
from typing import Dict, List, Pattern, Set, Tuple, Union
import re, unicodedata
import cmath as math
from typing import List
import lib.automod as mod




ACTIVATED_COLOR = 0x00ff00
DEACTIVATED_COLOR = 0xff0000
RED = 0xff0000
DELETE_TIME: float = 5

_BLACK_LIST = ["dood"]
_FILLERS = [" ", "\-", "_"]




class AutoMod(commands.Cog):
    

    def __init__(self, bot):
        self.bot = bot


    activated: bool
    blacklist: List[str]
    Toggle: bool

    Toggle = False
    @commands.command(name="automod")
    async def _automod(self, ctx):
        if not eligible(ctx.author):
            return

        global Toggle       
        Toggle = True
    

        if not eligible(ctx.author):
            return
        
            
        
        await ctx.message.add_reaction("✅")
               

    @commands.Cog.listener()
    async def on_message(self, message):
  
        if Toggle == True:
            try:
                message = message
                bl_words = mod.check_bl(str(message.content), _BLACK_LIST, bl_algorithms=[
                mod.check_bl_direct(), mod.check_bl_fillers()], fillers=_FILLERS)
                if bl_words:
                    embed = discord.Embed(title = "You said a blacklisted word.")
                    await message.channel.send(embed=embed, delete_after=3)
                    await message.delete()
                


                spam_probability = mod.get_spam_probability(str(message.content), spam_algorithms=[mod.check_spam_alternating_cases(
                ), mod.check_spam_by_repetition(), mod.check_spam_repeating_letters(), mod.check_spam_caps()])
                if spam_probability > 0.5:
                    embed = discord.Embed(title="Dont spam in this channel!")
                    await message.channel.send(embed=embed, delete_after=3)  
                    await message.delete()             
                
            except:
                pass
       

def eligible(member: Member) -> bool:
    return member.guild_permissions.administrator


   
        

    







def setup(bot):
    bot.add_cog(AutoMod(bot))
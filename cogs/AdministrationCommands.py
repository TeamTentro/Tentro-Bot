from operator import is_not, not_
from discord.ext import commands
from discord import Embed, Member, User, channel, client, guild, message, utils
import asyncio, discord
from discord.ext.commands.errors import MissingPermissions
import random


red = 0xff0000
green = 0x34eb40

time_convert = {"s":1, "m":60, "h":3600,"d":86400}

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    
    
   

    @commands.command(name="mute", aliases=["m"])
    async def _Mute(self, ctx,  member: Member, time=None, *, reason=None):

        if ctx.author.guild_permissions.manage_messages and member.guild_permissions!=ctx.author.guild_permissions:
            guild = ctx.guild
            mutedRole = utils.get(guild.roles, name="Muted")
            if time==None:
                guild = ctx.guild
                mutedRole = utils.get(guild.roles, name="Muted")
                if not mutedRole:
                    mutedRole = await guild.create_role(name="Muted", colour=green)
                    for channel in guild.channels:
                        await channel.set_permissions(mutedRole, speak=False, read_messages=False)
                else:
                    await member.add_roles(mutedRole, reason=reason)
                    muted_role = utils.get(ctx.guild.roles, name="Muted")
                    await member.add_roles(muted_role)

                    embed = Embed(description=f"**{member.mention} has been muted indefinitely.\nReason:{reason}**", color=red)
                    embed.timestamp = ctx.message.created_at
                    await ctx.send(embed=embed)

                    embed = Embed(title=f"You have been muted in: {guild.name}.\n**Time period:** indefinitely.\n**Reason:**{reason}", colour=red)
                    await member.send(embed=embed)

            elif time!=None and not mutedRole:
                mutedRole = await guild.create_role(name="Muted", colour=green)
                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, read_messages=False)
            else:
                await member.add_roles(mutedRole, reason=reason)
                muted_role = utils.get(ctx.guild.roles, name="Muted")
                await member.add_roles(muted_role)

                embed = Embed(description=f"**{member.mention} has been muted for {time}.\nReason:{reason}**", color=red)
                embed.timestamp = ctx.message.created_at
                await ctx.send(embed=embed)

                embed = Embed(title=f"You have been muted in: {guild.name}.\n**Time period:** {time}.\n**Reason:**{reason}", colour=red)
                await member.send(embed=embed)

                duration = float(time[0: -1]) * time_convert[time[-1]]
                await asyncio.sleep(duration)
                await member.remove_roles(muted_role)

                embed = Embed(title=f"You have been unmuted in: {guild.name}.", colour=red)
                await member.send(embed=embed)
          
            
            
        else:
            await ctx.send("You dont have the required permissions to do that!", delete_after=5)

    @commands.command(name="giveaway", aliases=["gw"])
    async def _Giveaway(self, ctx, time, *, prize):
        channel = ctx.channel
        author = ctx.author
        embed = Embed(title="🎉Giveaway🎉", description = f"{author.mention} is giving away {prize}! The giveaway will end in {time}. To participate react to the message with 🎉", color = green)
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

        winner = random.choice(users)
        embedwin = Embed(title = f"🎉Winner🎉", description = f"{winner.mention} has won the giveaway!")
        await ctx.send(embed=embedwin)
       


       
    @commands.command(name="unban", aliases=["ub", "bebis4u"])
    async def _Unban(self, ctx, *, user: User):
        member = Member

        if ctx.author.guild_permissions.administrator and member.guild_permissions!=ctx.author.guild_permissions:
            await ctx.guild.unban(user=user)
            embed = Embed(title="Success!", description=f"{user} has been sucessfully unbanned!", colour=red)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title="You do not have the required permissions to do that!", colour=red)
            await ctx.send(embed=embed, delete_after=5)

    @commands.command(description="Unmutes a specified user.")
    async def unmute(self, ctx, member: Member):

        if ctx.author.guild_permissions.manage_messages and member.guild_permissions!=ctx.author.guild_permissions:
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
        if ctx.author.guild_permissions.manage_messages and member.guild_permissions!=ctx.author.guild_permissions:
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

        if ctx.author.guild_permissions.kick_members and member.guild_permissions!=ctx.author.guild_permissions:
            
            await member.kick(reason=reason)
            embed = Embed(title="Kicked", description=f"{member.mention} has been kicked from the server.", colour=red)
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.set_footer(text="Kick")
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
            embed = discord.Embed(title=f"You have been kicked from {guild.name}\nReason: {reason}", colour=red)
            try:
                await member.send(embed=embed)
            except:()

        embed = Embed(title="You do not have the required permissions to do that!", colour=red)
        await ctx.send(embed=embed, delete_after=5)
            

            # Not needed
            #embed = Embed(title = (f"You have been kicked from: {ctx.guild.name}.\n**Reason:** {reason}."), colour=red)
            #await member.send(embed=embed)
      
            

    @commands.command(name="ban", aliases=["b", "nobebis4u"])
    async def ban(self, ctx, member: Member, *,time=None, reason=None):
        guild = ctx.guild
        user = User

        if ctx.author.guild_permissions.administrator and member.guild_permissions!=ctx.author.guild_permissions: ## and not same perms FIX
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
                except:()
        


            
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

                
                duration = float(time[0: -1]) * time_convert[time[-1]]
                await asyncio.sleep(duration)
                await ctx.guild.unban(user=member)

        embed = Embed(title="You do not have the required permissions to do that!", colour=red)
        await ctx.send(embed=embed, delete_after=5)
            
 


            # Not needed
            #embed = Embed(title = (f"You have been banned from: {ctx.guild.name}.\n**Reason:** {reason}."), colour=red)
            #await member.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Admin(bot)) 
    
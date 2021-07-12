from discord.ext import commands
from discord import Embed, Member, User, client, utils
import asyncio, discord


red = 0xff0000
green = 0x34eb40

time_convert = {"s":1, "m":60, "h":3600,"d":86400}

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="timedmute", aliases=["tm"])
    async def _Mute(self, ctx, member: Member, time, *, reason=None):

        if ctx.author.guild_permissions.manage_messages:
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

                embed = Embed(description=f"**{member.mention} has been muted for {time}**", color=red)
                embed.timestamp = ctx.message.created_at
                await ctx.send(embed=embed)

                embed = Embed(title=f"You have been muted in: {guild.name}.\n**Time period:** {time}.", colour=red)
                await member.send(embed=embed)

                duration = float(time[0: -1]) * time_convert[time[-1]]
                await asyncio.sleep(duration)
                await member.remove_roles(muted_role)

                embed = Embed(title=f"You have been unmuted in: {guild.name}.", colour=red)
                await member.send(embed=embed)
        else:
            await ctx.send("You dont have the required permissions to do that!", delete_after=5)

    @commands.command(name="unban", aliases=["ub", "bebis4u"])
    async def _Unban(self, ctx, *, user: User):

        if ctx.author.guild_permissions.administrator:
            await ctx.guild.unban(user=user)
            embed = Embed(title="Success!", description=f"{user} has been sucessfully unbanned!", colour=red)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title="You do not have the required permissions to do that!", colour=red)
            await ctx.send(embed=embed, delete_after=5)

    @commands.command(description="Unmutes a specified user.")
    async def unmute(self, ctx, member: Member):

        if ctx.author.guild_permissions.manage_messages:
            mutedRole = utils.get(ctx.guild.roles, name="Muted")
            await member.remove_roles(mutedRole)

            embed = Embed(title="Unmuted", description=f"{member.mention} has been unmuted.",colour=red)
            embed.set_footer(text="Unmute") # Inconsistant use of footers and timestamps
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)

            embed = Embed(title = (f"You have been unmuted in: **{ctx.guild.name}.**"), colour=red)
            await member.send(embed=embed)
        else:
            await ctx.send("You dont have the required permissions to do that!", delete_after=5)

    @commands.command(name="mute", aliases=['m', 'shut'])
    async def mute(self, ctx, member: Member, *, reason=None):

        permissions = ctx.message.author.guild_permissions
        if permissions.kick_members or permissions.administrator:
            guild = ctx.guild

            mutedRole = utils.get(guild.roles, name="Muted")
            if not mutedRole:
                mutedRole = await guild.create_role(name="Muted", colour=green)
                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, read_messages=False)

            await member.add_roles(mutedRole, reason=reason)

            embed = Embed(title="Muted", description=f"{member.mention} has been muted indefinitely.", colour=red)
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.set_footer(text="Mute")
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)

            embed = Embed(title=f"You have been muted in: {guild.name}.\n**Reason:** {reason}.", colour=red)
            await member.send(embed=embed)
        else:
            embed = Embed(title="You do not have the required permissions to do that!", colour=red)
            await ctx.send(embed=embed, delete_after=5)

    @commands.command(name="kick", aliases=["k", "yeet"])
    async def kick(self, ctx, member: Member, *, reason=None):
        guild = ctx.guild

        if ctx.author.guild_permissions.kick_members:
            

            embed = Embed(title="Kicked", description=f"{member.mention} has been kicked from the server.", colour=red)
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.set_footer(text="Kick")
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
            embed = discord.Embed(title=f"You have been kicked from {guild.name}\nReason: {reason}", colour=red)
            await member.send(embed=embed)
            await member.kick(reason=reason)

            # Not needed
            #embed = Embed(title = (f"You have been kicked from: {ctx.guild.name}.\n**Reason:** {reason}."), colour=red)
            #await member.send(embed=embed)
        else:
            embed = Embed(title="You do not have the required permissions to do that!", colour=red)
            await ctx.send(embed=embed, delete_after=5)

    @commands.command(name="ban", aliases=["b", "nobebis4u"])
    async def ban(self, ctx, member: Member, *, reason=None):
        guild = ctx.guild

        if ctx.author.guild_permissions.manage_messages:
            

            embed = Embed(title="Banned", description=f"{member.mention} has been banned from the server.", colour=red)
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.set_footer(text="Ban")
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
            embed = discord.Embed(title=f"You have been banned from {guild.name}\nReason: {reason}", colour=red)
            await member.send(embed=embed)
            await member.ban(reason=reason)

            # Not needed
            #embed = Embed(title = (f"You have been banned from: {ctx.guild.name}.\n**Reason:** {reason}."), colour=red)
            #await member.send(embed=embed)
        else:
            embed = Embed(title="You do not have the required permissions to do that!", colour=red)
            await ctx.send(embed=embed, delete_after=5)

def setup(bot):
    bot.add_cog(Admin(bot)) 
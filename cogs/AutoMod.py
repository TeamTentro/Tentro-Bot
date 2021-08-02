from discord.ext import commands
from discord import Embed, Member, User, channel, client, colour, guild, message, user, utils
from discord.ext.commands import bot
from discord.ext.commands.errors import MissingPermissions
from typing import List
import lib.automod as mod


ACTIVATED_COLOR = 0x00ff00
DEACTIVATED_COLOR = 0xff0000
RED = 0xff0000
DELETE_TIME: float = 5


_BLACK_LIST = ["Dood"]
_FILLERS = [" ", "-", "_"]


class AutoMod(commands.Cog):
    activated: bool
    blacklist: List[str]

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="automod", aliases=["s"])
    async def _automod(self, ctx, member: Member):
        self.activated = not self.activated
        if not eligible(member):
            return
        bot_activation(self.activated, ctx)

    @bot.event
    async def on_message(message):
        bl_words = mod.check_bl(message, _BLACK_LIST, bl_algorithms=[
            mod.check_bl_direct(), mod.check_bl_fillers()], fillers=_FILLERS, color=RED)
        embed = Embed("You dare say!", description=" ".join(bl_words))
        message.channel.send(embed)

        spam_probability = mod.get_spam_probability(message, spam_algorithms=[mod.check_spam_alternating_cases(
        ), mod.check_spam_by_repetition(), mod.check_spam_repeating_letters(), mod.check_spam_caps()])
        if spam_probability > 0.75:
            embed = Embed("You dare spam!", description=":angry:")
            message.channel.send(embed)


def eligible(member: Member) -> bool:
    return member.guild.permissions.administrator


def bot_activation(activated: bool, ctx):
    color, activation_text = (ACTIVATED_COLOR, "Activated") if activated else (
        DEACTIVATED_COLOR, "Deactivated")
    embed = Embed(title=f"Automod {activation_text}", color=color)
    ctx.send(send=embed, delete_after=DELETE_TIME)


def setup(bot):
    bot.add_cog(AutoMod(bot))

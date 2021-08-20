
from discord import Embed
from discord.ext import commands
import discord.utils, sqlite3


from operator import is_not, not_
from discord import Embed, Member, User, channel, client, colour, guild, message, user, utils

class tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    




    @commands.command(name="help_tickets")
    async def help_ticket(self, ctx):
        embed = Embed(title="Tickets", description="ticket_add: Creates a ticket channel and category, you can also add a custom message to it, if not it will use a default message we have set\nticket_remove: Deletes the ticket channel and category\nticket_addrole: Adds a role that will be able to see the tickets\nticket_removerole: Removes the role's permissions  to view tickets", colour=0xff0000)
        await ctx.send(embed=embed)

    @commands.command(name="tickets_add")
    @commands.is_owner()
    async def tickets_add(self, ctx, *, text=None):
        db = sqlite3.connect('tentro.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT msg FROM ticket WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
       
        

        # Check if the category already exists
        ticketcat_e = discord.utils.get(ctx.guild.categories, name="🎫-Tickets")
        if ticketcat_e:
            return await ctx.send("Ticket category already exists, setup aborted.")
        else:
            ticketcat = await ctx.guild.create_category(name="🎫-Tickets")

        # Check if the text channel already exists
        ticketchannel_e = discord.utils.get(ctx.guild.text_channels, name="ticketinfo")
        if ticketchannel_e:
            return await ctx.send("Ticket channel already exists, setup aborted.")
        else:
            ticketchannel = await ctx.guild.create_text_channel(name="ticketinfo", category=ticketcat)

        default_role = ctx.guild.default_role
        await ticketchannel.set_permissions(target=default_role, speak=False, send_messages=False, read_message_history=True, read_messages=True, add_reactions=False)
        if text:
            embedticket = Embed(title=f"Tickets for {ctx.guild.name}", description=f"{text}", color =0xff0000)
            ticketmsg = await ticketchannel.send(embed=embedticket)
            await ticketmsg.add_reaction("🎫")
            addedembed = Embed(title="✅| Succesfully added the Tentro ticket system to this server. Run t!help_tickets for more info.", colour = 0x00ff00)
            await ctx.send(embed=addedembed)
            
            print(ticketmsg.id)
            cursor.execute(f"SELECT msg_id FROM ticket WHERE guild_id = {ctx.guild.id}")
            result2 = cursor.fetchone()
            if result2 is None:
                sql = ("INSERT INTO ticket(guild_id, msg_id) VALUES(?,?)")
                val = (ctx.guild.id, ticketmsg.id)
                await ctx.send(f"Title has been set to {text}")
            elif result2 is not None:
                sql = ("UPDATE ticket SET msg_id = ? WHERE guild_id = ?")
                val = (ticketmsg.id, ctx.guild.id)
                await ctx.send(f"Msg id  has been set")
                cursor.execute(sql, val)
            print(result2)
 
            
            

        elif text==None:
            embedticketchannel = Embed(title=f"Tickets for {ctx.guild.name}", description="React to this message with '🎫' to open a ticket. Use tickets wisely and don't open them for dumb reasons.", color=0xc4f21d)
            ticketmsg = await ticketchannel.send(embed=embedticketchannel)
            await ticketmsg.add_reaction("🎫")

            addedembed = Embed(title="✅| Succesfully added the Tentro ticket system to this server. Run t!help_tickets for more info.", colour = 0x00ff00)
            await ctx.reply(embed=addedembed)

        if result and text==None:
            return


        if result:
            sql = ("UPDATE ticket SET msg = ? WHERE guild_id = ?")
            val = (text, ctx.guild.id)
            await ctx.reply(f"Ticket message has been set!")
        print(sql)
        print(val)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

      


    @commands.command(name="tickets_remove")
    @commands.is_owner()
    async def tickets_remove(self, ctx):
        
        ticketcategory = discord.utils.get(ctx.guild.categories, name="🎫-Tickets")
        ticketchannel = discord.utils.get(ctx.guild.text_channels, name="ticketinfo")
        if ticketcategory == None or ticketchannel == None:
            embed = Embed(title="✅| There are no ticket utils", colour = 0x00ff00)
            await ctx.reply(embed=embed)
        
        else:
          await ticketcategory.delete()
          await ticketchannel.delete()
          embed = Embed(title="✅| Successfully removed the ticket utilities from this server", colour = 0x00ff00)
          await ctx.reply(embed=embed)

    @commands.command(name="roleperm")
    @commands.is_owner()
    async def roleperm(self, ctx, role: discord.Role):
        db = sqlite3.connect('tentro.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT role_id FROM ticket WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO ticket(guild_id, role_id) VALUES(?,?)")
            val = (ctx.guild.id, role)
            await ctx.send(f"Role_id has been set to {role}")
        elif result is not None:
            sql = ("UPDATE ticket SET role_id = ? WHERE guild_id = ?")
            val = (role, ctx.guild.id)
            await ctx.send(f"Role_id has been updated to {role}") 
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        
            

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        member = payload.member

        db = sqlite3.connect('tentro.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT msg_id FROM ticket WHERE EXISTS(SELECT msg_id FROM ticket WHERE guild_id=?)", (payload.guild_id,))
        result_3 = cursor.fetchone()
      

        if payload.message_id == result_3[0] and member is not None:
            
            guild_id = payload.guild_id
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = self.bot.get_user(payload.user_id)
            guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
            emoji = payload.emoji.name
 
            name = payload.member.name     
            role2 = discord.utils.get(guild.roles, name="@everyone")
            ticketcategory = discord.utils.get(guild.categories, name="🎫-Tickets")

            tick = await guild.create_text_channel(name=f"ticket-{name}", category=ticketcategory)
            await message.remove_reaction(emoji, user)
            await tick.set_permissions(target=role2, speak=False, send_messages=False, read_message_history=False, read_messages=False, add_reactions=False, view_channel=False)
            await tick.set_permissions(target=user, speak=True, send_messages=True, read_message_history=True, read_messages=True, view_channel=True, add_reactions=False)

            


        guild_id = payload.guild_id
        guild = self.bot.get_guild(guild_id)

        user_id = payload.user_id
        user = self.bot.get_user(user_id)

        channel_id = payload.channel_id
        channel = self.bot.get_channel(channel_id)

        message_id = payload.message_id
        emoji = payload.emoji.name

   

    

def setup(bot):
    bot.add_cog(tickets(bot))
    
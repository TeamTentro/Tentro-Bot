# Import Discord Package

import discord, asyncio, datetime
from discord import *
from discord.ext import commands
import os, random
from pathlib import Path

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

#Client

client = commands.Bot(command_prefix='t!')


#le status

@client.event
async def on_ready():

    general_channel = client.get_channel(745925853229350975)

    await general_channel.send('Bot is online!')
    await client.change_presence(activity=discord.Game(name='t!help for Help!'))

#C O M M A N D S


@client.command(name='8ball')
async def eightball(ctx, *, question=None):
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
        await ctx.send('Please ask a question.', delete_after=5)

    else:
        embed = discord.Embed(title=f"**Question:**\n", description = f"{question}", color = (0xff0000))
        embed.add_field(name = f"**8ball:**\n" ,value = f"{random.choice(responses)}")
        
        
        
        await ctx.send(embed=embed)




@client.event
async def on_message(message):
    if message.content == 't!help' or message.content == 't!h':
      
        myEmbed = discord.Embed(title="These are all the commands", color=0xFF0000)
        myEmbed.add_field(name="Available commands:", value="!tclear, !tban, !tkick, !tmute, !tunban, !tunmute, !tping, !tserver", inline=False)
        myEmbed.add_field(name="Bot version:", value="v1.0", inline=False)
        myEmbed.add_field(name="Date released:", value="July 6th", inline=False)
        myEmbed.set_footer(text="Still in progress!")
        myEmbed.set_author(name=message.author.name)
        myEmbed.timestamp = message.created_at
       
        await message.channel.send(embed=myEmbed)
      
    elif message.content =='!t':
     
     await message.channel.send('This is the default prefix')


    if message.content == "hi":     

        await message.channel.send("Hello There")  

    await client.process_commands(message)
    


@client.command(name='slowmode', aliases=['sm'])
async def setdelay(ctx, seconds : int):
  guild = ctx.guild
  if ctx.author.guild_permissions.manage_messages:
      await ctx.channel.edit(slowmode_delay=seconds)
      embed = discord.Embed(title=f'Slowmode set to {seconds}s.', colour=discord.Color(0xff0000))
      await ctx.send(embed=embed)
  else:
      embed = discord.Embed(title=f'You do not have the required permissions to do that!', colour=discord.Color(0xff0000))
      await ctx.send(embed=embed, delete_after=5)

@client.command(name='createchannel', aliases=['createch'])
async def createchannel(ctx, name=None):
    guild = ctx.message.guild
    if ctx.author.guild_permissions.administrator:
        await guild.create_text_channel(name=name)
        embed = discord.Embed(title=f"Channel {name} has been created!")
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)


    else:
        embed = discord.Embed(title=f'You do not have the required permissions to do that!', colour=discord.Color(0xff0000))
        await ctx.send(embed=embed, delete_after=5)





@client.command(name='slowmodecheck', aliases=['checksm'])
async def checkdelay(ctx):
    seconds = ctx.channel.slowmode_delay
    
    if ctx.author.guild_permissions.manage_messages:
        embed = discord.Embed(title=f'Slowmode is {seconds}s.', colour=discord.Colour(0xff0000))
        await ctx.send(embed=embed)
    
    else:
        embed = discord.Embed(title=f'You do not have the required permissions to do that!', color=discord.Colour(0xff0000))
        await ctx.send(embed=embed, delete_after=4)


   

@client.command(name='avatar', aliases=['av'])
async def avatar(ctx, *, member: discord.Member = None):
    member = ctx.author if not member else member
    embed = discord.Embed(title = f"{member.name}", color = (0xff0000), timestamp = ctx.message.created_at)
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"Requested by : {ctx.author}",icon_url=ctx.author.avatar_url)  
    await ctx.send(embed=embed)




    
@client.command(name='giverole', aliases=['gr'])
async def role(ctx, user : discord.Member, *, role : discord.Role):
    guild = ctx.guild
    if ctx.author.guild_permissions.manage_messages or ctx.author.guild_permissions.administrator:
        await user.add_roles(role)
        embed = discord.Embed(title='Success!', description=f"Given {role.mention} to {user.mention}.", colour=discord.Color(0xff0000))
        embed.set_footer(text='Role Given')
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='You do not have the required permissions to do that!', colour=discord.Color(0xff0000))
        await ctx.send(embed=embed, delete_after=5)
     


@client.command(name='takerole', aliases=['tr'])
async def role(ctx, user : discord.Member, *, role : discord.Role):
    guild = ctx.guild
    if ctx.author.guild_permissions.manage_messages or ctx.author.guild_permissions.administrator:
        await user.remove_roles(role)
        embed = discord.Embed(title='Success!', description=f"Taken {role.mention} from {user.mention}.", colour=discord.Color(0xff0000))
        embed.set_footer(text='Role Taken')
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='You do not have the required permissions to do that!', colour=discord.Color(0xff0000))
        await ctx.send(embed=embed, delete_after=5)



@client.command(name='clear', aliases=['cl'])
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit = amount+1)
    embed = discord.Embed(title = 'Messages purged', description=f"{ctx.author.mention}, purged {amount} message(s)", colour=discord.Color(0xff0000))
    await ctx.send(embed=embed, delete_after=5)


     
@client.command(name='resetslowmode', aliases=['rsm'])
async def setdelay(ctx):
  guild = ctx.guild
  if ctx.author.guild_permissions.manage_messages:
      await ctx.channel.edit(slowmode_delay=0)
      embed = discord.Embed(title=f'Slowmode reset.', colour=discord.Color(0xff0000))
      await ctx.send(embed=embed)
  else:
      embed = discord.Embed(title=f'You do not have the required permissions to do that!', colour=discord.Color(0xff0000))
      await ctx.send(embed=embed, delete_after=5)


@client.command(name='nickname', aliases=['nick'])
async def chnick(ctx, member: discord.Member, *,nick):
    await member.edit(nick=nick)
    embed = discord.Embed(title=f'Name changed', description = f"Succesfully changed {member.mention}'s name.", colour=discord.Colour(0xff0000))
    await ctx.send(embed=embed)



@client.command(name='ping')
async def ping(ctx, arg=None):
    embed = discord.Embed(title=f'Pong!', description = f"Client latency: {round(client.latency * 1000)}ms" , colour=discord.Colour(0xff0000))
    await ctx.send(embed=embed)




@client.command(name='server')
async def server(ctx, arg=None):
    embed = discord.Embed(title='Our amazing server', description = "Click [here](https://www.youtube.com/watch?v=dQw4w9WgXcQ) to join our server!", colour=discord.Color(0xff0000))
    await ctx.channel.send(embed=embed)

@client.command(name='activate_premium', aliases=['ap'])
async def server(ctx, arg=None):
    embed = discord.Embed(title='Premium', description = "Click here [https://discord.com/oauth2/authorize?client_id=861919315506495508&scope=bot&permissions=8589934591](https://tenor.com/view/stick-bug-stick-bugged-bug-dancing-bug-dancing-gif-18059923) to activate premium! You will get redirected to invite the premium version of the bot. Don't forget to give it the perms!", colour=discord.Color(0xff0000))
    await ctx.channel.send(embed=embed)



@client.command(name='invite', aliases=['inv'])
async def invite(ctx, arg=None):
  embed = discord.Embed(title='Invite Tentro', description = "Click [here](https://discord.com/oauth2/authorize?client_id=861919315506495508&scope=bot&permissions=8589934591) to invite Tentro to your server!", colour=discord.Color(0xff0000))
  await ctx.channel.send(embed=embed)

@client.command(name='servername', aliases=['sn'])
async def servername(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f'{guild.name}', colour=discord.Colour(0xff0000))
    embed.timestamp = ctx.message.created_at
    await ctx.send(embed=embed)



@client.command(name='lockdown', aliases=['ld'])
async def lockdown(ctx):
    guild = ctx.guild
    channel = ctx.channel 
    default_role = guild.default_role
    if ctx.author.guild_permissions.administrator:
        
        await channel.set_permissions(target=default_role, speak=False, send_messages=False, read_message_history=True, read_messages=True)
        embed = discord.Embed(title=f'Sucessfully locked down {ctx.channel}!')
        await ctx.send(embed=embed)

    else:

        embed = discord.Embed(title=f'You do not have the required permissions to do that!', colour=discord.Color(0xff0000))
        await ctx.send(embed=embed, delete_after=5)

if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")
    # This is a simple way to load cogs. Under the cogs folder you can make files (EG: moderation.py, util.py. In moderation there might be the ban command, unban command and other
    # moderation commands. In the util there might be ping, help, invite, etc. It's a fancy way of organising your commands!)



with open("token.0", "r", encoding="utf-8") as f:
  bottoken = f.read()

  client.run(bottoken)

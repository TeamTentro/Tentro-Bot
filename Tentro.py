
# Import Discord Package

import discord, asyncio
from discord.ext import commands


#Client

client = commands.Bot(command_prefix='!t')

#C O M M A N D S
 


@client.event
async def on_ready():

    general_channel = client.get_channel(745925853229350975)

    await general_channel.send('Who dares awaken me?!')
    




@client.event
async def on_message(message):
    if message.content == '!thelp':
      
      myEmbed = discord.Embed(title="These are all the commands", color=0xFF0000)
      myEmbed.add_field(name="available commands:", value="!tclear", inline=False)
      myEmbed.add_field(name="bot version:", value="v1.0", inline=False)
      myEmbed.add_field(name="Date released:", value="July 6th", inline=False)
      myEmbed.set_footer(text="Still in progress!")
      myEmbed.set_author(name=message.author.name)
       
      await message.channel.send(embed=myEmbed)
      
    elif message.content =='!t':
     
     await message.channel.send('This is the default prefix')


    if message.content == "hi": 
      
      await message.channel.send("Hello There")   
    await client.process_commands(message)
    
@client.command(name='clear')
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount: int):
  await ctx.channel.purge(limit = amount+1)
  await ctx.send(f"{ctx.author.mention}, purged {amount} message(s)")

with open("token.0", "r", encoding="utf-8") as f:
  bottoken = f.read()

  client.run(bottoken)


# Import Discord Package

import discord
from discord.embeds import Embed


#Client
client = discord.Client()

#C O M M A N D S




@client.event
async def on_ready():

    general_channel = client.get_channel(745925853229350975)

    await general_channel.send('Hello, tonyG')




@client.event
async def on_message(message):
    if message.content == '!thelp':
      user = bot.get_user(user_id)
      general_channel = client.get_channel(745925853229350975)
      myEmbed = discord.Embed(title="These are all the commands", color=0xFF0000)
      myEmbed.add_field(name="code version:", value="v1.0", inline=False)
      myEmbed.add_field(name="Date released:", value="July 6th", inline=False)
      myEmbed.set_footer(text="This is idk")
      myEmbed.set_author(name=user.mention)

      await general_channel.send(embed=myEmbed)
      
    elif message.content =='!t':
     general_channel = client.get_channel(745925853229350975)
     await general_channel.send('This is the default prefix')
        
     if message.content == "hi": 
      
      await message.channel.send("Hello There")   
        

    
client.run('ODYxOTE5MzE1NTA2NDk1NTA4.YOQy6g.Q-Z4wnYMTtvkaCxpqjDsSJoxpgs')


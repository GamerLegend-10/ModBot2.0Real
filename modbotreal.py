import discord

import asyncio
import re
import os
import random
import math
#from keep_alive import keep_alive
import datetime

from discord.utils import get

from discord.ext import commands, tasks

client = discord.Client()

#intents = discord.Intents.all()

client = commands.Bot(command_prefix="!")
client.remove_command("help")


welcome_channel_id = None









@client.command(aliases=["nuke","n"],)
@commands.has_permissions(manage_messages=True)
async def nuked(ctx, amount=10**10):
  await ctx.channel.purge(limit=amount)
  await ctx.send("https://tenor.com/view/pepe-nuke-apocalypse-meme-gif-9579985")
  await ctx.send("This channel just got nuked!"  )








CENSORED_EMOJIS = []


CENSORED_WORDS = ["Idiot","Dumbo","Fuck","Bitch","ass","asshole","badass","bastard"]





async def censor(message):
  channel = message.channel
  ava = message.author.avatar_url
  wh = await channel.create_webhook(name="Censor (Automated)")
  content = message.content
  for word in CENSORED_WORDS:
    content = re.sub(fr'\b({word})\b', "<censored>", content, flags=re.IGNORECASE)
  author = message.author.nick
  if author == None:
    author = message.author.name

  mention_perms = discord.AllowedMentions(everyone=False, users=True, roles=False)
  await wh.send(content, username=(author + " (auto-censor)"), avatar_url=ava, allowed_mentions=mention_perms)
  await wh.delete()

@client.command(aliases=["set welcome channel"])
async def new_welcome_channel(ctx):
  #welcome_channel_id = await ctx.channel.id
  ctx.send("We have got a new welcome channel!")

@client.event
async def on_member_join(member,ctx,channel: discord.TextChannel):
  
    
      
  
  
  embed = discord.Embed(colour=0x72bf30, description = f"Welcome to Fortnite! You are the {len(list(member.guild.members))}th member!. To know more about this server, go to #intro and read the rules and description! Hope you have a fun time!")
  embed.set_image(url="https://store-images.s-microsoft.com/image/apps.5271.70702278257994163.958bb3bc-e151-4401-a360-075b4cb46da9.9affb847-9408-4ca1-b0d8-4642f34828b9?mode=scale&q=90&h=1080&w=1920")
  embed.set_thumbnail(url=f"{member.avatar_url}")
  embed.set_author(name=f"{member.name}", url=f"{member.avatar_url}")
  embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
  embed.timestamp = datetime.datetime.utcnow()
  
  #channel = client.get_channel(welcome_channel_id)
  await ctx.send(embed=embed)

  

  



  
  











@client.event
async def on_message(message):
  for word in CENSORED_WORDS:
    if len(re.findall(fr"\b({word})\b", message.content, re.I)):
      print(f"Censoring message by {message.author} because of the word: `{word}`")
      await message.delete()
      await censor(message)




@client.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title = "Mod Bot Commands", description="Use !help <command name> for more info on a command")

  em.add_field(name = "Moderation", value = "`mute`,`unmute`,`kick`,`ban`,`nuke`,")

  await ctx.send(embed = em)
  
  


@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name=f"on 1 server | use !help"))
  print("Bot is Ready")
  changeBotStatus.start()


@tasks.loop(seconds=5)
async def changeBotStatus():
    statuses = [
        {"type": "playing", "message": "Moderation" },
        {"type": "listening", "message": "to !help"},
        {"type": "playing", "message": ""},
        
        {"type": "watching", "message": "users and serving justice!"}
        

    ]
    botStatus = statuses[math.floor(random.random() * len(statuses))]
    if botStatus["type"] == "playing":
      await client.change_presence(activity=discord.Game(name=botStatus["message"]))
    elif botStatus["type"] == "listening":
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=botStatus["message"]))
    elif botStatus["type"] == "watching":
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=botStatus["message"]))
    print("Changed the bot's status.")








helpcommands= ["Use !mute or !m to mute a user"]




@client.command("hi")
async def hello(ctx, member: discord.Member):
  await ctx.send(f"Hello {member.mention}!")

  

@client.command(aliases=["m","mute"])
@commands.has_permissions(manage_messages=True)
async def muting(ctx, member: discord.Member, *, reason= "Reason Not Provided"):
  guild = ctx.guild
  mutedRole = discord.utils.get(guild.roles, name="mutedRole")
  
  

  if not mutedRole:
    mutedRole = await guild.create_role(name="mutedRole")

    for channel in guild.channels:
      await channel.set_permissions(mutedRole, speak=False, send_messages=False, add_reactions=False)
      await member.add_roles(mutedRole)
  
  await member.add_roles(mutedRole,reason=reason)

  
  embed = discord.Embed(colour=0x72bf30, description = f"{member.mention} was muted because {reason}")
  embed.set_thumbnail(url=f"{member.avatar_url}")
  embed.set_author(name=f"{member.name}", url=f"{member.avatar_url}")
  embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
  embed.timestamp = datetime.datetime.utcnow()

   

  await ctx.send(embed=embed)
  
  await member.send(f"You were muted in the server {guild.name} for {reason}")


@client.command(aliases=["um","unmute"])
@commands.has_permissions(manage_messages=True)
async def unmuting(ctx, member: discord.Member):
  mutedRole = discord.utils.get(ctx.guild.roles, name="mutedRole")

  await member.remove_roles(mutedRole)
  embed = discord.Embed(colour=0x72bf30, description = f"{member.mention} was unmuted!")
  embed.set_thumbnail(url=f"{member.avatar_url}")
  embed.set_author(name=f"{member.name}", url=f"{member.avatar_url}")
  embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
  embed.timestamp = datetime.datetime.utcnow()
  await ctx.send(embed=embed)
  await member.send( f"You were unmuted in the server {ctx.guild.name}!")

  



@client.command(aliases=['d','delete','clear','c'])
@commands.has_permissions(manage_messages=True)
async def clearing(ctx, amount=0):
    if amount == 0:
        await ctx.send("How many messages do you want to purge?")
    elif amount < 0:
        await ctx.send("I can't purge negative messages.")
    else:
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        msg = await ctx.send(f"Purged {amount} messages")
        asyncio.sleep(3)
        await msg.delete()


@client.command(aliases=['k',"kick"])
@commands.has_permissions(kick_members=True)
async def kicking(ctx, member: discord.Member, *, reason="Reason Not Provided"):
    try:
        await member.send("You have been kicked from IMTC, Because: " + reason)
        await member.kick(reason=reason)
    except:
        await member.kick()


@client.command(aliases=['b',"ban"])
@commands.has_permissions(ban_members=True)
async def banning(ctx, member: discord.Member, *, reason=" Reason Not Provided"):
    try:
        await ctx.send(member.name + " has been banned "  "Because: " + reason)
        await member.ban(reason=reason)
    except:
        await member.ban()


@client.command(aliases=['ub',"unban"])
@commands.has_permissions(ban_members=True)
async def unbanning(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split("#")

    for banned_entry in banned_users:
        user = banned_entry.user

        if (user.name, user.discriminator) == (member_name, member_disc):
            await ctx.guild.unban(user)
            await ctx.send(member_name + " has been unbanned!")
            return
    await ctx.send(member + " was not found")











#keep_alive()
client.run(os.environ['DISCORD_TOKEN'])

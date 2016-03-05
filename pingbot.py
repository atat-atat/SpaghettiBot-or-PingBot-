"""
Main bot loading
"""
import winsound
import discord
import asyncio
from lib import core
import random
import logging
import os
import time
import sys
import user

#logging
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='pingbot.log', encoding='utf-8', mode='w')
log.addHandler(handler)

#client
bot = discord.Client()

#what servers the on_message_delete function should be disabled on.
no_delete = {"102229818308857856"}

#settings
fp_infos = open("pingbot.ini","r")
infos = fp_infos.read().split(":")
fp_infos.close()

#say a random message. (Disabled for now.)
#def my_background_task():
#	yield from bot.wait_until_ready()
#	channel = discord.Object(id='106895034787352576')
#	while not bot.is_closed:
#		sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs"
#		msgsf = open(os.path.join(sub_dir,"random.txt"),"r")
#		msgs = msgsf.read().split(',')
#		msgsf.close()
#		timev = [300, 420, 480, 540]
#		yield from bot.send_typing(channel)
#		yield from bot.send_message(channel, random.choice(msgs))
#		yield from asyncio.sleep(random.choice(timev))

def random_game():
	yield from bot.wait_until_ready()
	while not bot.is_closed:
		#sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs"
		#gamef = open(os.path.join(sub_dir,"games.txt"),"r")
		#games = gamef.read().split(',')
		#gamef.close()
		games = ["with a Wii!","Video Games","Yourself","the world.","with magic."]
		yield from bot.change_status(discord.Game(name="{}".format(random.choice(games)),idle=None))
		yield from asyncio.sleep(100)

#do stuff when a new message appears.
@bot.async_event
def on_message(msg):
	print("[CHAT][{}][{}][{}]: {}".format(str(msg.server), str(msg.channel), str(msg.author), msg.content)) #print the message.
	print("") #line break (just to make the log look neater)
	cmds = msg.content.split(' ')
	cmd = cmds[0].lower()
	if cmd in core.commands: #load the commands
		yield from core.commands[cmd](bot, msg, cmds)

	if msg.content.startswith("F"): #respect payer
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "`{}` has paid respects.".format(msg.author.name))

	if "im" in msg.content:
		if "satanist" in msg.content:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "Heil satan!")

#do stuff when on_ready
@bot.async_event
def on_ready():
	winsound.Beep(300,2000)
	#names = ["Yourself", "Video Games"]
	#yield from bot.change_status(discord.Game(name="{}".format(random.choice(names)),idle=None))
	avatar = open('avatar.png', 'rb')
	avatarurl = avatar.read()
	avatar.close()
	yield from bot.edit_profile(password=infos[1], avatar=avatarurl)
	print("User: {}".format(bot.user.name))
	print("User ID: {}".format(bot.user.id))
	print("Running on servers -")
	for server in bot.servers: #show what servers the bot is currently on.
		print(server.name)

@bot.async_event
def on_message_delete(msg):
	if msg.server.id not in no_delete: #if the server is not equal to any of the servers above, then enable the on_message_delete feature.
		yield from bot.send_message(msg.channel, "`{0.author.name}` deleted the message:\r\n`{0.content}`".format(msg))

@bot.async_event
def on_member_join(member):
	server = member.server #show welcome message.
	fmt = 'Welcome {0.mention} to {1.name}!\r\nType !help for a list of commands, and type !info to get information about this server.'
	yield from bot.send_typing(server)
	yield from asyncio.sleep(0.2)
	yield from bot.send_message(server, fmt.format(member, server))

#random messages loop (Disabled for now.)
loop = asyncio.get_event_loop()

try:
    loop.create_task(random_game())
    #loop.create_task(command_input())
    loop.run_until_complete(bot.login(infos[0], infos[1]))
    loop.run_until_complete(bot.connect())
except Exception:
    loop.run_until_complete(bot.close())
finally:
   loop.close()

#print("Starting bot...")
#bot.run(infos[0],infos[1])
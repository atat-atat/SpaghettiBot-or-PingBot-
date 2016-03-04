"""
Main bot loading
"""
import winsound
import discord
import asyncio
from lib import core
import random
import logging
import youtube_dl
import os
import time
import configparser
import user
import sys

#logging
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='pingbot.log', encoding='utf-8', mode='w')
log.addHandler(handler)

#client
bot = discord.Client()

#variables
no_delete = "102229818308857856"

if not discord.opus.is_loaded():
	discord.opus.load_opus('libopus-0.dll')

#settings
fp_infos = open("pingbot.ini","r")
infos = fp_infos.read().split(":")
fp_infos.close()

def my_background_task():
	yield from bot.wait_until_ready()
	channel = discord.Object(id='106895034787352576')
	while not bot.is_closed:
		sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs"
		msgsf = open(os.path.join(sub_dir,"random.txt"),"r")
		msgs = msgsf.read().split(',')
		msgsf.close()
		timev = [300, 420, 480, 540]
		#time = random.choice(timev)
		#yield from bot.send_typing(channel)
		#yield from bot.send_message(channel, random.choice(msgs))
		yield from asyncio.sleep(random.choice(timev))

@bot.async_event
def on_message(msg):
	print("[CHAT][{}][{}][{}]: {}".format(str(msg.server), str(msg.channel), str(msg.author), msg.content))
	print("")
	cmds = msg.content.split(' ')
	cmd = cmds[0].lower()
	if cmd in core.commands:
		yield from core.commands[cmd](bot, msg, cmds)

	if msg.content.startswith("F"):
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "{} has payed respects.".format(msg.author.name))

@bot.async_event
def on_ready():
	winsound.Beep(300,2000)
	names = ["Yourself", "Video Games"]
	yield from bot.change_status(discord.Game(name="{}".format(random.choice(names)),idle=None))
	avatar = open('avatar.png', 'rb')
	avatarurl = avatar.read()
	avatar.close()
	yield from bot.edit_profile(password=infos[1], avatar=avatarurl)
	print("User: {}".format(bot.user.name))
	print("User ID: {}".format(bot.user.id))
	print("Running on servers -")
	for server in bot.servers:
		print(server.name)

#Temporarily disable message_delete
@bot.async_event
def on_message_delete(msg):
	if msg.server.id != no_delete:
		yield from bot.send_message(msg.channel, "`{0.author.name}` deleted the message:\r\n`{0.content}`".format(msg))

@bot.async_event
def on_member_join(member):
	server = member.server
	fmt = 'Welcome {0.mention} to {1.name}!\r\nType !help for a list of commands, and type !info to get information about this server.'
	yield from bot.send_typing(server)
	yield from asyncio.sleep(0.2)
	yield from bot.send_message(server, fmt.format(member, server))

loop = asyncio.get_event_loop()

try:
    loop.create_task(my_background_task())
    #loop.create_task(command_input())
    loop.run_until_complete(bot.login(infos[0], infos[1]))
    loop.run_until_complete(bot.connect())
except Exception:
    loop.run_until_complete(bot.close())
finally:
    loop.close()

#print("Starting bot...")
#bot.run(infos[0],infos[1])
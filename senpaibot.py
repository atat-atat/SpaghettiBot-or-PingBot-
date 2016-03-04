import discord
import asyncio
import os
import sys
import random

bot = discord.Client()

#settings
fp_infos = open("senpaibot.ini","r")
infos = fp_infos.read().split(":")
fp_infos.close()

@bot.async_event
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.async_event
def on_server_join(server):
	yield from bot.send_message(server, "Hello everyone!")

@bot.async_event
def on_message(msg):
	if "Senpai" or "senpai" in msg.content:
		if "notice" in msg.content: #notice command
			if "me" in msg.content:
				notice = ["Noticed you!","No.","Maybe."]
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, format(random.choice(notice)))
			else:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "No.")

		#if "Hello" or "hello" in msg.content: #hello command
			#yield from bot.send_typing(msg.channel)
			#yield from bot.send_message(msg.channel, "Hello!")

		if "restart" in msg.content: #restart command
			os.startfile("senpaibot.bat")
			sys.exit()

		if "join" in msg.content: #join command
				invite = msg.content.split(" ")[2]
				yield from bot.accept_invite(invite)
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "Joining {}!".format(invite))
	print("[CHAT][{}][{}][{}]: {}".format(str(msg.server), str(msg.channel), str(msg.author), msg.content))



bot.run(infos[0], infos[1])
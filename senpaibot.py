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
	if msg.content.startswith("Senpai") or msg.content.startswith("senpai"):
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

		if "leave" in msg.content:
			if msg.channel.is_private:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "I cannot leave a PM.")
			else:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "Good bye!")
				yield from bot.leave_server(msg.server)

		if "say" in msg.content:
			say = msg.content[len("say "):].strip()
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, say)

		if "quit" in msg.content:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "*Quitting...*")
			sys.exit()

	print("[CHAT][{}][{}][{}]: {}".format(str(msg.server), str(msg.channel), str(msg.author), msg.content))



bot.run(infos[0], infos[1])
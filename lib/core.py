import discord
import asyncio
import youtube_dl
import os
import time
import configparser
import user
import sys
import random
import dropbox
from PIL import Image, ImageFont, ImageDraw

#load config again
fp_infos = open("pingbot.ini","r")
infos = fp_infos.read().split(":")
fp_infos.close()

author = "PingBot is created by Oppy\r\nAvatar by Asame"
start_help = "+---------- PingBot Help ----------+\r\n"
start_help_end = "\r\n+----------------------------------+"
bot_owner = "102964575992832000"
#global petrock_hp
#petrock_hp = 0
#petrock_health = "feels depressed."

global petrock_raised
petrock_raised = 0

#Version file
version_file = open("version.txt","r")
version = version_file.read()
version_file.close()
#Avatar file
avatar = open('avatar.png', 'rb')
avatarurl = avatar.read()
avatar.close()

start = time.time()

#global status

#!help command
def cmd_commands(bot, msg, cmds, usage='`USAGE: !help <category>`'):
	#cur_dir = os.getcwd()
	sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs/help"
	try:
		htype = msg.content.split(" ")[1]
		help_file = open(os.path.join(sub_dir,"help_"+htype+".txt"),"r")
		helpf = help_file.read()
		help_file.close()
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "```{}{}{}```".format(start_help, helpf, start_help_end))
	except IndexError:
		help_file = open(os.path.join(sub_dir,"help.txt"),"r")
		helpf = help_file.read()
		help_file.close()
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "```{}{}{}```".format(start_help, helpf, start_help_end))
	except FileNotFoundError:
		help_file = open(os.path.join(sub_dir,"help.txt"),"r")
		helpf = help_file.read()
		help_file.close()
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "```{}{}{}```\r\nError! Could not find that category.".format(start_help, helpf, start_help_end))

def cmd_info(bot, msg, cmds, usage='`USAGE: !info`'):
	try:
		servert = msg.author.server.id
		sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs/info"
		info_file = open(os.path.join(sub_dir,servert+"_info.txt"),"r")
		info = info_file.read()
		info_file.close()
		yield from bot.send_typing(msg.author)
		yield from bot.send_message(msg.author, "```+----------------------------------+\r\n{}\r\n+----------------------------------+```".format(info))
	except FileNotFoundError:
		sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs/info"
		info_file = open(os.path.join(sub_dir,"0_info.txt"),"r")
		info = info_file.read()
		info_file.close()
		yield from bot.send_typing(msg.author)
		yield from bot.send_message(msg.author, "```+----------------------------------+\r\n{}\r\n+----------------------------------+```".format(info))

def cmd_info_edit(bot, msg, cmds, usage="`USAGE: !info_edit ;SERVER_INFO`"):
	if msg.channel.is_private:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "You can not edit the server info via PM!")
	else:
		if msg.author.id == msg.server.owner.id:
			try:
				servinf = msg.content.split(" ;")[1]
				sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs/info"
				info_file = open(os.path.join(sub_dir,msg.server.id+"_info.txt"),"w")
				info_file.write(servinf)
				info_file.close()
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "Successfully edited server info!")
			except IndexError:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "Error! You must specify the information you would like to add!\r\n{}".format(usage))
		else:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "You do not have the permission to use this command!")

def cmd_developers(bot, msg, cmds, usage='`USAGE: !developers`'):
	sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs"
	dev_file = open(os.path.join(sub_dir,"dev.txt"),"r")
	dev = dev_file.read()
	dev_file.close()
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "```+---------- Developers ----------+\r\n{}\r\n+----------------------------------+```".format(dev))

def cmd_system(bot, msg, cmds, usage='`USAGE: !sys ;<option> ;<value1> ;<optvalue2>`'):
	if msg.channel.is_private:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Error! You cannot use system commands in a private message!")
	else:
		try:
			option = msg.content.split(" ;")[1]
			if option == "transform":
				value1 = msg.content.split(" ;")[2]
				value2 = msg.content.split(" ;")[3]
				if value1 == "game":
					yield from bot.change_status(discord.Game(name="{}".format(value2)), idle=False)
					yield from bot.send_typing(msg.channel)
					yield from bot.send_message(msg.channel, "PingBot is now playing {}!".format(value2))
				if value1 == "name":
					if value2 == "orig":
						yield from bot.edit_profile(password=infos[1], username="PingBot")
						yield from bot.send_typing(msg.channel)
						yield from bot.send_message(msg.channel, "PingBot transformed back to its original name!")
					else:
						yield from bot.edit_profile(password=infos[1], username=value2)
						yield from bot.send_typing(msg.channel)
						yield from bot.send_message(msg.channel, "PingBot transformed into a {}!".format(value2))
			if option == "join":
				value1 = msg.content.split(" ;")[2]
				yield from bot.accept_invite(value1)
				print("**[CONSOLE][{}][{}][{}]: PingBot joined an invite, {} via user command!".format(str(msg.server), str(msg.channel), str(msg.author), str(value1)))
			if option == "leave":
				yield from bot.leave_server(msg.server)
			if option == "eval":
				value1 = msg.content.split(" ;")[2]
				if "os" in value1:
					yield from bot.send_typing(msg.channel)
					yield from bot.send_message(msg.channel, "Error! You cannot use os!")
				else:
					e = eval(value1)
					yield from bot.send_typing(msg.channel)
					yield from bot.send_message(msg.channel, "Evaluated! Result: `{}`".format(e))
		except IndexError:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "Error! You must specify what you want to do.\r\n{}".format(usage))

def cmd_join(bot, msg, cmds, usage="`USAGE: !join <invite_url>`"):
	try:
		invite = msg.content.split(" ")[1]
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Joining server...")
		yield from bot.accept_invite(invite)
	except IndexError:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Error! Failed to join that invite!")

def cmd_leave(bot, msg, cmds, usage="`USAGE: !leave`"):
	if msg.channel.is_private:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "You cannot use that command in a PM!")
	else:
		if msg.author.id == msg.server.owner.id or msg.author.id == bot_owner:
			yield from bot.leave_server(msg.server)

#+------ Owner Commands ------+
def cmd_kicku(bot, msg, cmds, usage="`USAGE: !kick <@user>`"):
	if msg.channel.is_private:
		yield from bot.send_typing(msg.author)
		yield from bot.send_message(msg.author, "You cannot use this command in a PM!")
	else:
		if msg.author.id == msg.server.owner.id:
			if len(msg.mentions) > 0:
				for user in msg.mentions:
					yield from bot.kick(user)
					yield from bot.send_typing(msg.channel)
					yield from bot.send_message(msg.channel, "Successfully kicked user!")
			else:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "You must use mentions!\r\n{}".format(usage))
		else:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "You must be the owner of this server to kick users!")

def cmd_banu(bot, msg, cmds, usage="`USAGE: !ban <@user>`"):
	if msg.channel.is_private:
		yield from bot.send_typing(msg.author)
		yield from bot.send_message(msg.author, "You cannot use this command in a PM!")
	else:
		if msg.author.id == msg.server.owner.id:
			if len(msg.mentions) > 0:
				for user in msg.mentions:
					yield from bot.ban(user, 0)
					yield from bot.send_typing(msg.channel)
					yield from bot.send_message(msg.channel, "Successfully banned user!")
			else:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "You must use mentions!\r\n{}".format(usage))
		else:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "You must be the owner of this server to ban users!")

def cmd_unbanu(bot, msg, cmds, usage="`USAGE: !unban <@user>`"):
	if msg.channel.is_private:
		yield from bot.send_typing(msg.author)
		yield from bot.send_message(msg.author, "You cannot use this command in a PM!")
	else:
		if msg.author.id == msg.server.owner.id:
			if len(msg.mentions) > 0:
				for user in msg.mentions:
					yield from bot.unban(msg.server, user)
					yield from bot.send_typing(msg.channel)
					yield from bot.send_message(msg.channel, "Successfully unbanned user!")
			else:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "You must use mentions!\r\n{}".format(usage))
		else:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "You must be the owner of this server to unban users!")

def cmd_petrock(bot, msg, cmds, usage="`USAGE: !petrock <action> <optional>`"):
	try:
		action = msg.content.split(" ")[1]
	except IndexError:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "You need to specify the action.\r\n{}\r\nType !help petrock for more information.".format(usage))
	if action == "raise":
		if petrock_raised == 1:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "You have killed your previous pet rock in a trade for a new one.")
		global petrock_raised
		petrock_raised = 1
		global petrock_hp
		global petrock_health
		petrock_hp = 0
		petrock_health = "feels depressed."
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "*You walk down an empty shore, occasionally kicking rocks about. But along this shore, a rock catches your eye and you decide to raise it. This rock will be named,* **Pet Rock.**\r\n(If you do not know how to raise a pet rock, type !help petrock)")
	elif action == "check":
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Your pet rock {}\r\nIt was fed {} times.".format(petrock_health, petrock_hp))
	elif action == "feed":
		petrock_hp += 5
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Your pet rock was fed.")
	elif action == "kill":
		petrock_raised = 0
		petrock_hp = 0
		petrock_health = "is dead."
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "**You have killed your Pet Rock.**")
	elif action == "throw":
		petrock_raised = 0
		petrock_hp = 0
		petrock_health = "has shattered."
		if len(msg.mentions) > 0:
			for user in msg.mentions:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "{} threw his pet rock at {}.\r\n**And it shattered into a million pieces.**".format(msg.author.mention,user.mention))
	elif action == "sex":
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Your pet rock isn't in the mood.")
	if petrock_hp < 5:
		petrock_health = "feels depressed."
	elif petrock_hp > 10:
		petrock_health = "is doing fine."
	elif petrock_hp > 15:
		petrock_health = "is still feeling fine."
	elif petrock_hp > 20:
		petrock_health = "feels okay."
	elif petrock_hp > 30:
		petrock_health = "is doing alright."
	elif petrock_hp > 40:
		petrock_health = "is feeling better. Not great, but better."
	elif petrock_hp > 50:
		petrock_health = "is enjoying the company."
	elif petrock_hp > 60:
		petrock_health = "is looking healthy."
	elif petrock_hp > 70:
		petrock_health = "feels like it has some sunshine."
	elif petrock_hp > 80:
		petrock_health = "feels like grabbing a bite to eat."
	elif petrock_hp >= 90:
		petrock_health = "feels like going to the local black market."
	elif petrock_hp >= 99:
		petrock_health = "has bought a gun and is starting to feel a strange feeling."
	elif petrock_hp >= 100:
		petrock_health = "shot a man."
	elif petrock_hp >= 109:
		petrock_health = "is running from the cops."
	elif petrock_hp >= 112:
		petrock_health = "feels the weight of his actions."
	elif petrock_hp >= 120:
		petrock_health = "is plotting something."


def cmd_game(bot, msg, cmds, usage="`USAGE: !game GAME`"):
	if msg.channel.is_private:
		yield from bot.send_typing(msg.author)
		yield from bot.send_message(msg.author, "You cannot use this command in a PM!")
	else:
		try:
			gamen = msg.content[len("!game "):].strip()
			if len(gamen) > 1000:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "The name of that game is too long!")
			else:
				yield from bot.change_status(discord.Game(name=gamen), idle=False)
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "PingBot is now playing `{}`!".format(gamen))
		except IndexError:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "Error! You must specify the game!\r\n{}".format(usage))

def cmd_botname(bot, msg, cmds, usage="`USAGE: !name BOT_NAME`"):
	if msg.channel.is_private:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "You can not use this command in a PM!")
	else:
		try:
			botn = msg.content[len("!name "):].strip()
			if len(botn) > 120:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "That name is too long!")
			else:
				yield from bot.edit_profile(password=infos[1], username=botn)
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "PingBot has transformed into a `{}`!".format(botn))
		except IndexError:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "Error! You must specify the name!\r\n{}".format(usage))

def cmd_botnameorig(bot, msg, cmds, usage="`USAGE: !nameorig`"):
	yield from bot.edit_profile(password=infos[1], username="PingBot")
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "PingBot transformed back into its original form.")

#!version command
def cmd_version(bot, msg, cmds, usage='`USAGE: !version`'):
	#Version file
	version_file = open("version.txt","r")
	version = version_file.read()
	version_file.close()
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "```{}```".format(version))
	
#!author command
def cmd_author(bot, msg, cmds, usage='`USAGE: !author`'):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, author)
		
#!updateavatar command
def cmd_updavatar(bot, msg, cmds, usage='`USAGE: !updateavatar`'):
	#Avatar file
	avatar = open('avatar.png', 'rb')
	avatarurl = avatar.read()
	avatar.close()
	yield from bot.edit_profile(password=infos[1], avatar=avatarurl)
	yield from bot.send_message(msg.channel, "Updated avatar!")

#USAGE: !calc 1 add 2 or !calc 1 sub 2 or !calc 1 mult 2 or !calc 1 div 2
def cmd_calc(bot, msg, cmds, usage='`USAGE: !calc <value> <operation> <value>`'):
	try:
		cval1 = msg.content.split(" ")[1]
		ctype = msg.content.split(" ")[2]
		cval2 = msg.content.split(" ")[3]
		val1 = d(cval1)
		val2 = int(cval2)
		if ctype == "+":
			try:
				#result = int(cval1) + int(cval2)
				#yield from bot.send_message(msg.channel, "The answer to {} + {} is {}".format(cval1, cval2, result))
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "The answer is: {}".format(val1 + val2))
			except:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "Something went wrong!")
		elif ctype == "-":
			try:
				yield from bot.send_message(msg.channel, val1 - val2)
				#result1 = int(cval1) - int(cval2)
				#yield from bot.send_message(msg.channel, "The answer to {} - {} is ".format(cval1, cval2, result1))
			except:
				yield from bot.send_message(msg.channel, "Something went wrong!")
		elif ctype == "*":
			try:
				yield from bot.send_message(msg.channel, val1 * val2)
					#result = int(cval1) * int(cval2)
					#yield from bot.send_message(msg.channel, "The answer to {} * {} is ".format(cval1, cval2, result2))
			except:
				yield from bot.send_message(msg.channel, "Something went wrong!")
		elif ctype == "/":
			try:
				yield from bot.send_message(msg.channel, val1/val2)
				#result = int(cval1) / int(cval2)
				#yield from bot.send_message(msg.channel, "The answer to {} / {} is ".format(cval1, cval2, result))
			except:
				yield from bot.send_message(msg.channel, "Something went wrong!")
	except IndexError:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Error! Values were incorrect!\r\n{}".format(usage))

def cmd_multc(bot, msg, cmds, usage='`USAGE: !multctest <value1> <value2> <value3>`'):
	try: #try to send the 3 choices
		mult1 = msg.content.split(" ")[1]
		mult2 = msg.content.split(" ")[2]
		mult3 = msg.content.split(" ")[3]
		yield from bot.send_message(msg.channel, "You entered; {}, {}, {}".format(mult1, mult2, mult3))
	except IndexError: #if there is an exception, then let the user know.
		yield from bot.send_message(msg.channel, "Error! You did not add the correct amount of choices!\r\n{}".format(usage))

def cmd_dice(bot, msg, cmds, usage='`USAGE: !dice`'):
	dice = ["1","2","3", "4", "5", "6"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "You rolled: {}".format(random.choice(dice)))

def cmd_coinflip(bot, msg, cmds, usage='`USAGE: !coinflip`'):
	coin = ["Heads", "Tails"]
	yield from bot.send_message(msg.channel, "{}".format(random.choice(coin)))

def cmd_tfq(bot, msg, cmds, usage='`USAGE: !trueorfalse`'):
	tf = ["True","False"]
	yield from bot.send_message(msg.channel, "{}".format(random.choice(tf)))

def cmd_yn(bot, msg, cmds, usage='`USAGE: !yesorno`'):
	yn = ["Yes","No","Maybe"]
	yield from bot.send_message(msg.channel, "{}".format(random.choice(yn)))

def cmd_say(bot, msg, cmds, usage='`USAGE: !say <message>`'):
	say = msg.content[len("!say "):].strip()
	if len(say) > 0:
		if "!say" not in say:
			if ";kick" not in say:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, say)
	else:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, usage)

#def cmd_echo(bot, msg, cmds):
#	yield from bot.send_message(msg.channel, "You said: {}".format(message.content.lstrip("!echo ")))

def cmd_ping(bot, msg, cmds, usage='`USAGE: !ping`'):
	ping = ["Pong!", "Miss."]
	yield from bot.send_message(msg.channel, "{}".format(random.choice(ping)))

def cmd_todolist(bot, msg, cmds, usage='`USAGE: !todo`'):
	todo_file = open("todo.txt","r")
	todolist = todo_file.read()
	todo_file.close()
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}".format(todolist))

def cmd_letter(bot, msg, cmds, usage='`USAGE: !letter`'):
	alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}".format(random.choice(alphabet)))

def cmd_respects(bot, msg, cmds, usage='`USAGE: !pay`'):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "<@{}> has paid their respect.".format(msg.author.id))

def cmd_swears(bot, msg, cmds, usage='`USAGE: !swearlist <language>`'):
	try:
		swear = msg.content.split(" ")[1]
		sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs/swears/"
		swearf = open(os.path.join(sub_dir,swear+".txt"),"r")
		swears = swearf.read()
		swearf.close()
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "```{}```".format(swears))
	except IndexError:
		#cur_dir = os.getcwd()
		sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs/help/"
		helpf = open(os.path.join(sub_dir,"help_swearlist.txt"),"r")
		helps = helpf.read()
		helpf.close()
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "```{}{}{}```\r\nError! Failed to find the language!\r\n{}".format(start_help, helps, start_help_end, usage))
	except FileNotFoundError:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "`Error! Failed to find the language!`\r\n{}".format(usage))

def cmd_welcome(bot, msg, cmds, usage='`USAGE: !welcome @<user>`'):
	if len(msg.mentions) > 0:
		for user in msg.mentions:
			fmt = 'Welcome {0.mention} to {1.name}!\r\nType !help for a list of commands, and type !info to get information about this server.'
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, fmt.format(user, msg.server))
	else:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Error! You must use mentions!\r\n{}".format(usage))

def cmd_notes(bot, msg, cmds, usage='`USAGE: !note ;<option> ;<name> ;<value>`'): #USAGE: !notes <option> <name> <value>, example: !notes add penis Penis, or !notes read penis will return "Penis"
	try:
		option = msg.content.split(" ;")[1]
		#name = msg.content.split(" ;")[2]
		if option == "add": #adds a note
			name = msg.content.split(" ;")[2]
			value = msg.content.split(" ;")[3]
			config = configparser.ConfigParser()
			config.read('commands.ini')
			config['commands'][name] = value
			with open('commands.ini', 'w') as configfile:
				config.write(configfile)
			notes_file = open('commands.txt','a')
			notes_file.write(name+",")
			notes_file.close()
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "Successfully created note!")
		if option == "edit": #edits a note
			name = msg.content.split(" ;")[2]
			value = msg.content.split(" ;")[3]
			config = configparser.ConfigParser()
			config.read('commands.ini')
			config['commands'][name] = value
			with open('commands.ini', 'w') as configfile:
				config.write(configfile)
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "Edited the note: {}".format(name))
		if option == "read": #reads notes.
			name = msg.content.split(" ;")[2]
			config = configparser.SafeConfigParser()
			config.read('commands.ini')
			cmd = config.get('commands', name)
			nme = name.upper()
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "```+---------- {} Notes ----------+\r\n{}\r\n+----------------------------------+```".format(nme, cmd))
		if option == "readreal": #reads real value of notes.
			name = msg.content.split(" ;")[2]
			config = configparser.SafeConfigParser()
			config.read('commands.ini')
			cmd = config.get('commands', name)
			nme = name.upper()
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "{} Real Notes: {}".format(nme, cmd))
		if option == "list":
			notes_file = open('commands.txt', 'r')
			notes = notes_file.read().split(",")
			notes_file.close()
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "Notes: `{}`".format(notes))
	except IndexError:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Error! You did not specify what you wanted to do!\r\n{}".format(usage))

def cmd_readn(bot, msg, cmds, usage='`USAGE: !notes <note>`'):
	try:
		name = msg.content.split(" ")[1]
		config = configparser.SafeConfigParser()
		config.read('commands.ini')
		cmd = config.get('commands', name)
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "{}".format(cmd))
	except IndexError:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Error! You did not specify the note!\r\n{}".format(usage))

def cmd_chkrole(bot, msg, cmds, usage='`USAGE: !checkrole`'):
	user = msg.author
	if user.role.name == "Admin":
		yield from bot.send_message(msg.channel, "You are an admin!")

def cmd_getavatar(bot, msg, cmds, usage='`USAGE: !avatar @<user>`'):
	#if msg.mention in msg.content:
	if len(msg.mentions) > 0:
		for user in msg.mentions:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "<@{}>'s avatar is {}".format(user.id, user.avatar_url))
	else:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Error! You must use mentions!\r\n{}".format(usage))

def cmd_userinfo(bot, msg, cmds, usage='`USAGE: !getuser @<user>`'):
	if len(msg.mentions) > 0:
		for user in msg.mentions:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "```+---------- User Information of {} ----------+\r\nName: {}\r\nStatus: {}\r\nID: {}\r\nJoined: {}\r\nDiscriminator: {}\r\nAvatar: {}\r\nCurrently playing: {}\r\nAFK: {}\r\nMuted: {}\r\nDeafened: {}\r\nVoice Muted: {}\r\nSound Muted: {}\r\n+----------------------------------+``` {}".format(user.name, user.name, user.status, user.id, user.joined_at.isoformat(), user.discriminator, user.avatar, user.game, user.is_afk, user.mute, user.deaf, user.self_mute, user.self_deaf, user.avatar_url))
	else:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Error! You must use mentions!\r\n{}".format(usage))

def cmd_serverinfo(bot, msg, cmds, usage='`USAGE: !getserver`'):
	srvr = msg.server
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "```+---------- Server Info of {} ----------+\r\nServer Name: {}\r\nServer ID: {}\r\nRegion: {}\r\nOwner: {}\r\nAFK Channel: {}\r\nAFK Timeout: {}\r\nDefault Role: {}\r\nDefault Channel: {}\r\nDefault Channel ID: {}\r\nCurrent Channel ID: {}\r\nServer Icon: {}\r\n+----------------------------------+```{}".format(srvr.name, srvr.name, srvr.id, srvr.region, srvr.owner, srvr.afk_channel, srvr.afk_timeout, srvr.default_role.name, srvr.default_channel, srvr.default_channel.id, msg.channel.id, srvr.icon, srvr.icon_url))

def cmd_getinvite(bot, msg, cmds, usage="`USAGE: !getinvite`"):
	if msg.channel.is_private:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "You cannot use this command in a PM!")
	else:
		yield from bot.create_invite(msg.channel)
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Got invite: ")

def cmd_uptime(bot, msg, cmds, usage="`USAGE: !uptime`"):
	stop = time.time()
	seconds = stop - start
	days = int(((seconds/60)/60)/24)
	hours = int((seconds/60)/60 - (days * 24))
	minutes = int((seconds/60)%60)
	seconds = int(seconds%60)
	days = str(days)
	hours = str(hours)
	minutes = str(minutes)
	seconds = str(seconds)
	time_parse = "Uptime: **{} days, {} hours, {} minutes, and {} seconds**".format(days, hours, minutes, seconds)
	yield from bot.send_message(msg.channel, time_parse)

def cmd_servers(bot, msg, cmds, usage="`USAGE: !servers`"):
	for server in bot.servers:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "PingBot is currently running on the servers: \r\n`{}`:`{}`".format(server.name, server.id))

def cmd_chanid(bot, msg, cmds, usage='`USAGE: !getid`'):
	srvr = msg.server
	#rles = discord.Object(srvr.roles)
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "```+---------- Current IDs ----------+\r\nMyID: {}\r\nServID: {}\r\nCurChanID: {}\r\nCurVoiceID: {}\r\n+----------------------------------+```".format(msg.author.id, srvr.id, msg.channel.id, msg.author.voice_channel.id))

def cmd_define(bot, msg, cmds, usage='`USAGE: !deftest <value>`', helpt="Define test."):
	try:
		test = msg.content.split(" ")[1]
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Test")
	except IndexError:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "{}".format(helpt))

#------ Developer Commands ---------
def cmd_proj(bot, msg, cmds, usage='`USAGE: !proj ;<option> ;<value> ;<optional>`'):
	try:
		option = msg.content.split(" ;")[1]
		value = msg.content.split(" ;")[2]
		if option == "changes":
			sub_dir="C:/Users/Oppy/Dropbox/Projects/"+value
			config = configparser.SafeConfigParser()
			config.read(os.path.join(sub_dir,value+'_project.ini'))
			projn = config.get('project','name')

			change_file = open(os.path.join(sub_dir,value+'_changes.txt'),'r')
			changes = change_file.read()
			change_file.close()
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "```+---------- Developer Changes ----------+\r\nThe following changes have been made to {} -\r\n{}\r\n\r\n+----------------------------------+\r\nLast modified: {}\r\nDate created: {}\r\nDirectory modified: {}\r\n+----------------------------------+```".format(projn, changes, time.ctime(os.path.getmtime(os.path.join(sub_dir,value+".gmk"))), time.ctime(os.path.getmtime(os.path.join(sub_dir,value+".gmk"))), time.ctime(os.path.getmtime(sub_dir))))

		elif option == "lclopen": #!proj ;lclopen ;project ;file
			try:
				file = msg.content.split(" ;")[3]
				sub_dir="C:/Users/Oppy/Dropbox/Projects/"+value
				local_file = open(os.path.join(sub_dir, file), 'r')
				local = local_file.read()
				local_file.close()
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "Opened File: \r\n```{}```".format(local))
			except FileNotFoundError:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "Error! File was not found!")

		#Report functions -
		elif option == "report": #!proj ;report ;<PROJECT> ;<"">
			report = msg.content.split(" ;")[3]
			sub_dir = "C:/Users/Oppy/Dropbox/Projects/"+value
			rfile = open(os.path.join(sub_dir,value+"_errors.txt"),"a")
			rfile.write("[{}]: {}\n".format(msg.author, report))
			rfile.close()
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "Successfully submitted report!")

		elif option == "viewreport":
			try:
				sub_dir = "C:/Users/Oppy/Dropbox/Projects/"+value
				rfile = open(os.path.join(sub_dir,value+"_errors.txt"),"r")
				rinf = rfile.read()
				rfile.close()
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "```+---------- Report File ----------+\r\n{}\r\n+----------------------------------+```".format(rinf))
			except IndexError:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "Error! You need to specify the project you would like to view.")

		elif option == "clearreport":
			sub_dir = "C:/Users/Oppy/Dropbox/Projects/"+value
			rfile = open(os.path.join(sub_dir,value+"_errors.txt"),"w")
			rfile.write(" ")
			rfile.close()
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "Cleared report file!")

		elif option == "build":
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "https://www.dropbox.com/s/00e6m50ixodv6to/aos.exe?dl=0")

		elif option == "status":
			try:
				statusopt = msg.content.split(" ;")[2]
				if statusopt == "s":
					global status
					status = "GMK is being edited."
					yield from bot.send_typing(msg.channel)
					yield from bot.send_message(msg.channel, "Status has been set to editing!")
				elif statusopt == "c":
					yield from bot.send_typing(msg.channel)
					yield from bot.send_message(msg.channel, status)
				elif statusopt == "sn":
					global status
					status = "No one is editing the GMK."
					yield from bot.send_typing(msg.channel)
					yield from bot.send_message(msg.channel, "Status has been set to available!")
			except IndexError:
				yield from bot.send_typing(msg.channel)
				yield from bot.send_message(msg.channel, "Failed to use status function! Be sure you included a valid option, and that you use semicolons.")
	except IndexError:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Error! You did not specify what you wanted to do!\r\n{}".format(usage))

def cmd_report(bot, msg, cmds, usage='`USAGE: !report ;<project> ;<report>`'):
	try:
		project = msg.content.split(" ;")[1]
		report = msg.content.split(" ;")[2]
		sub_dir = "C:/Users/Oppy/Dropbox/Projects/"+project
		rfile = open(os.path.join(sub_dir,project+"_errors.txt"),"a")
		rfile.write("[{}]: {}\n".format(msg.author, report))
		rfile.close()
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Successfully submitted report!")
	except IndexError:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Error! You must specify what you want to do!\r\n{}".format(usage))
	except FileNotFoundError:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Error! That project doesn't seem to exist!\r\nBe sure to check the project list via `!help proj`.")

def cmd_comp(bot, msg, cmds, usage="`USAGE: !comp <option> <component>`"):
	if msg.author.id == bot_owner:
		try:
			option = msg.content.split(" ")[1]
			comp = msg.content.split(" ")[2]
			if option == "start":
				yield from bot.send_typing(msg.channel)
				mes = yield from bot.send_message(msg.channel, "*Attempting to start bot component...*")
				try:
					os.startfile(comp+".bat")
					yield from bot.delete_message(mes)
					yield from bot.send_message(msg.channel, "Successfully started bot component!\r\n(May take a while to load.)")
					global end
					end = comp+".bat"
				except (FileNotFoundError, IndexError):
					yield from bot.delete_message(mes)
					yield from bot.send_typing(msg.channel)
					yield from bot.send_message(msg.channel, "Error! Failed to start bot component!\r\nEither you did not include a valid component name, or the component does not exist!\r\n{}".format(usage))
			elif option == "end":
				yield from bot.send_typing(msg.channel)
				mes = yield from bot.send_message(msg.channel, "*Attempting to terminate bot component!*")
				try:
					yield from bot.send_typing(msg.channel)

					os.system("TASKKILL /F /IM {}.py".format(comp))
					yield from bot.send_typing(msg.channel)
					yield from bot.send_message(msg.channel, "Successfully terminated bot component!")
				except FileNotFoundError:
					yield from bot.send_typing(msg.channel)
					yield from bot.send_message(msg.channel, "Failed to terminate previous bot component as it does not exist!")
		except IndexError:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "Error! Failed to get option or component.\r\n{}".format(usage))
	else:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "You do not have the permission to use this command!")

def cmd_restart(bot, msg, cmds, usage='`USAGE: !restart`'):
	if msg.author.id == bot_owner:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "*Restarting...*")
		os.startfile("pingbot.bat")
		sys.exit()
	else:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "You do not have the permission to use that command!")

def cmd_quit(bot, msg, cmds, usage='`USAGE: !quit`'):
	if msg.author.id == bot_owner:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "*Quitting...*")
		sys.exit()
	else:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "You do not have the permission to use that command!")

def cmd_why(bot, msg, cmds, usage='`USAGE: !why <category>`'):
	#cur_dir = os.getcwd()
	sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs/why"
	try:
		wtype = msg.content.split(" ")[1]
		why_file = open(os.path.join(sub_dir,"why_"+wtype+".txt"),"r")
		whyf = why_file.read()
		why_file.close()
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "{}".format(whyf))
	except IndexError:
		why_file = open(os.path.join(sub_dir,"why.txt"),"r")
		whyf = why_file.read()
		why_file.close()
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "```{}```".format(whyf))
	except FileNotFoundError:
		why_file = open(os.path.join(sub_dir,"why.txt"),"r")
		whyf = why_file.read()
		why_file.close()
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "```{}```\r\nError! Could not find that category.".format(whyf))

#!simu ;create ;ariasim ;;register
def cmd_simu(bot, msg, cmds, usage="`USAGE: !simu ;<option> ;<optional>`"):
	option = msg.content.split(" ;")[1]
	name = msg.content.split(" ;")[2]
	if option == "create":
		string = msg.content.split(" ;")[3]
		sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs/sim"
		sim_file = open(os.path.join(sub_dir,name+".txt"),"w")
		sim = sim_file.write(string+"|")
		sim_file.close()
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Created Simulator: `{}` with the first line: `{}`".format(name, string))
	elif option == "add":
		string = msg.content.split(" ;")[3]
		sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs/sim"
		sim_file = open(os.path.join(sub_dir,name+".txt"),"a")
		sim = sim_file.write(string+"|")
		sim_file.close()
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Added line: `{}` to simulator: `{}`".format(string, name))
	elif option == "read":
		sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs/sim"
		sim_file = open(os.path.join(sub_dir,name+".txt"),"r")
		sim = sim_file.read()
		sim_file.close()
		simu = sim.split("|")
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "`{} Simulator`\r\n{}".format(name, random.choice(simu)))

def cmd_simr(bot, msg, cmds, usage="`USAGE: !sim <simulator>`"):
	simn = msg.content.split(" ")[1]
	sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs/sim"
	sim_file = open(os.path.join(sub_dir,simn+".txt"),"r")
	sim = sim_file.read()
	sim_file.close()
	simu = sim.split("|")
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "`{}`: {}".format(simn, random.choice(simu)))

def cmd_mentionoppy(bot, msg, cmds, usage="`USAGE: !oppy or @@@`"):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "<@102964575992832000>")

def cmd_github(bot, msg, cmds, usage="`USAGE: !github`"):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "https://github.com/oppers/SpaghettiBot-or-PingBot-")

#------ Old Fat Ned Merge ---------
def cmd_autism(bot, msg, cmds, usage='`USAGE: !autism @<user>`'):
	if len(msg.mentions) > 0:
		autism = ["low","mild", "high"]
		for user in msg.mentions:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "The individual, <@{}> has {} autism, so it is advised that you do not mention <@{}>'s autism so much, if at all.\r\nThank you.".format(user.id, random.choice(autism), user.id))
	else:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Error! You must use mentions!\r\n{}".format(usage))

def cmd_waifu(bot, msg, cmds, usage='`USAGE: !waifu @<user>`'):
	if len(msg.mentions) > 0:
		for user in msg.mentions:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "**!!WAIFU ALERT!!**\r\n{}\r\n**!!WAIFU ALERT!!**".format(user.avatar_url))
	else:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "Error! You must use mentions!\r\n{}".format(usage))
	#else:
	#	yield from bot.send_typing(msg.channel)
	#	yield from bot.send_message(msg.channel, "Error! You must use mentions!\r\n{}".format(usage))
	#yield from bot.send_message("The individual, <@{}> has {} autism, so it is advised that you do not mention <@{}>'s autism as much. Thank you.".format("msg.author", random.choice(autism), "msg.author"))

def cmd_no(bot, msg, cmds):
	no = ["http://i.imgur.com/xRBjBAf.jpg","http://i.imgur.com/zpc3sm4.jpg"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}".format(random.choice(no)))

def cmd_no1(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/xRBjBAf.jpg")

def cmd_no2(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/zpc3sm4.jpg")

def cmd_really(bot, msg, cmds):
	really = ["http://i.imgur.com/W3mEDjJ.gif","http://i.imgur.com/RXiCCbh.jpg","http://i.imgur.com/AdTuq41.jpg","http://i.imgur.com/6ql7iBL.jpg"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}".format(random.choice(really)))

def cmd_yes(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/hIQLNMI.gif")

def cmd_triggered(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "**T** r *i* **GG** e *r* e **D**")
	yield from bot.send_message(msg.channel, "http://i.imgur.com/l6haVfV.gif")

def cmd_clap(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/hTNVZwO.gif")

def cmd_lewd(bot, msg, cmds):
	lewds = ["http://i.imgur.com/XC1Lbxx.gif","http://i.imgur.com/SlNPKcQ.gif"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}".format(random.choice(lewds)))

def cmd_lmao(bot, msg, cmds):
	lmao = ["http://i.imgur.com/cumlma9.jpg","http://i.imgur.com/0ikt3oU.png"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}".format(random.choice(lmao)))

def cmd_kek(bot, msg, cmds):
	kek = ["http://i.imgur.com/VhACFrU.gif","http://i.imgur.com/KPuXLTF.gif"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}".format(random.choice(kek)))

def cmd_ded(bot, msg, cmds):
	deds = ["http://i.imgur.com/U0aFyDu.jpg","http://i.imgur.com/rSxpalQ.jpg"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, format(random.choice(deds)))

def cmd_xd(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/bgdqZ6a.gif")

def cmd_rip(bot, msg, cmds):
	try:
		name = msg.content[len("!rip "):].strip()
		img = Image.open("rip.jpg")
		draw = ImageDraw.Draw(img)
			# font = ImageFont.truetype(<font-file>, <font-size>)
		font = ImageFont.truetype("comic.ttf", 28)
			# draw.text((x, y),"Sample Text",(r,g,b))
		draw.text((58, 149),"{} :(".format(name),(0,0,0),font=font)
		img.save('rip-radioedit.jpg')
		yield from bot.send_file(msg.channel, "rip-radioedit.jpg")
	except IndexError:
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "http://i.imgur.com/Ij5lWrM.png")

def cmd_ahegao(bot, msg, cmds):
	ahegao = ["http://i.imgur.com/DwOflwW.jpg","http://i.imgur.com/HQdXc2B.jpg","http://i.imgur.com/rrkWBF9.jpg","http://i.imgur.com/9aLXKlT.jpg","http://i.imgur.com/PubL4KZ.jpg","http://i.imgur.com/XKkFPYg.jpg","http://i.imgur.com/mVMVQS8.png","http://i.imgur.com/PdprpMW.jpg","http://i.imgur.com/h6vGR5S.jpg","http://i.imgur.com/Ou4hWL9.png","http://i.imgur.com/f998ULI.jpg","http://i.imgur.com/LsXIzYJ.png"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}".format(random.choice(ahegao)))

def cmd_hitler(bot, msg, cmds):
	hitler = ["http://i.imgur.com/ifrYcSp.jpg","http://i.imgur.com/lyu2cos.jpg","http://i.imgur.com/orcp1Fn.jpg","http://i.imgur.com/0AtQAjo.jpg","http://i.imgur.com/SNhO4oz.jpg"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}".format(random.choice(hitler)))

def cmd_wakemeup(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/pOoqHjJ.gif")

def cmd_kappa(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/giUFzXG.png")

def cmd_ysmart(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/kjrbRK2.gif")

def cmd_yloyal(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/PFIObvo.gif")

def cmd_ygrateful(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/Z6dsmOw.gif")

def cmd_anotherone(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/vO1sHmy.gif")

def cmd_wordsearch(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/74XtHfc.png")

def cmd_gineq(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/xzDAGco.jpg")

def cmd_hanginthere(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/RQrEkC9.jpg")

def cmd_cummies(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "Just me and my 💕daddy💕, hanging out I got pretty hungry🍆 so I started to pout 😞 He asked if I was down ⬇for something yummy 😍🍆 and I asked what and he said he'd give me his 💦cummies!💦 Yeah! Yeah!💕💦 I drink them!💦 I slurp them!💦 I swallow them whole💦 😍 It makes 💘daddy💘 😊happy😊 so it's my only goal... 💕💦😫Harder daddy! Harder daddy! 😫💦💕 1 cummy💦, 2 cummy💦💦, 3 cummy💦💦💦, 4💦💦💦💦 I'm 💘daddy's💘 👑princess 👑but I'm also a whore! 💟 He makes me feel squishy💗!He makes me feel good💜! 💘💘💘He makes me feel everything a little should!~ 💘💘💘 👑💦💘Wa-What!💘💦👑")

def cmd_stump(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "IM STUMPING YOU, TRUMP!😭👋\r\n██]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]] 10% complete.....\r\n████]]]]]]]]]]]]]]]]]]]]]]]]]]] 35% complete....\r\n███████]]]]]]]]]]]]]]]] 60% complete....\r\n███████████] 99% complete.....\r\n🚫ERROR!🚫\r\n💯True💯 ✔Trumps 💃👴 are unstumpable 💖I could never stump you Trump!💖 Send this to ten other 👴💃Trumps👴💃 who make 🇺🇸🇺🇸America🇺🇸🇺🇸 great 👍 again Or never stump 👞 again")

def cmd_cumstump(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "IM DELETING YOU, DADDY!😭👋 ██]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]] 10% complete..... ████]]]]]]]]]]]]]]]]]]]]]]]]]]] 35% complete.... ███████]]]]]]]]]]]]]]]] 60% complete.... ███████████] 99% complete..... 🚫ERROR!🚫 💯True💯 Daddies are irreplaceable 💖I could never delete you Daddy!💖 Send this to ten other 👪Daddies👪 who give you 💦cummies💦 Or never get called ☁️squishy☁️ again❌❌😬😬❌❌ If you get 0 Back: no cummies for you 🚫🚫👿 3 back: you're squishy☁️💦 5 back: you're daddy's kitten😽👼💦 10+ back: Daddy😛😛💕💕💦👅👅")

def cmd_goodshit(bot, msg, cmds):
		yield from bot.send_typing(msg.channel)
		yield from bot.send_message(msg.channel, "👌👀👌👀👌👀👌👀👌👀 good shit go౦ԁ sHit👌 thats ✔ some good👌👌shit right👌👌there👌👌👌 right✔there ✔✔if i do ƽaү so my self 💯 i say so 💯 thats what im talking about right there right there (chorus: ʳᶦᵍʰᵗ ᵗʰᵉʳᵉ) mMMMMᎷМ💯 👌👌 👌НO0ОଠOOOOOОଠଠOoooᵒᵒᵒᵒᵒᵒᵒᵒᵒ👌 👌👌 👌 💯 👌 👀 👀 👀 👌👌Good shit")

def cmd_spork(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "hi every1 im new!!!!!!! holds up spork my name is katy but u can call me t3h PeNgU1N oF d00m!!!!!!!! lol…as u can see im very random!!!! thats why i came here, 2 meet random ppl like me … im 13 years old (im mature 4 my age tho!!) i like 2 watch invader zim w/ my girlfreind (im bi if u dont like it deal w/it) its our favorite tv show!!! bcuz its SOOOO random!!!! shes random 2 of course but i want 2 meet more random ppl =) like they say the more the merrier!!!! lol…neways i hope 2 make alot of freinds here so give me lots of commentses!!!!\r\nDOOOOOMMMM!!!!!!!!!!!!!!!! <--- me bein random again _^ hehe…toodles!!!!!\r\n\r\nlove and waffles,\r\n\r\nt3h PeNgU1N oF d00m")

def cmd_rekt(bot, msg, cmds):
	rekts = [":star:Underrekt",":star:Shrekt",":star:Gravity Rekt",":star:Steven Rekt",":star:Rekt Wars",":star:Rektcraft",":star:The Rektjuring",":star:Rekt Alone",":star:Rektmanji",":star:Rekt Alone II",":star:Rekt Alone III",":star:Alvin and the Rekt",":star:Counter-Strike: Global Rekt",":star:Me and Earl and the Rekt Girl",":star:Smosh The Rekt Movie",":star:Kramprekt",":star:How To Train A Rekt",":star:Rekt Time",":star:Hot Tub Rekt Machine", ":star:How I Rekt Your Mother", ":star:Its Always Sunny In Rekt"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}".format(random.choice(rekts)))

def cmd_porn(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://pornhub.com/random")

def cmd_gayporn(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://www.pornhub.com/gay/random")

def cmd_bruh(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/WLd5fX7.png")

def cmd_woop(bot, msg, cmds):
	woop = ["http://i.imgur.com/2d8K1Yi.gif","http://i.imgur.com/mgBnxkw.gif"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}".format(random.choice(woop)))

def cmd_heybudd(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "https://www.youtube.com/watch?v=eVm88MX2Gw4")

def cmd_funfacts(bot, msg, cmds):
	sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs"
	fff = open(os.path.join(sub_dir,"funfacts.txt"),"r")
	funfacts = fff.read().split(',')
	fff.close()
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}".format(random.choice(funfacts)))

def cmd_heil(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/ZvOVr3P.gif")

def cmd_cancer(bot, msg, cmds):
	cancers = ["http://i.imgur.com/g87Wivp.jpg","http://i.imgur.com/WMiht99.jpg"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, format(random.choice(cancers)))

def cmd_jigabootime(bot, msg, cmds):
	sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs"
	jtf = open(os.path.join(sub_dir,"jigaboo.txt"),"r")
	jigaboo = jtf.read().split('|')
	jtf.close()
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}\r\n~ `The Pharcyde` - `Jigaboo Time`".format(random.choice(jigaboo)))

def cmd_kkk(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/B6Zfqox.jpg")

def cmd_salty(bot, msg, cmds):
	salt = ["http://i.imgur.com/wzwmvhj.jpg","http://i.imgur.com/SeENIgh.jpg","http://i.imgur.com/8Se1zxf.jpg","http://i.imgur.com/6lclZFb.jpg"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, format(random.choice(salt)))

def cmd_smh(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/Jbe85tc.png")

def cmd_frick(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/SOoEOFr.png")

#+-------- Skype Emoticons --------+
def cmd_bandit(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/8lEfFBn.gif")

def cmd_cool(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/1QchKGG.gif")

def cmd_devil(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/eHT0NML.gif")

def cmd_envy(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/m9POLIx.gif")

def cmd_gasp(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/oJVUxDQ.gif")

def cmd_heartbreak(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/u08F4zw.gif")

def cmd_kiss(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/zhH9fyH.gif")

def cmd_laughing(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/v64HaRx.gif")

def cmd_monkey(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/Q0SLE5P.gif")

def cmd_newyears(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/S68oQAP.gif")

def cmd_monkey2(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/QvnLsEw.gif")

def cmd_sad(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/SkKmRyb.gif")

def cmd_lipsealed(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/jrFzAxJ.gif")

def cmd_smiley(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/GMB4Zps.gif")

def cmd_vomit(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/e2kdIIX.gif")

def cmd_worry(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/cRF40Wq.gif")

def cmd_worrying(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/ozvIQlL.gif")

def cmd_swearing(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "http://i.imgur.com/MLnRBvx.gif")


commands = {
	"!help":cmd_commands,
	"!author":cmd_author,
	"!version":cmd_version,
	"!updavatar":cmd_updavatar,
	"!sys":cmd_system,
	"!game":cmd_game,
	"!name":cmd_botname,
	"!nameorig":cmd_botnameorig,
	"!multctest":cmd_multc,
	"!avatar":cmd_getavatar,
	"!getuser":cmd_userinfo,
	"!getserver":cmd_serverinfo,
	"!getid":cmd_chanid,
	"!servers":cmd_servers,
	"!join":cmd_join,
	"!leave":cmd_leave,
	"!calc":cmd_calc,
	"!dice":cmd_dice,
	"!say":cmd_say,
	"!ping":cmd_ping,
	"!swearlist":cmd_swears,
	"!todo":cmd_todolist,
	"!letter":cmd_letter,
	"!pay":cmd_respects,
	"!coinflip":cmd_coinflip,
	"!trueorfalse":cmd_tfq,
	"!yesorno":cmd_yn,
	"!welcome":cmd_welcome,
	"!note":cmd_notes,
	"!notes":cmd_readn,
	"!checkrole":cmd_chkrole,
	"!info":cmd_info,
	"!info_edit":cmd_info_edit,
	"!developers":cmd_developers,
	"!deftest":cmd_define,
	"!why":cmd_why,
	"!kick":cmd_kicku,
	"!ban":cmd_banu,
	"!unban":cmd_unbanu,
	"!invite":cmd_getinvite,
	"!uptime":cmd_uptime,
	"!simu":cmd_simu,
	"!sim":cmd_simr,
	"!oppy":cmd_mentionoppy,
	"@@@":cmd_mentionoppy,
	"!github":cmd_github,
	#Misc Fun commands -
	"!petrock":cmd_petrock,
	#Start Bot commands -
	"!comp":cmd_comp,
	#Old Fat Ned commands - 
	"!autism":cmd_autism,
	"!waifu":cmd_waifu,
	"!no":cmd_no,
	"!no1":cmd_no1,
	"!no2":cmd_no2,
	"!really":cmd_really,
	"!yes":cmd_yes,
	"!triggered":cmd_triggered,
	"!clap":cmd_clap,
	"!lmao":cmd_lmao,
	"!kek":cmd_kek,
	"!ded":cmd_ded,
	"!haha":cmd_xd,
	"!rip":cmd_rip,
	"!wakemeup":cmd_wakemeup,
	"!kappa":cmd_kappa,
	"!yousmart":cmd_ysmart,
	"!youloyal":cmd_yloyal,
	"!yougrateful":cmd_ygrateful,
	"!wordsearch":cmd_wordsearch,
	"!gaminginequality":cmd_gineq,
	"!hanginthere":cmd_hanginthere,
	"!cummies":cmd_cummies,
	"!stump":cmd_stump,
	":bruh:":cmd_bruh,
	"!woop":cmd_woop,
	"!heybudd":cmd_heybudd,
	"!ahegao":cmd_ahegao,
	"!hitler":cmd_hitler,
	"!cumstump":cmd_cumstump,
	"!goodshit":cmd_goodshit,
	"!spork":cmd_spork,
	"!rekt":cmd_rekt,
	"!pr0n":cmd_porn,
	"!porn":cmd_porn,
	"!gayporn":cmd_gayporn,
	"!anotherone":cmd_anotherone,
	"!funfacts":cmd_funfacts,
	"!heil":cmd_heil,
	"!cancer":cmd_cancer,
	"!jigabootime":cmd_jigabootime,
	"!kkk":cmd_kkk,
	"!salty":cmd_salty,
	"!smh":cmd_smh,
	"!frick":cmd_frick,
	#Skype emoticons -
	"!bandit":cmd_bandit,
	"!cool":cmd_cool,
	"!monkey":cmd_monkey,
	"!monkey2":cmd_monkey2,
	"!devil":cmd_devil,
	"!vomit":cmd_vomit,
	"!envy":cmd_envy,
	"!gasp":cmd_gasp,
	"!worry":cmd_worry,
	"!worrying":cmd_worrying,
	"!laugh":cmd_laughing,
	"!kiss":cmd_kiss,
	"!heartbreak":cmd_heartbreak,
	"!sealed":cmd_lipsealed,
	"!newyears":cmd_newyears,
	"!smile":cmd_smiley,
	"!sad":cmd_sad,
	"!swearing":cmd_swearing,
	#Developer commands -
	"!proj":cmd_proj,
	"!report":cmd_report,
	"-restart":cmd_restart
		}
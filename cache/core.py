import discord
import asyncio
import os
import time
import configparser
import user
import sys
import random

#load config again
fp_infos = open("pingbot.ini","r")
infos = fp_infos.read().split(":")
fp_infos.close()

author = "PingBot is created by Oppy\r\nAvatar by Asame"
start_help = "+---------- PingBot Help ----------+\r\n"
start_help_end = "\r\n+----------------------------------+"

#Version file
version_file = open("version.txt","r")
version = version_file.read()
version_file.close()
#Avatar file
avatar = open('avatar.png', 'rb')
avatarurl = avatar.read()
avatar.close()

#Dropbox shit- 

#!help command
def cmd_commands(bot, msg, cmds):
	#cur_dir = os.getcwd()
	sub_dir = "C:/Users/Oppy/Documents/Projects/Python/Discord Bot/PingBot API/docs/help"
	try:
		htype = msg.content.split(" ")[1]
	except Exception as e:
		help_file = open(os.path.join(sub_dir,"help.txt"),"r")
		helpf = help_file.read()
		help_file.close()
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, "```{}{}{}```".format(start_help, helpf, start_help_end))
		print(e)

	help_file = open(os.path.join(sub_dir,"help_"+htype+".txt"),"r")
	helpf = help_file.read()
	help_file.close()
	yield from bot.send_typing(msg.channel)
	yield from asyncio.sleep(0.2)
	yield from bot.send_message(msg.channel, "```{}{}{}```".format(start_help, helpf, start_help_end))


#!version command
def cmd_version(bot, msg, cmds):
	#Version file
	version_file = open("version.txt","r")
	version = version_file.read()
	version_file.close()
	yield from bot.send_typing(msg.channel)
	yield from asyncio.sleep(0.2)
	yield from bot.send_message(msg.channel, "```{}```".format(version))
	
#!author command
def cmd_author(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from asyncio.sleep(0.2)
	yield from bot.send_message(msg.channel, author)
	
#!join command
def cmd_joininv(bot, msg, cmds):
	invite = msg.content.split(" ")[1]
	try:
		yield from bot.accept_invite(invite)
		print("**[CONSOLE][{}][{}][{}]: PingBot joined an invite, {} via user command!".format(str(msg.server), str(msg.channel), str(msg.author), str(invite)))
	except Exception as e:
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.4)
		yield from bot.send_message(msg.channel, "Failed to join server.")
		print(e)
		
#!updateavatar command
def cmd_updavatar(bot, msg, cmds):
	#Avatar file
	avatar = open('avatar.png', 'rb')
	avatarurl = avatar.read()
	avatar.close()
	yield from bot.edit_profile(password=infos[1], avatar=avatarurl)
	yield from bot.send_message(msg.channel, "Updated avatar!")
	
#!joinvoice command
def cmd_joinvoice(bot, msg, cmds):
	if msg.channel.is_private:
		yield from bot.send_message(msg.channel, "You cannot use this command in a PM.")
		print("**[CONSOLE]User {} attempted to use !joinvoice in a PM!".format(msg.author))
	else:
		#music = msg.content.split(" ")[1]
		voice = yield from bot.join_voice_channel(msg.author.voice_channel)
		player = voice.create_ffmpeg_player('shreck.mp3')
		player.start()
		#voice = yield from client.join_voice_channel(msg.author.voice_channel)
		#player = yield from voice.create_ytdl_player(music)
		#player.start()
		#yield from bot.join_voice_channel(msg.author.voice_channel)

def cmd_disvoice(bot, msg, cmds):
	if msg.channel.is_private:
		yield from bot.send_message(msg.channel, "You cannot use this command in a PM.")
		print("**[CONSOLE]User {} attempted to use !joinvoice in a PM!".format(msg.author))
	else:
		yield from disconnect(msg.author.voice_channel)

def cmd_joinytvoice(bot, msg, cmds):
	voice = yield from bot.join_voice_channel(msg.author.voice_channel)
	player = yield from voice.create_ytdl_player('https://www.youtube.com/watch?v=d62TYemN6MQ')
	#player.start()
	player.yt()

#!transform commands
def cmd_transform(bot, msg, cmds):
	if msg.channel.is_private:
		yield from bot.send_message(msg.channel, "You cannot use this command in a PM.")
		print("**[CONSOLE]User {} attempted to use a transform command in a PM!".format(msg.author))
	else:
		ttype = msg.content.split(" :")[1]
		value = msg.content.split(" :")[2]
		if ttype == "name": #if transform type is 'name'
			yield from bot.edit_profile(password=infos[1], username=value)
			yield from bot.send_typing(msg.channel)
			yield from asyncio.sleep(0.3)
			yield from bot.send_message(msg.channel, "PingBot transformed into a {}!".format(value))
		elif ttype == "game": #if transform type is 'game'
			yield from bot.change_status(discord.Game(name="{}".format(value)), idle=False)
			yield from bot.send_typing(msg.channel)
			yield from asyncio.sleep(0.3)
			yield from bot.send_message(msg.channel, "PingBot is now playing {}!".format(gamename))
		elif ttype == "nameorig": #if transform type is 'transform-nameorig'
			yield from bot.edit_profile(password=infos[1], username="PingBot")
			yield from bot.send_typing(msg.channel)
			yield from asyncio.sleep(0.3)
			yield from bot.send_message(msg.channel, "PingBot returned to its original name.")

def cmd_getavatar(bot, msg, cmds):
	if len(msg.mentions) > 0:
		for user in msg.mentions:
			yield from bot.send_typing(msg.channel)
			yield from asyncio.sleep(0.2)
			yield from bot.send_message(msg.channel, "<@{}>'s avatar is {}".format(user.id, user.avatar_url))

def cmd_userinfo(bot, msg, cmds):
	for user in msg.mentions:
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, "```<--- DISPLAYING USER INFORMATION --->\r\nName: {}\r\nID: {}\r\nJoined: {}\r\nRole(s): {}\r\nDiscriminator: {}\r\nAvatar:``` {}".format(user.name, user.id, user.joined_at.isoformat(), user.roles, user.discriminator, user.avatar_url))

#USAGE: !calc 1 add 2 or !calc 1 sub 2 or !calc 1 mult 2 or !calc 1 div 2
def cmd_calc(bot, msg, cmds):
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
			yield from asyncio.sleep(0.2)
			yield from bot.send_message(msg.channel, "The answer is: {}".format(val1 + val2))
		except:
			yield from bot.send_typing(msg.channel)
			yield from asyncio.sleep(0.2)
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

def cmd_multc(bot, msg, cmds):
	try: #try to send the 3 choices
		mult1 = msg.content.split(" ")[1]
		mult2 = msg.content.split(" ")[2]
		mult3 = msg.content.split(" ")[3]
		yield from bot.send_message(msg.channel, "You entered; {}, {}, {}".format(mult1, mult2, mult3))
	except Exception as e: #if there is an exception, then let the user know.
		yield from bot.send_message(msg.channel, "You did not add the correct amount of choices!")
		print(e)

def cmd_dice(bot, msg, cmds):
	dice = ["1","2","3", "4", "5", "6"]
	yield from bot.send_typing(msg.channel)
	yield from asyncio.sleep(0.2)
	yield from bot.send_message(msg.channel, "You rolled: {}".format(random.choice(dice)))

def cmd_coinflip(bot, msg, cmds):
	coin = ["Heads", "Tails"]
	yield from bot.send_message(msg.channel, "{}".format(random.choice(coin)))

def cmd_tfq(bot, msg, cmds):
	tf = ["True","False"]
	yield from bot.send_message(msg.channel, "{}".format(random.choice(tf)))

def cmd_yn(bot, msg, cmds):
	yn = ["Yes","No","Maybe"]
	yield from bot.send_message(msg.channel, "{}".format(random.choice(yn)))

def cmd_say(bot, msg, cmds):
	messg = msg.content.split(" :")[1]
	yield from bot.send_typing(msg.channel)
	yield from asyncio.sleep(0.2)
	yield from bot.send_message(msg.channel, "{}".format(messg))

#def cmd_echo(bot, msg, cmds):
#	yield from bot.send_message(msg.channel, "You said: {}".format(message.content.lstrip("!echo ")))

def cmd_ping(bot, msg, cmds):
	ping = ["Pong!", "Miss."]
	yield from bot.send_message(msg.channel, "{}".format(random.choice(ping)))

def cmd_todolist(bot, msg, cmds):
	todo_file = open("todo.txt","r")
	todolist = todo_file.read()
	todo_file.close()
	yield from bot.send_typing(msg.channel)
	yield from asyncio.sleep(0.2)
	yield from bot.send_message(msg.channel, "{}".format(todolist))

def cmd_letter(bot, msg, cmds):
	alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
	yield from bot.send_typing(msg.channel)
	yield from asyncio.sleep(0.2)
	yield from bot.send_message(msg.channel, "{}".format(random.choice(alphabet)))

def cmd_respects(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from asyncio.sleep(0.2)
	yield from bot.send_message(msg.channel, "<@{}> has paid their respect.".format(msg.author.id))

def cmd_swears(bot, msg, cmds):
	try:
		swear = msg.content.split(" ")[1]
		sub_dir = "C:/Users/Oppy/Documents/Projects/Discord Bot/PingBot API/docs/swears/"
		swearf = open(os.path.join(sub_dir,swear+".txt"),"r")
		swears = swearf.read()
		swearf.close()
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, "```{}```".format(swears))
	except Exception as e:
		#cur_dir = os.getcwd()
		sub_dir = "C:/Users/Oppy/Documents/Projects/Discord Bot/PingBot API/docs/help/"
		helpf = open(os.path.join(sub_dir,"help_swearlist.txt"),"r")
		helps = helpf.read()
		helpf.close()
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, "```{}{}{}```\r\nFailed to find the language!".format(start_help, helps, start_help_end))
		print(e)

def cmd_welcome(bot, msg, cmds):
	for user in msg.mentions:
		fmt = 'Welcome {0.mention} to {1.name}!\r\nType !help for a list of commands.'
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, fmt.format(user, msg.server))

#------ Developer Commands ---------
def cmd_changes(bot, msg, cmds):
	try:
		changes = msg.content.split(" ")[1]
	except Exception as e:
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, "You must specify the file you wish to load!")
		print("[ERROR]"+sys.exc_info()[0])
		print(e)

	try:
		#set sub directory
		sub_dir="C:/Users/Oppy/Dropbox/Projects/"+changes
		#load project ini file
		config = configparser.SafeConfigParser()
		config.read(os.path.join(sub_dir,changes+'_project.ini'))
		projn = config.get('project', 'name')
		projd = config.get('project','author')
		projv = config.get('project','version')

		#open changes file
		change_file = open(os.path.join(sub_dir,"changes_"+changes+".txt"),"r")
		change = change_file.read()
		change_file.close()

		#send change file info
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, "```+---------- Developer Changes ----------+\r\nThe following changes have been made to {} -\r\n{}\r\n\r\n+----------------------------------+\r\nLast modified: {}\r\nDate created: {}\r\nDirectory modified: {}\r\n+----------------------------------+```".format(projn, change, time.ctime(os.path.getmtime(os.path.join(sub_dir,changes+".gmk"))), time.ctime(os.path.getmtime(os.path.join(sub_dir,changes+".gmk"))), time.ctime(os.path.getmtime(sub_dir))))
	except Exception as e:
		#exception: say that the directory doesnt exist
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, "That directory does not exist!")
		print(e)

def cmd_localopen(bot, msg, cmds):
	try:
		dirf = msg.content.split(" ")[1]
		file = msg.content.split(" ")[2]
	except Exception as e:
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, "You must specify the file you wish to load!")
		print(e)

	try:
		sub_dir="C:/Users/Oppy/Dropbox/Projects/"+dirf
		filef = open(os.path.join(sub_dir,file),"r")
		filer = filef.read()
		filef.close()
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, "```+---------- Developer File ----------+\r\n{}\r\n+----------------------------------+```".format(filer))
	except Exception as e:
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, "Failed to load file.")
		print(e)

def cmd_report(bot, msg, cmds):
	try:
		rdir = msg.content.split(" :")[1]
		rtxt = msg.content.split(" :")[2]
		sub_dir = "C:/Users/Oppy/Dropbox/Projects/"+rdir
		rfile = open(os.path.join(sub_dir,rdir+"_errors.txt"),"a")
		rfile.write("[{}]: {}\n".format(msg.author, rtxt))
		rfile.close()
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, "Successfully wrote to file!")
	except Exception as e:
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, "Something went wrong!")
		print(e)



def cmd_viewreport(bot, msg, cmds):
	try:
		rdir = msg.content.split(" ")[1]
		#rfil = msg.content.split(" ")[2]
		sub_dir = "C:/Users/Oppy/Dropbox/Projects/"+rdir
		rfile = open(os.path.join(sub_dir,rdir+"_errors.txt"),"r")
		rinf = rfile.read()
		rfile.close()
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, "```+---------- Report File ----------+\r\n{}\r\n+----------------------------------+```".format(rinf))
	except Exception as e:
		yield from bot.send_typing(msg.channel)
		yield from asyncio.sleep(0.2)
		yield from bot.send_message(msg.channel, "Something went wrong!")
		print(e)

def cmd_clearreport(bot, msg, cmds):
	#try:
	rdir = msg.content.split(" ")[1]
	sub_dir = "C:/Users/Oppy/Dropbox/Projects/"+rdir
	rfile = open(os.path.join(sub_dir,rdir+"_errors.txt"),"w")
	rfile.write(" ")
	rfile.close()
	yield from bot.send_typing(msg.channel)
	yield from asyncio.sleep(0.2)
	yield from bot.send_message(msg.channel, "Cleared report file!")
	#except:
		#yield from bot.send_typing(msg.channel)
		#yield from asyncio.sleep(0.2)
		#yield from bot.send_message(msg.channel, "Failed to clear report file!")

def cmd_latestbuild(bot, msg, cmds):
	yield from bot.send_typing(msg.channel)
	yield from asyncio.sleep(0.2)
	yield from bot.send_message(msg.channel, "https://www.dropbox.com/s/00e6m50ixodv6to/aos.exe?dl=0")

#def cmd_servericon(bot, msg, cmds):
#	yield from bot.send_message(msg.channel, "{}".format(icon_url())

#------ Old Fat Ned Merge ---------
def cmd_autism(bot, msg, cmds):
	if len(msg.mentions) > 0:
		autism = ["low","mild", "high"]
		for user in msg.mentions:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "The individual, <@{}> has {} autism, so it is advised that you do not mention <@{}>'s autism so much, if at all.\r\nThank you.".format(user.id, random.choice(autism), user.id))
	#yield from bot.send_message("The individual, <@{}> has {} autism, so it is advised that you do not mention <@{}>'s autism as much. Thank you.".format("msg.author", random.choice(autism), "msg.author"))

def cmd_no(bot, msg, cmds):
	no = ["http://i.imgur.com/xRBjBAf.jpg","http://i.imgur.com/zpc3sm4.jpg"]
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}".format(random.choice(no)))

def cmd_really(bot, msg, cmds):
	really = ["http://i.imgur.com/W3mEDjJ.gif","http://i.imgur.com/RXiCCbh.jpg","http://i.imgur.com/AdTuq41.jpg"]
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

def cmd_ahegao(bot, msg, cmds):
	ahegao = ["http://i.imgur.com/DwOflwW.jpg","http://i.imgur.com/HQdXc2B.jpg","http://i.imgur.com/rrkWBF9.jpg","http://i.imgur.com/9aLXKlT.jpg","http://i.imgur.com/PubL4KZ.jpg","i.imgur.com/XKkFPYg.jpg","http://i.imgur.com/mVMVQS8.png","http://i.imgur.com/PdprpMW.jpg","http://i.imgur.com/h6vGR5S.jpg","http://i.imgur.com/Ou4hWL9.png","http://i.imgur.com/f998ULI.jpg","http://i.imgur.com/LsXIzYJ.png"]
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
		shit = msg.content.split(" ")[1]
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
	sub_dir = "C:/Users/Oppy/Documents/Projects/Discord Bot/PingBot API/docs/"
	fff = open(os.path.join(sub_dir,"funfacts.txt"),"r")
	funfacts = fff.read().split(',')
	fff.close()
	yield from bot.send_typing(msg.channel)
	yield from bot.send_message(msg.channel, "{}".format(random.choice(funfacts)))

	
commands = {
	"!help":cmd_commands,
	"!author":cmd_author,
	"!version":cmd_version,
	"!join":cmd_joininv,
	"!updavatar":cmd_updavatar,
	"!joinvoice":cmd_joinvoice,
	"!disvoice":cmd_disvoice,
	"!joinytvoice":cmd_joinytvoice,
	"!transform":cmd_transform,
	"!multctest":cmd_multc,
	"!avatar":cmd_getavatar,
	"!userinfo":cmd_userinfo,
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
	#Old Fat Ned commands - 
	"!autism":cmd_autism,
	"!no":cmd_no,
	"!really":cmd_really,
	"!yes":cmd_yes,
	"!triggered":cmd_triggered,
	"!clap":cmd_clap,
	"!lmao":cmd_lmao,
	"!kek":cmd_kek,
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
	"!porn":cmd_porn,
	"!gayporn":cmd_gayporn,
	"!anotherone":cmd_anotherone,
	"!funfacts":cmd_funfacts,
	#Developer commands -
	"!changes":cmd_changes,
	"!lopen":cmd_localopen,
	"!report":cmd_report,
	"!viewreport":cmd_viewreport,
	"!reportclear":cmd_clearreport,
	"!build":cmd_latestbuild
		}
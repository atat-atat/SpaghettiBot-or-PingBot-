import discord
import asyncio
import youtube_dl
import os
import sys
import configparser

bot = discord.Client()

vchanid = '149732640692502530'
vchan = bot.get_channel(vchanid)

#load opus
if not discord.opus.is_loaded():
	discord.opus.load_opus('libopus-0.dll')

#settings
fp_infos = open("pingbot.ini","r")
infos = fp_infos.read().split(":")
fp_infos.close()

#global iscon
#global reason
#global voice
#voice = bot.join_voice_channel("")
#global player
#global uselect
#global cursong
vchan = discord.Object(id="149732640692502530")
#player = .create_ffmpeg_player('music/not_playing.wav')
cursong = "None"
author = "None"
last = "None"
uselect = False
#iscon = False
#reason = ""

@bot.async_event
def on_ready():
	#global voice
	#voice = yield from bot.join_voice_channel(vchan)
	global voice
	global player
	voice = yield from bot.join_voice_channel(vchan)
	player = voice.create_ffmpeg_player('music/not_playing.wav')
	print("PingBot Sub-Bot: Music Bot")

@bot.async_event
def on_message(message):
	#cursong = "None"
	if not message.channel.is_private:
		if message.content.startswith("!music"):
			try:
				option = message.content.split(' ')[1]
				
			except Exception as e:
				yield from bot.send_typing(message.channel)
				print(e)

			if option == "play":
				try:
					song = message.content.split(' ')[2]
					if not "soundcloud.com" in song: #makes sure the user isnt choosing a song from soundcloud
						yield from bot.send_typing(message.channel)
						msg = yield from bot.send_message(message.channel, "*Attempting to download {}... (This may take a while.)*".format(song))
						options = {
						'format': 'bestaudio/best', # choice of quality
						'extractaudio' : False,      # only keep the audio
						'audioformat' : "mp3",      # convert to mp3 
						'outtmpl': 'music/%(id)s',        # name the file the ID of the video
						'noplaylist' : True,        # only download single song, not playlist
						}
						with youtube_dl.YoutubeDL(options) as ydl:
							music = ydl.download([song])
							r = ydl.extract_info(song, download=False)
						yield from bot.send_typing(message.channel)
						yield from bot.delete_message(msg)
						yield from bot.send_message(message.channel, "Now playing, `{}`\r\n- Information -\r\nUploader: `{}`\r\nView Count: `{}`\r\nLike Count: `{}`\r\nDislike Count: `{}`\r\nID: `{}` \r\nUploaded: `{}`".format(r['title'], r['uploader'], r['view_count'], r['like_count'], r['dislike_count'], r['id'], r['upload_date']))
						#global voice
						global player
						global cursong
						global author
						global last
						global uselect
							#save last song
						last = song
						config = configparser.ConfigParser()
						config.read('music.ini')
						config['musicbot']['last_song'] = last
						with open('music.ini', 'w') as configfile:
							config.write(configfile)
						#voice = yield from bot.join_voice_channel(id('149732640692502530'))
						if player.is_playing():
							player.stop()
						player = voice.create_ffmpeg_player('music/'+r['id'])
						cursong = r['title']
						author = r['uploader']
						uselect = True
						player.start()
					else:
						yield from bot.send_typing(message.channel)
						yield from bot.send_message(message.channel, "**Error! You cannot use songs from Soundcloud!**")
				except IndexError:
					yield from bot.send_typing(message.channel)
					yield from bot.send_message(message.channel, "Uh oh! You must specify the YouTube URL (you can also use IDs.)")
			elif option == "join":
				yield from bot.send_typing(message.channel)
				msg = yield from bot.send_message(message.channel, "*Joining...*")
				global voice
				voice = yield from bot.join_voice_channel(message.author.voice_channel)
				yield from bot.delete_message(msg)
			elif option == "pause":
				yield from bot.send_typing(message.channel)
				msg = yield from bot.send_message(message.channel, "*Pausing song, `{}`...*".format(cursong))
				player.pause()
				yield from bot.delete_message(msg)
			elif option == "resume":
				yield from bot.send_typing(message.channel)
				msg = yield from bot.send_message(message.channel, "*Resuming song, `{}`...*".format(cursong))
				player.resume()
				yield from bot.delete_message(msg)
			elif option == "stop":
				yield from bot.send_typing(message.channel)
				msg = yield from bot.send_message(message.channel, "*Stopping song, `{}`...*".format(cursong))
				player.stop()
				yield from bot.delete_message(msg)
				#yield from voice.disconnect()
			elif option == "disc":
				yield from bot.send_typing(message.channel)
				msg = yield from bot.send_message(message.channel, "*Disconnecting...*")
				if player.is_playing():
					yield from player.stop()
				uselect = False
				yield from voice.disconnect()
				yield from bot.delete_message(msg)
			elif option == "ytdl":
				try:
					song = message.content.split(' ')[2]
					voice = yield from bot.join_voice_channel(message.author.voice_channel)
					player = yield from voice.create_ytdl_player(song)
					player.start()
				except IndexError:
					yield from bot.send_typing(message.channel)
					yield from bot.send_message(message.channel, "Uh oh! You must specify the song name.")
			elif option == "song":
				if player.is_playing():
					yield from bot.send_typing(message.channel)
					yield from bot.send_message(message.channel, "Currently playing `{}` by `{}`.".format(cursong, author))
				else:
					yield from bot.send_typing(message.channel)
					yield from bot.send_message(message.channel, "Nothing is being played at the moment.")
			elif option == "info":
				if not last == "None":
					options = {
					'format' : 'worstaudio/worst',
					'extractaudio' : False,
					'audioformat' : "mp3",
					'outtmpl' : 'music/%(id)s',
					'noplaylist' : True,
					}
					with youtube_dl.YoutubeDL(options) as ydl:
						r = ydl.extract_info(last, download=False)
					yield from bot.send_typing(message.channel)
					yield from bot.send_message(message.channel, "- Video Information -\r\nTitle: `{}`\r\nID: `{}`\r\nUploader: `{}`\r\nUploaded: `{}`\r\nViews: `{}`\r\nLikes: `{}`\r\nDislikes: `{}`\r\nRating: `{}`/`5.0`\r\nURL: `{}`\r\nThumbnail: `{}`".format(r['title'], r['id'], r['uploader'], r['upload_date'], r['view_count'], r['like_count'], r['dislike_count'], r['average_rating'], r['url'], r['thumbnail']))
				else:
					yield from bot.send_typing(message.channel)
					yield from bot.send_message(message.channel, "Uh oh! Unable to get the information of the last song.")
			elif option == "desc":
				try:
					if not last == "None":
						options = {
						'format' : 'worstaudio/worst',
						'extractaudio' : False,
						'audioformat' : "mp3",
						'outtmpl' : 'music/%(id)s',
						'noplaylist' : True,
						}
						with youtube_dl.YoutubeDL(options) as ydl:
							r = ydl.extract_info(last, download=False)
						yield from bot.send_typing(message.channel)
						yield from bot.send_message(message.channel, "- Video Description -\r\nTitle: `{}`\r\n```{}```".format(r['title'], r['description']))
					else:
						yield from bot.send_typing(message.channel)
						yield from bot.send_message(message.channel, "Uh oh! Unable to get the video description of the last song.")
				except:
					yield from bot.send_typing(message.channel)
					yield from bot.send_message(message.channel, "Uh oh! Failed to get video description!")
			elif option == "playlast":
				try:
					yield from bot.send_typing(message.channel)
					msg = yield from bot.send_message(message.channel, "*Attempting to load last song...*")
					config = configparser.SafeConfigParser()
					config.read('music.ini')
					music = config.get('musicbot', 'last_song')
					options = {
						'format': 'bestaudio/best', # choice of quality
						'extractaudio' : False,      # only keep the audio
						'audioformat' : "mp3",      # convert to mp3 
						'outtmpl': 'music/%(id)s',        # name the file the ID of the video
						'noplaylist' : True,        # only download single song, not playlist
						}
					with youtube_dl.YoutubeDL(options) as ydl:
						msc = ydl.download([music])
						r = ydl.extract_info(music, download=False)
					yield from bot.delete_message(msg)
					yield from bot.send_message(message.channel, "Successfully loaded last song (`{}` by `{}`)!".format(r['title'], r['uploader']))
					#voice = yield from bot.join_voice_channel(message.author.voice_channel)
					if player.is_playing():
						player.stop()
					player = voice.create_ffmpeg_player('music/'+r['id'])
					cursong = r['title']
					author = r['uploader']
					player.start()
				except:
					yield from bot.send_typing(message.channel)
					yield from bot.send_message(message.channel, "Uh oh! Failed to load the last song!")
			elif option == "local":
				try:
					if not player.is_playing():
						song = message.content.split(' ')[2]
						yield from bot.send_typing(message.channel)
						yield from bot.send_message(message.channel, "*Attempting to play local song...*")
						cursong = "Local File"
						author = "Local Artist"
						player = voice.create_ffmpeg_player('music/'+song)
						player.start()
					else:
						song = message.content.split(' ')[2]
						yield from bot.send_typing(message.channel)
						yield from bot.send_message(message.channel, "*Attempting to play local song...*")
						player.stop
						player = voice.create_ffmpeg_player('music/'+song)
						cursong = "Local File"
						author = "Local Artist"
						player.start()
				except IndexError:
					yield from bot.send_typing(message.channel)
					yield from bot.send_message(message.channel, "Uh oh! You must include the name of the local song you wish to play.")
				except FileNotFoundError:
					yield from bot.send_typing(message.channel)
					yield from bot.send_message(message.channel, "Uh oh! That song was not found!")
			elif option == "end":
				yield from bot.send_typing(message.channel)
				msg = yield from bot.send_message(message.channel, "*Attempting to quit bot component...*")
				yield from bot.delete_message(msg)
				sys.exit()
			elif option == "restart":
				yield from bot.send_typing(message.channel)
				msg = yield from bot.send_message(message.channel, "*Attempting to restart bot component...*")
				yield from bot.delete_message(msg)
				os.startfile("musicbot.bat")
				sys.exit()

	#print("Playing music: "+str(iscon)+"\r\n"+"Reason: "+reason)"""

bot.run(infos[0], infos[1])
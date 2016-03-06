import discord
import asyncio
import os
import sys
import random
import json
import urllib.parse
from urllib.request import urlopen
import aiohttp
import requests
from bs4 import BeautifulSoup

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

		#if "join" in msg.content: #join command
				#invite = msg.content.split(" ")[2]
				#yield from bot.accept_invite(invite)
				#yield from bot.send_typing(msg.channel)
				#yield from bot.send_message(msg.channel, "Joining {}!".format(invite))

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

		if "search" in msg.content:
			search_string = msg.content.split(" ;")[1]
			query = urllib.parse.urlencode({'q': search_string})
			url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
			search_response = urllib.request.urlopen(url)
			search_results = search_response.read().decode("utf8")
			results = json.loads(search_results)
			data = results['responseData']
			print('Total results: %s' % data['cursor']['estimatedResultCount'])
			hits = data['results']
			print('Top %d hits:' % len(hits))
			#len(hits) = 1
			for h in hits:
				h = h['url']
			yield from bot.send_message(msg.channel, h)
			#for h in hits: yield from bot.send_message(msg.channel, h['url'])# print(' ', h['url'])
			#print('For more results, see %s' % data['cursor']['moreResultsUrl'])
			#return hits
			#search(searchin, 1)
			#yield from bot.send_typing(msg.channel)
			#yield from bot.send_message(msg.channel, search.hits)

		if "urban" in msg.content:
			urban_search = msg.content.split(" ;")[1]
			r = requests.get("http://www.urbandictionary.com/define.php?term={}".format(urban_search))
			soup = BeautifulSoup(r.content)
			urban = soup.find("div",attrs={"class":"meaning"}).text
			example = soup.find("div",attrs={"class":"example"}).text
			contributor = soup.find("div",attrs={"class":"contributor"}).text
			#print(soup.find("div",attrs={"class":"meaning"}).text)
			yield from bot.send_message(msg.channel, "{}\r\n{}\r\nContributed by {}".format(urban, example, contributor))

		if "osu" in msg.content:
			urban_search = msg.content.split(" ;")[1]
			r = requests.get("http://www.urbandictionary.com/define.php?term={}".format(urban_search))
			soup = BeautifulSoup(r.content)
			avatar = soup.find("div",attrs={"class":"meaning"}).text
			#print(soup.find("div",attrs={"class":"meaning"}).text)
			yield from bot.send_message(msg.channel, "{}\r\n{}\r\nContributed by {}".format(urban, example, contributor))

		if "quit" in msg.content:
			yield from bot.send_typing(msg.channel)
			yield from bot.send_message(msg.channel, "*Quitting...*")
			sys.exit()

	print("[CHAT][{}][{}][{}]: {}".format(str(msg.server), str(msg.channel), str(msg.author), msg.content))

def search(search_string):
	query = urllib.parse.urlencode({'q': search_string})
	url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
	search_response = urllib.request.urlopen(url)
	search_results = search_response.read().decode("utf8")
	results = json.loads(search_results)
	data = results['responseData']
	print('Total results: %s' % data['cursor']['estimatedResultCount'])
	hits = data['results']
	print('Top %d hits:' % len(hits))
	for h in hits: print(' ', h['url'])
	print('For more results, see %s' % data['cursor']['moreResultsUrl'])
	return hits

bot.run(infos[0], infos[1])
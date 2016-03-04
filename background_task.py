import discord
import asyncio

client = discord.Client()

#settings
fp_infos = open("pingbot.ini","r")
infos = fp_infos.read().split(":")
fp_infos.close()

def my_background_task():
	yield from client.wait_until_ready()
	counter = 0
	channel = discord.Object(id='106895034787352576')
	while not client.is_closed:
		counter += 1
		yield from client.send_message(channel, counter)
		yield from asyncio.sleep(5) # task runs every 60 seconds

@client.async_event
def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

loop = asyncio.get_event_loop()

try:
	loop.create_task(my_background_task())
	loop.run_until_complete(client.login(infos[0], infos[1]))
	loop.run_until_complete(client.connect())
except Exception:
	loop.run_until_complete(client.close())
finally:
	loop.close()
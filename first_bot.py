import random
import asyncio
import aiohttp
import json
from discord import Game
from discord.ext.commands import Bot


BOT_PREFIX = ("!")
TOKEN = 'NTg0MjkyMzU1MTM4NTE5MDUz.XPLH2Q.YD_OAt0xO_vzoZhdjxq875rKtgU'
client = Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)


@client.command(help='Bot gửi lời chào đến cả nhà iu.')
async def greet():
    possible_responses = [
        'Hello xin chào cả nhà iu của kem',
        'Hello xin chào cả nhà iu đụ đĩ mẹ cả nhà, ố là la',
    ]
    await client.say(random.choice(possible_responses))


@client.command(help='Bot làm bình phương cho nèk.')
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " bình là " + str(squared_value))


@client.command(help='Bot cho coi giá bitcoin nèk.')
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Giá nè con đĩ: $" + response['bpi']['USD']['rate'])


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)
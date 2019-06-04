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
    await client.change_presence(game=Game(name="with póngs"))
    print("Logged in as " + client.user.name)


@client.command(help='Bot gửi lời chào đến cả nhà iu.')
async def greet():
    possible_responses = [
        'Hello xin chào cả nhà iu của kem',
        'Hello xin chào cả nhà iu đụ đĩ mẹ cả nhà, ố là la',
    ]
    await client.say(random.choice(possible_responses))


@client.command(help='Chửi chết con đĩ mẹ nó.',
                description='type !chửi đứa_bị_chửi to get me chửi chết con đĩ mẹ nó',
                )
async def chửi(*person):
    if len(person) > 1:
        person = ' '.join(person)
    elif len(person) == 1:
        person = person[0]
    else:
        await client.say('Chửi ai má?')
    cursed_sentences = [
        'con đĩ mẹ mày',
        'nứng lồn quá chơi mình đi má ai rảnh đâu mà chơi',
        'dô diên nứng lồn hả đĩ chó',
        'cái lồn con đĩ mẹ mày',
        'muốn dzạt cái mỏ lồn mày ghê',
        'dòng thứ chổi phù thủy tao nhét dô lồn chết con đĩ mẹ mày nghe chưa',
        'póng mà giả trai đụ nai đụ bò',
        'tưởng đây ngu chắc hỏng pít tụi pây póng mà gồng',
        'nói chiện như cái lông lồn dị đó',
        'nói chiện như lồn trệt dưới mương',
        'bạn nói như dị là bạn xạo lồn',
        'con póng khùng, con póng nứng lồn',
        'có xạo lồn quá hong dạ',
        'thằng cha con đĩ mẹ mày',
        'dô diên mày nứng lồn hả tao xé lồn mày ra',
        
    ]
    await client.say(random.choice(cursed_sentences) + ' ' + person)


@client.command(help='Bot làm bình phương cho nèk.',
                description='type !square number to get me square up the number')
async def square(number):
    squared_value = float(number) * float(number)
    await client.say(str(number) + " bình là " + str(squared_value))


@client.command(help='Bot làm tính nhân cho nèk.', 
                description='type !mul num1 num2 num3 to get me multiply all of them')
async def mul(*args):
    result = 1
    for arg in args:
        result *= float(arg)
    await client.say('Ra ' + str(result) + ' nè.')


@client.command(help='Bot cho coi giá bitcoin nèk.')
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Giá nè con đĩ: $" + response['bpi']['USD']['rate'])



@client.command(help='Bot cho coi giá đô la nèk.')
async def usd():
    url = 'https://free.currconv.com/api/v7/convert?q=USD_VND&compact=ultra&apiKey=fc5de87be9f62c4191ef'
    async with aiohttp.ClientSession() as session:
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Hiện là {} đồng nhoe".format(response['USD_VND']))


@client.command(help='Thách mày xùm xì thắng tao đó con đĩ.', pass_context=True)
async def x(context):
    try:
        options = ['kéo', 'búa', 'bao']
        bot_choice = random.choice(options)
        bot_response = {
            'win': 'Tao ra ' + bot_choice + ', thắng mày rồi nhe.',
            'lose': 'Tao ra ' + bot_choice + ', hên thôi nhường mày 1 lần.'
        }
        await client.say('Chị ra gì? ' + context.message.author.mention)
        response = await client.wait_for_message(author=context.message.author)
        print(context.message.author)
        print(help(response))
        print(response.content)
        # for e in response:
        #     print(e)
        # print(help(response))
        if response.content == 'kéo':
            if bot_choice == 'búa':
                await client.say(bot_response['win'])
            elif bot_choice == 'bao':
                await client.say(bot_response['lose'])
        elif response.content == 'búa':
            if bot_choice == 'bao':
                await client.say(bot_response['win'])
            elif bot_choice == 'kéo':
                await client.say(bot_response['lose'])
        elif response.content == 'bao':
            if bot_choice == 'kéo':
                await client.say(bot_response['win'])
            elif bot_choice == 'búa':
                await client.say(bot_response['lose'])
        else:
            await client.say('Nói dì dạ hong hỉu?')
    except Exception as e:
        await client.say('chưa chơi được :(')
        print(e)


@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)
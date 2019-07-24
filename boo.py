# python lib
from datetime import datetime
import pprint
import random
import time

# external import
import feedparser
from utils.command import generate_help_message, generate_hello_message
from utils.log import get_logger
from utils.json_parser import dump_json_to_file, parse_json_file

# discord import
import asyncio
import discord
from discord.ext import tasks

# utils
pp = pprint.PrettyPrinter(indent=4)
logger, LOG_LEVEL, stream = get_logger()
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)
news_url = 'https://vnexpress.net/rss/tin-moi-nhat.rss'

# discord property
client = discord.Client()
TOKEN = 'NTg0MjkyMzU1MTM4NTE5MDUz.XPLH2Q.YD_OAt0xO_vzoZhdjxq875rKtgU'


class MyBoo(discord.Client):
    # load blessings
    _blessings = parse_json_file('data/blessings.json')
    logger.info('Blessings successfully loaded')
    # load server's emojis
    _emojis = parse_json_file("data/emojis.json")
    logger.info('Server\'s emojis successfully loaded')
    # load server's users
    _users = parse_json_file("data/users.json")
    logger.info('Server\'s users successfully loaded')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.send_news())

    async def on_ready(self):
        logger.info('We have logged in as {}'.format(self.user))
        # dump server's emojis to file data/emojis.json
        dump_json_to_file('emoji', self.emojis, "data/emojis.json")
        logger.info("Successfully get emojis to file data/emojis.json")
        # dump server's users to file data/users.json
        dump_json_to_file('user', self.users, 'data/users.json')
        logger.info('Successfully dump users to data/users.json')

        games = ["with the leaves", "with fire", "with you"]
        game = discord.Game(name=random.choice(games))
        await self.change_presence(status=discord.Status.online, activity=game)

    async def send_news(self):
        await self.wait_until_ready()
        # get channel báo-mới-mỗi-ngày
        news_channel = self.get_channel(602426911469207552)
        while not self.is_closed():
            logger.info('Runnning background task')
            now = datetime.now()
            if now.hour == 1: # at 8 AM Vietnam
                # get the latest news on vnexpress
                feed = feedparser.parse(news_url)
                logger.info('Successfully get information from url')
                for entryNo in range(5):
                    # get the title of the article
                    title = feed.entries[entryNo].title
                    # get the link of the article
                    link = feed.entries[entryNo].links[0].href
                    logger.info('Sending "{}" to {} at {}'.format(
                                title, news_channel, now))
                    await news_channel.send('**{}**\n{}'.format(title, link))
            await asyncio.sleep(3600) # task run every hour

    async def on_message(self, message):
        if message.author == client.user:
            return

        # Show help message
        if message.content.startswith('$help'):
            embed = generate_help_message(self._emojis)
            logger.info('Sending help message to {}'.format(message.channel))
            await message.channel.send(embed=embed)

        # Say Hello
        if message.content.startswith('$hello'):
            response, current_hour = generate_hello_message(self._blessings)
            logger.info('Sending "{}" to {} at {}'.format(
                        response, str(message.channel).upper(), current_hour))
            await message.channel.send(response)
        
        # Get all the users of the server
        if message.content.startswith('$user'):
            logger.info('Getting users of the server')
            await message.channel.send(self._users)

        # Slap contest
        if message.content.startswith('$slap'):
            mess = message.content.split()
            if len(mess) == 1:
                embed=discord.Embed(colour=0xfef249)
                embed.add_field(name='Slap contest',
                    value="{}, I'm seeing that you want"
                        " to slap but I don't see anyone "
                        "you want to slap. In case you want "
                        "to slap yourself, Here's a hand".format(message.author.mention))
                bot_mess = await message.channel.send(embed=embed)
                await bot_mess.add_reaction(self._emojis["fist"])
            # await message.channel.send('<@423461043935772682>')
            pass


def main():
    try:
        client = MyBoo()
        client.run(TOKEN)
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    main()

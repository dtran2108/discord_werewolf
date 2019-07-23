# python lib
from datetime import datetime
import pprint
import random
import time

# external import
import feedparser
from utils.command import generate_help_message
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.send_news())

    async def on_ready(self):
        logger.info('We have logged in as {}'.format(self.user))
        # dump server's emojis to file data/emojis.json
        dump_json_to_file('emoji', self.emojis, "data/emojis.json")
        logger.info("Successfully get emojis to file data/emojis.json")

        games = ["with the leaves", "with fire", "with you"]
        game = discord.Game(name=random.choice(games))
        await self.change_presence(status=discord.Status.online, activity=game)

    async def send_news(self):
        await self.wait_until_ready()
        # get the latest news on vnexpress
        feed = feedparser.parse(news_url)
        # get channel báo-mới-mỗi-ngày
        news_channel = self.get_channel(602426911469207552)
        logger.info('Successfully get information from url')
        while not self.is_closed():
            now = datetime.now()
            if now.hour == 8:
                for entryNo in range(5):
                    # get the title of the article
                    title = feed.entries[entryNo].title
                    # get the link of the article
                    link = feed.entries[entryNo].links[0].href
                    logger.info('Sending "{}" to {}'.format(title, news_channel))
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
            current_time = datetime.now()
            # 7 <= hour < 10
            if current_time.hour >= 7 and current_time.hour < 10:
                logger.info('It\'s morning so I\'m getting morning responses')
                response = random.choice(self._blessings["morning"])
            # 10 <= hour < 13
            elif current_time.hour >= 10 and current_time.hour < 13:
                logger.info('It\'s lunch time !!!')
                response = random.choice(self._blessings["lunch"])
            # 13 <= hour < 17
            elif current_time.hour >= 13 and current_time.hour < 17:
                logger.info('It\'s afternoon, doing something helpful')
                response = random.choice(self._blessings["afternoon"])
            # 17 <= hour < 22
            elif current_time.hour >= 17 and current_time.hour < 22:
                logger.info('It\'s evening, nothing left to say')
                response = random.choice(self._blessings["evening"])
            # 22 <= hour <= 23 or 0 <= hour < 7 
            elif ((current_time.hour >= 22 and current_time.hour <= 23)
                    or (current_time.hour >= 0 and current_time.hour < 7)):
                logger.info('It\'s late_night, going to sleep')
                response = random.choice(self._blessings["late_night"])
            await message.channel.send(response)
        
        # Get all the users of the server
        if message.content.startswith('$user'):
            logger.info('Getting users of the server')
            await message.channel.send(client.users)

        # Slap contest
        if message.content.startswith('$slap'):
            pass


def main():
    try:
        client = MyBoo()
        client.run(TOKEN)
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    main()

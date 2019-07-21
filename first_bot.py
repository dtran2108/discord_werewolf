from datetime import datetime
import discord
import feedparser
from log import get_logger
import time
import pprint
import random

pp = pprint.PrettyPrinter(indent=4)

client = discord.Client()
TOKEN = 'NTg0MjkyMzU1MTM4NTE5MDUz.XPLH2Q.YD_OAt0xO_vzoZhdjxq875rKtgU'
logger, LOG_LEVEL, stream = get_logger()
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)

url = 'https://vnexpress.net/rss/tin-moi-nhat.rss'

@client.event
async def on_ready():
    logger.info('We have logged in as {}'.format(client.user))
    games = ["with the leaves", "with fire"]
    game = discord.Game(name=random.choice(games))
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Show help message
    if message.content.startswith('$help'):
        embed=discord.Embed(description="Hi I'm Boo and I was assigned a mission to cheer you up",
                            colour=0xfef249)
        embed.set_author(name="Boo - Happy Virus v1.0.0")
        # commands
        embed.add_field(name=':hand_splayed: $hello', value="`I'll molasses\ninto your ear`", inline=True)
        embed.add_field(name=':newspaper: $news', value="`I'll get you\nthe latest news`", inline=True)
        # footer
        embed.set_footer(text="You're beautiful no matter what ❤️")
        logger.info('Sending help message to {}'.format(message.channel))
        await message.channel.send(embed=embed)

    # Say Hello
    if message.content.startswith('$hello'):
        logger.info('Saying hello')
        current_time = datetime.now()
        morning = [
            'Roses are red\nViolets are blue\nSugar is sweet\n'
            'And so are you\n\nHave a nice day ^^',
            'Hề lô, gụt mó ninh',
        ]
        lunch = [
            'Trưa rồi đi ăn trưa đi',
            'Cơm gà ngon đó, đi ăn đi',
            'Ăn đi rồi rửa mặt cho tỉnh táo quay lại làm việc nèk'
        ]
        afternoon = [
            'Chiều rồi đi học bài đi',
            'Không đi học thì chơi đàn đi',
            'Giặt đồ chưa? Đi giặt nhanh',
            'Tranh thủ ngủ trưa xíu đi, sau này không được ngủ đâu'
        ]
        evening = [
            'Đi ăn chiều đi tối rồi.',
            'Hôm nay, chị đi học hay ở nhà?\nCó gì thú vị kể em nghe',
            'Dọn nhà ik, nhà hơi dơ rồi đó'
        ]
        late_night = [
            'Giờ này giờ nào rồi sao chưa đi ngủ ???',
            '0 giờ rồi em ngủ đi em\nHơi đâu mà lo kế sinh nhaiii',
            'Mai có đi học không? Sao con mắt còn thao láo z ?',
            'Mai không đi học thì cũng nên đi ngủ sớm đi chị\nYêu chị gất nhiều ❤️',
            'Ông trời ơi ngó xuống mà coi h này nó còn thức nè\nNgủ đi má :mad:',
            'Khuya rồi mà chưa ngủ? Chơi bê đê ko?'
        ]
        # 7 <= hour < 10
        if current_time.hour >= 7 and current_time.hour < 10:
            logger.info('It\'s morning so I\'m getting morning responses')
            response = random.choice(morning)
        # 10 <= hour < 13
        elif current_time.hour >= 10 and current_time.hour < 13:
            logger.info('It\'s lunch time !!!')
            response = random.choice(lunch)
        # 13 <= hour < 17
        elif current_time.hour >= 13 and current_time.hour < 17:
            logger.info('It\'s afternoon, doing something helpful')
            response = random.choice(afternoon)
        # 17 <= hour < 22
        elif current_time.hour >= 17 and current_time.hour < 22:
            logger.info('It\'s evening, nothing left to say')
            response = random.choice(evening)
        # 22 <= hour <= 23 or 0 <= hour < 7 
        elif ((current_time.hour >= 22 and current_time.hour <= 23)
                or (current_time.hour >= 0 and current_time.hour < 7)):
            logger.info('It\'s late_night, going to sleep')
            response = random.choice(late_night)
        await message.channel.send(response)
    
    # Get all the users of the server
    if message.content.startswith('$user'):
        logger.info('Getting users of the server')
        await message.channel.send(client.users)

    # Send the latest news from vnexpress to channel
    # báo-mới-mỗi-ngày
    if message.content.startswith('$news'):
        # get the latest news on vnexpress
        feed = feedparser.parse(url)
        # get channel báo-mới-mỗi-ngày
        news_channel = client.get_channel(602426911469207552)
        logger.info('Successfully get information from url')

        for entryNo in range(5):
            e = discord.Embed()
            # get the title of the article
            title = feed.entries[entryNo].title
            summary = feed.entries[entryNo].summary
            # get the news image
            image_link = summary.split('<')[2].split('"')[1]
            e.set_image(url=image_link)
            # get the link of the article
            link = feed.entries[entryNo].links[0].href
            logger.info('Sending "{}" to {}'.format(title, news_channel))
            await news_channel.send('**{}**\n<{}>'.format(title, link), embed=e)


def main():
    try:
        client.run(TOKEN)
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    main()

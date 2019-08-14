# python lib
from datetime import datetime
import json
import pprint
import random
from string import ascii_uppercase
import time

# external import
import feedparser
from utils.log import get_logger
from utils.json_parser import dump_json_to_file, parse_json_file
from utils.tools import (embed_message,
                         generate_help_message,
                         generate_hello_message,
                         generate_spelling_result)

# discord import
import asyncio
import discord
from discord.ext import commands, tasks

# utils
pp = pprint.PrettyPrinter(indent=4)
logger, LOG_LEVEL, stream = get_logger()
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)
news_url = 'https://vnexpress.net/rss/thoi-su.rss'

# discord property
client = commands.Bot(command_prefix="$")
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

        # create the background tasks and run it in the background
        self.bg_send_news = self.loop.create_task(self.send_news())
        self.bg_update_users = self.loop.create_task(self.update_users())
        self.bg_load_users = self.loop.create_task(self.load_users())

    async def on_ready(self):
        logger.info('We have logged in as {}'.format(self.user))
        games = ["with the leaves", "with fire", "with you", "with your heart"]
        game = discord.Game(name=random.choice(games))
        await self.change_presence(status=discord.Status.online, activity=game)
    
    async def update_users(self):
        await self.wait_until_ready()
        try:
            while not self.is_closed():
                dump_json_to_file('user', self.users, 'data/users.json')
                await asyncio.sleep(2) # task run every two seconds
        except Exception as e:
            logger.error('An error occur while updating users: {}'.format(e))
    
    def update_emo(self):
        try:
            dump_json_to_file('emoji', self.emojis, 'data/emojis.json')
        except Exception as e:
            logger.error('An error occur while updating emojis: {}'.format(e))
        else:
            logger.info('Successfully dump users to data/emojis.json '
                        'in the background')

    def load_emo(self):
        try:
            self._emojis = parse_json_file('data/emojis.json')
        except Exception as e:
            logger.error('An error occur while loading emojis: {}'.format(e))
        else:
            logger.info('Successfully loaded emojis from the background')
    
    async def load_users(self):
        await self.wait_until_ready()
        try:
            while not self.is_closed():
                self._users = parse_json_file('data/users.json')
                await asyncio.sleep(1) # task run every second
        except Exception as e:
            logger.error('An error occur while updating users: {}'.format(e))
    
    async def send_news(self):
        await self.wait_until_ready()
        # get channel báo-mới-mỗi-ngày
        news_channel = self.get_channel(602426911469207552)
        while not self.is_closed():
            logger.info('Runnning send news in background')
            now = datetime.now()
            if now.hour == 1: # at 8 AM Vietnam
                # get the latest news on vnexpress
                feed = feedparser.parse(news_url)
                logger.info('Successfully get information'
                            ' from url: {}'.format(feed))
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

        # update emojis (for dev only)
        elif message.content.startswith('$emoup'):
            self.update_emo()
            self.load_emo()
            logger.info('Emojis updated')
        
        # load blessings (for dev only)
        elif message.content.startswith('$load_bless'):
            self._blessings = parse_json_file('data/blessings.json')
            await message.channel.send('All blessings loaded')
        
        # update new blessings (for dev only)
        elif message.content.startswith('$add_bless'):
            mess_content = message.content.split()
            time_period, content = mess_content[1], ' '.join(mess_content[2:])
            self._blessings[time_period].append(content)
            dump_json_to_file('bless', self._blessings, 'data/blessings.json')
            await message.channel.send('Blessing successfully updated\n'
                                       'Remember to reload blessings')
        
        # show blessings for time period (for dev only)
        elif message.content.startswith('$show_bless'):
            _, time_period = message.content.split()
            for blessing in self._blessings[time_period][-5:]:
                await message.channel.send('```\n{}\n```\n'.format(
                    blessing))
            await message.channel.send('\nTotal: {}'.format(
                len(self._blessings[time_period])))

        # Show help message
        elif message.content.startswith('$help'):
            embed = generate_help_message(message.content, self._emojis)
            logger.info('Sending help message to {}'.format(message.channel))
            await message.channel.send(embed=embed)

        # Say Hello
        elif message.content.startswith('$hello')\
             or message.content.startswith('$hi'):
            response, current_hour = generate_hello_message(self._blessings)
            logger.info('Sending "{}" to {} at {}'.format(
                        response, str(message.channel).upper(), current_hour))
            await message.channel.send(response)
        
        # Slap contest
        elif message.content.startswith('$slap'):
            if str(message.channel) not in ['dev-env', 'slap-room']:
                slap_room = self.get_channel(608969666047639563)
                embed=discord.Embed(colour=0xc4160a)
                embed.add_field(name="Wrong place to slap !!",
                                value="Sorry {}, please go to {} "
                                      "to start a slap contest".format(
                                        message.author.mention, slap_room))
                logger.warning('Wrong place to slap, '
                               'sending warning message !!')
                await message.channel.send(embed=embed)
            else:
                mess = message.content.split()
                # if the user slap themselves
                if len(mess) == 1:
                    embed = embed_message(message.author.mention, 0xfef249,
                            'Slap contest', ", I'm seeing that you want"
                            " to slap but I don't really see "
                            "a name. In case you want "
                            "to slap yourself, here's a hand\n"
                            "You have 10 seconds to make a decision")
                    bot_mess = await message.channel.send(embed=embed)
                    await bot_mess.add_reaction(self._emojis["fist"])
                    # check if the author react with the right emoji
                    def check(reaction, user):
                        logger.info("Checking user and emoji "
                                    "if the user slap himself: "
                                    "user: {}, emo: {}".format(
                            user == message.author,
                            str(reaction.emoji) == self._emojis["fist"],
                        ))
                        return user == message.author \
                            and str(reaction.emoji) == self._emojis["fist"]
                    
                    try: 
                        # wait for user's reactions and perform
                        # the check func above
                        reaction, user = await self.wait_for('reaction_add',
                                                    timeout=15.0, check=check)
                    # if the user didn't slap
                    except asyncio.TimeoutError:
                        embed = embed_message(message.author.mention, 0xfef249,
                            'Slap contest', ", Time is up. It's hard"
                                            " to hurt yourself right? "
                            "But honestly, who the hell would hurt themselves "
                            "like that. Carry on the love for yourself",
                            thumbnail=True,
                            url="https://www.flaticon.com/premium-icon/"
                                "icons/svg/1910/1910815.svg")
                        logger.info('They didn\'t slap, editting message')
                        await bot_mess.edit(embed=embed)
                    else: # if they slapped
                        embed = embed_message(message.author.mention, 0xfef249,
                            'Slap contest', ", Oh, what a slap! Did it hurt? "
                            "It's okay babe. Come here, I'll give "
                            "you a hug\nThere there", thumbnail=True, 
                            url="https://www.flaticon.com/premium-icon/"
                                "icons/svg/1744/1744732.svg")
                        logger.info('They slapped, editting message')
                        await bot_mess.edit(embed=embed)
                else: # user found someone to slap
                    embed = discord.Embed(colour=0xfef249)
                    embed.add_field(name="Slap contest",
                                    value="Beware {}, The great {} challenge"
                                        " you to a slap contest\n"
                                        "Accept or not?".format(
                                            mess[1], message.author.mention
                                        ))
                    slap_mess = await message.channel.send(embed=embed)
                    await slap_mess.add_reaction(self._emojis["absolutely"])
                    # check if the oponent react with the absolutely emojis
                    def _check(reaction, user):
                        logger.info("Checking user and emoji "
                                    "if the opponent say yes: "
                                    "user: {}, emo: {}".format(
                            user.mention == mess[1],
                            str(reaction.emoji) == self._emojis["absolutely"],
                        ))
                        return user.mention == mess[1] \
                            and str(reaction.emoji) == \
                                self._emojis["absolutely"]
                    try: # wait for user's reactions and perform
                         # the check func above
                        reaction, user = await self.wait_for('reaction_add',
                                                    timeout=10.0, check=_check)
                    except asyncio.TimeoutError:
                        # if the opponent didn't accept
                        embed = embed_message(message.author.mention, 0xfef249,
                            'Slap contest', ", sorry, {} don't have "
                                            "time or something idk\n"
                                            "Please try again later.".format(
                                                mess[1]),
                                            thumbnail=True, 
                            url="https://www.flaticon.com/premium-icon/" \
                                "icons/svg/1650/1650336.svg")
                        logger.info("The opponent didn't agree, "
                                    "editting message")
                        await slap_mess.edit(embed=embed)
                    else: # if the opponent accepted
                        # challenger's turn
                        challenger_embed = discord.Embed(colour=0xfef249)
                        challenger_embed.add_field(name="Slap contest",
                                        value="It's your turn {}, time "
                                              "to scare your opponent".format(
                                                message.author.mention))
                        res = await message.channel.send(embed=challenger_embed)
                        await res.add_reaction(self._emojis["fist"])
                        challenger_start = datetime.now()
                        challenger_reaction, user = await self.wait_for(
                            'reaction_add',
                            check=lambda reaction,
                                    user: (str(reaction.emoji) == \
                                        self._emojis["fist"])\
                                    and (user == message.author))
                        if challenger_reaction:
                            challenger_time = datetime.now() - challenger_start
                        # opponent's turn
                        opponent_embed = discord.Embed(colour=0xfef249)
                        opponent_embed.add_field(name="Slap contest",
                                        value="Now's yours {}, "
                                              "prove yourself!".format(
                                                  mess[1]))
                        response = await message.channel.send(
                            embed=opponent_embed)
                        await response.add_reaction(self._emojis["fist"])
                        opponent_start = datetime.now()
                        opponent_reaction, user = \
                            await self.wait_for(
                                'reaction_add',
                                check=lambda reaction,
                                        user: (str(reaction.emoji) == \
                                            self._emojis["fist"])\
                                        and (user.mention == mess[1]))
                        if opponent_reaction:
                            opponent_time = datetime.now() - opponent_start
                        # get result of the contest
                        if challenger_time < opponent_time:
                            result_embed = discord.Embed(colour=0xfef249)
                            result_embed.add_field(
                                name="Slap contest - Result",
                                value="Congratulations {}!\n"
                                      "You slapped {} out of "
                                      "the server".format(
                                            message.author.mention, mess[1]
                                        ))
                            winner, loser = message.author.id, self.get_user(
                                int(mess[1][2:-1]))
                        else:
                            result_embed = discord.Embed(colour=0xfef249)
                            result_embed.add_field(
                                name="Slap contest - Result",
                                value="Congratulations {}!\n"
                                      "You slapped {} out of the server".format(
                                            mess[1], message.author.mention
                                        ))
                            winner, loser = mess[1][2:-1], message.author
                        result_embed.set_thumbnail(
                            url="https://www.flaticon.com/"
                                "premium-icon/icons/svg/1926/1926050.svg")
                        await message.channel.send(embed=result_embed)
                        my_server = self.get_guild(593748332203999232)
                        await my_server.kick(loser)
                        try: # send DM to loser
                            loser_dm = await loser.create_dm()
                            logger.info('Sending DM to the loser')
                            await loser_dm.send(
                                'You have been slapped out of Bita In '
                                'Wonder Land\nWanna rejoin?\n'
                                'https://discord.gg/cCgaTVv')
                        except discord.Forbidden:
                            # send invite link to channel
                            embed=discord.Embed(colour=0xc4160a)
                            embed.add_field(
                                name="I was rejected",
                                value="Sorry I can't send a DM to {} :(\n"
                                      "Can anyone with a kind heart "
                                      "please invite them back?\n"
                                      "Thanks\nhttps://discord.gg/"
                                      "cCgaTVv".format(loser.mention))
                            logger.warning(
                                'Cannot send DM to the loser, sending invite '
                                'link to channel')
                            await message.channel.send(embed=embed)
        # Vietnamese spellings
        elif message.content.startswith('$cta') \
                or message.content.startswith('$chinhta'):
            unicode_letters = ['🇦', '🇧', '🇨', '🇩']
            choices = {}
            choices_string = ''
            questions = parse_json_file('data/spellings.json')
            # the question is also the answer
            random_question = list(questions.keys())[random.randint(
                0, len(questions)-1)]
            # get the answers of the question
            custom_answers = questions[random_question]
            logger.info('Successfully parse questions')
            logger.info('Random question is: {}'.format(random_question))
            random.shuffle(custom_answers)
            i = 0
            for answer in custom_answers:
                choices_string +=  '`[ {} ]:` {}\n'.format(
                    ascii_uppercase[i], answer)
                choices[unicode_letters[i]] = answer
                i += 1
            # get the right answer in unicode form
            for choice in choices.keys():
                if choices[choice] == random_question:
                    right_answer = choice
                    break
            embed=discord.Embed(colour=0xeddb39)
            embed.add_field(name="Vietnamese spelling quick question in 10s\n"
                                    "Which one is correct?",
                            value=choices_string+'\n{}, please react'
                                                 ' a letter.'.format(
                                message.author.mention
                            ))
            mess = await message.channel.send(embed=embed)
            for i in range(len(custom_answers)):
                await mess.add_reaction(unicode_letters[i])
            def __check(reaction, user):
                return user == message.author
            try:
                reaction, user = await self.wait_for('reaction_add',
                                            timeout=10.0, check=__check)
            except asyncio.TimeoutError: # if the user didn't react anything
                result = generate_spelling_result(
                    custom_answers, random_question)
                embed=discord.Embed(colour=0xfa031c)
                embed.add_field(name="Vietnamese spelling quick "
                                     "question in 10s\n"
                                     "Which one is correct?",
                                value=result+'\n{}, time out!, '
                                             'the answer is {}'.format(
                                                 message.author.mention,
                                                 right_answer))
                await mess.edit(embed=embed)
            else:
                # if the user reacted something,
                # if the answer is wrong we have to wait for 10 secs
                if reaction.emoji != right_answer: # if it is a wrong answer
                    result = generate_spelling_result(
                        custom_answers, random_question)
                    embed=discord.Embed(colour=0xfa031c)
                    embed.add_field(name="Vietnamese spelling "
                                         "quick question in 10s\n"
                                         "Which one is correct?",
                                    value=result+'\n{}, nope, it\'s {}'.format(
                                        message.author.mention, right_answer))
                    await mess.edit(embed=embed)
                else: # if it is right
                    result = generate_spelling_result(
                        custom_answers, random_question)
                    embed=discord.Embed(colour=0x09e30d)
                    embed.add_field(name="Vietnamese spelling "
                                         "quick question in 10s\n"
                                         "Which one is correct?",
                                    value=result+'\n{}, you are '
                                                 'absolutely right!'.format(
                                        message.author.mention
                                    ))
                    await mess.edit(embed=embed)
            
                    
def main():
    try:
        client = MyBoo()
        client.run(TOKEN)
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    main()

from datetime import datetime
import discord
import random
from string import ascii_uppercase


def embed_message(author, color, name, value, thumbnail=False, url=''):
    embed=discord.Embed(colour=color)
    embed.add_field(name=name, value=author+value)
    if thumbnail: embed.set_thumbnail(url=url)
    return embed


def generate_spelling_result(lang, custom_answers, random_question, author,
                             right_answer, meaning, example, kind, pronounce):
    """
    Return embed to send message to the channel

    :param list custom_answers: the answers of the question
    :param str random_question: the question as well as the answer
    :param str author: the author who run the command
    :param str right_answer: the right answer in unicode form
    :param str meaning: meaning of the question
    :param str example: use case of the question
    :param str kind: type of the answer the author chose

    :example:

    >>> custom_answers = ['abc', 'def']
    >>> random_question = 'abc'
    >>> author = <@:123456789098>
    >>> right_answer = 'A'
    >>> kind = 'wrong'
    >>> embed = generate_spelling_result(custom_answers, random_question, author, right_answer, kind)
    >>> print(embed)
    Vietnamese spelling quick question in 10s
    Which one is correct?
    **`[ A ]:` abc**
    ~~`[ B ]:` def~~

    <@:123456789098>, nope, it's A
    """
    if lang == 'vn':
        heading = "Vietnamese"
    elif lang == 'en':
        heading = "English"
    heading += " spelling quick question in 10s\nWhich one is correct?"
    i, result = 0, ''
    for answer in custom_answers:
        if answer == random_question:
            result +=  '**`[ {} ]:` {}\n**'.format(ascii_uppercase[i], answer)
            i += 1
        else:
            result +=  '~~`[ {} ]:` {}\n~~'.format(ascii_uppercase[i], answer)
            i += 1
    def _generate_embed(color):
        embed=discord.Embed(colour=color)
        value = '**Pronounce**: {}\n{}'.format(pronounce, result) if pronounce else result
        embed.add_field(name=heading, value=value, inline=False)
        embed.add_field(name="Meaning", value=meaning, inline=False)
        embed.add_field(name="Example",value=example, inline=False)
        return embed
    if kind == 'wrong':
        result += '\n{}, nope, it\'s {}\n'.format(author, right_answer)
        embed = _generate_embed(0xfa031c)
    elif kind == 'right':
        result += '\n{}, you are absolutely right!\n'.format(author)
        embed = _generate_embed(0x09e30d)
    elif kind == 'time-out':
        result += '\n{}, time out!, the answer is {}\n'.format(author, right_answer)
        embed = _generate_embed(0xfa031c)
    return embed


def generate_help_message(message, emojis):
    if message.endswith('dev'):
        embed=discord.Embed(
            title=emojis["kitty"] + " **Boo - The Happy Virus**",
            description="A help menu for dev only",
            colour=0xfef249
        )
        # commands
        embed.add_field(
            name='`$emoup`',
            value='`Update server\'s\nemojis`',
            inline=True
        )
        embed.add_field(
            name="`$load_bless`",
            value="`Load blessings\nin case blessings\nwere updated\nbut never"
                  " loaded`",
            inline=True           
        )
        embed.add_field(
            name='`$add_bless`',
            value="`Add new bless\n',,': '\\n'\n[time] [new_bless]`",
            inline=True
        )
        embed.add_field(
            name='`$show_bless`',
            value="`Show bless on time\n[time]: morning, lunch\nafternoon, "
                  "evening, late_night`"
        )
        # footer
        embed.set_footer(text="Dev tool | {}".format(datetime.now()))
    else:    
        embed=discord.Embed(
            title=emojis["kitty"] + " **Boo - The Happy Virus**",
            description="Hi I'm Boo and I was assigned a " \
                        "mission to cheer you up",
            colour=0xfef249
        )
        # commands
        embed.add_field(
            name=':hand_splayed: $hello | $hi',
            value="`I'll molasses\ninto your ear`",
            inline=True
        )
        embed.add_field(
            name=emojis["competition"]+' $slap',
            value="`Have a bad day?\nTell me who you\nwant to slap`",
            inline=True
        )
        embed.add_field(
            name=':pencil: $spell | $spelling',
            value="`Check your spellings\n$spell vn | $spell en`",
            inline=True
        )
        # footer
        embed.set_footer(text="You're beautiful no matter what ❤️")
    return embed

def generate_hello_message(blessings):
    # +7.00 to get Vietnam clock
    current_hour = datetime.now().hour + 7
    if current_hour >= 24:
        current_hour -= 24
    # 7 <= hour < 10
    if current_hour >= 7 and current_hour < 10:
        response = random.choice(blessings["morning"])
    # 10 <= hour < 13
    elif current_hour >= 10 and current_hour < 13:
        response = random.choice(blessings["lunch"])
    # 13 <= hour < 17
    elif current_hour >= 13 and current_hour < 17:
        response = random.choice(blessings["afternoon"])
    # 17 <= hour < 22
    elif current_hour >= 17 and current_hour < 22:
        response = random.choice(blessings["evening"])
    # 22 <= hour <= 23 or 0 <= hour < 7 
    elif ((current_hour >= 22 and current_hour <= 23)
            or (current_hour >= 0 and current_hour < 7)):
        response = random.choice(blessings["late_night"])
    return response, current_hour

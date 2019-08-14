from datetime import datetime
import discord
import random
from string import ascii_uppercase


def embed_message(author, color, name, value, thumbnail=False, url=''):
    embed=discord.Embed(colour=color)
    embed.add_field(name=name, value=author+value)
    if thumbnail: embed.set_thumbnail(url=url)
    return embed


def generate_spelling_result(custom_answers, random_question):
    i, result = 0, ''
    for answer in custom_answers:
        if answer == random_question:
            result +=  '**`[ {} ]:` {}\n**'.format(ascii_uppercase[i], answer)
            i += 1
        else:
            result +=  '~~`[ {} ]:` {}\n~~'.format(ascii_uppercase[i], answer)
            i += 1
    return result


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
            value="`Add new bless\n[time] [new_bless]`",
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
            name=':pencil: $chinhta | $cta',
            value="`Check your Vietnamese\nspellings`",
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

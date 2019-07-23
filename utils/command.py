import discord


def generate_help_message(emojis):    
    embed=discord.Embed(
        title=emojis["kitty"] + " **Boo - The Happy Virus**",
        description="Hi I'm Boo and I was assigned a mission to cheer you up",
        colour=0xfef249
    )
    # commands
    embed.add_field(
        name=':hand_splayed: $hello',
        value="`I'll molasses\ninto your ear`",
        inline=True
    )
    embed.add_field(
        name=emojis["competition"]+' $slap',
        value="`Have a bad day?\nTell me who you\nwant to slap`",
        inline=True
    )
    # footer
    embed.set_footer(text="You're beautiful no matter what ❤️")
    return embed

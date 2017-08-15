#!/usr/bin/env python

import discord
import os

client = discord.Client()


def get_role(role_name, message):
    """Returns the Role object referred to in message"""
    roles = message.server.roles
    role = None
    for r in roles:
        if r.name == role_name:
            role = r
    return role


def check_mc_role(message):
    """Returns if the Mega Corporation Role has been assigned to the user"""
    roles = message.author.roles
    assigned = False
    for r in ['Cosmo Stellar', 'Humanoid', 'Gene-X', 'Nyoko Labs']:
        role = get_role(r, message)
        if role in roles:
            assigned = True
    return assigned


def get_emoji(name):
    """Returns the identifier for the given emoji name"""
    emojis = client.get_all_emojis()
    emoji = ""
    for ident in emojis:
        if name in str(ident):
            emoji = ident
    return emoji


async def parse_ping(message):
    """Sends a direct message to the user responding to the $ping command"""
    await client.send_message(message.author, "Hi!")


async def parse_help(message):
    """Sends a direct message to the user responding to the $help command"""
    client.start_private_message(message.author)
    reply = "Howdy! Here is what I currently know:\n\n"
    reply += "$MegaCorp <corporation>\n"
    reply += "  Adds a Discord role corresponding to your Mega Corporation to your user.\n"
    reply += "  Replace '<corporation>' with your corporation.\n"
    reply += "  Accepted values are 'Cosmo Stellar', 'Humanoid', 'Gene-X', and 'Nyoko Labs'.\n"
    reply += "$ping\n"
    reply += "  Pong!\n"
    reply += "$version\n"
    reply += "  Returns the current version of the bot in a DM.\n"
    await client.send_message(message.author, reply)


async def parse_version(message):
    """Sends a direct message to the user responding to the $version command"""
    try:
        f = open('VERSION', 'r')
        version = f.readline().strip()
        f.close()
        await client.send_message(message.author, "Version: {}".format(version))
    except Exception as e:
        print(e)


async def apply_mc_role(message, mc):
    """Applies the specified Mega Corporation role and reacts with the sorting hat"""
    try:
        await client.add_roles(message.author, get_role(mc, message))
        await client.add_reaction(message, get_emoji("sorting_hat"))
        await client.send_message(message.author, "Successfully applied {} role".format(mc))
    except Exception as e:
        print(e)


async def parse_megacorp(message):
    """Sends a direct message to the user responding to the $MegaCorp command"""
    words = message.content.split(' ')
    assigned = check_mc_role(message)
    if not assigned:
        if len(words) == 3 and words[1].lower() == "cosmo" and words[2].lower() == "stellar":
            await apply_mc_role(message, "Cosmo Stellar")
        elif len(words) == 2 and words[1].lower() == "humanoid":
            await apply_mc_role(message, "Humanoid")
        elif len(words) == 2 and words[1].lower() == "gene-x":
            await apply_mc_role(message, "Gene-X")
        elif len(words) == 3 and words[1].lower() == "nyoko" and words[2].lower() == "labs":
            await apply_mc_role(message, "Nyoko Labs")
        else:
            await client.send_message(message.author,
                                      "Invalid command. See $help for syntax and parameters of commands")
    else:
        await client.send_message(message.author, "Your Mega Corporation role has already been applied")


async def parse_content_creation(message):
    """Deletes any messages that aren't media in #content_creation"""
    if len(message.attachments) == 0:
        await client.delete_message(message)


@client.event
async def on_ready():
    """Called when bot is successfully logged in and ready for input"""
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')


@client.event
async def on_message(message):
    """Called when a message is sent to a channel the bot is a member of"""
    if message.channel.name == "content_creation":
        await parse_content_creation(message)
    else:
        if message.content.startswith('$ping'):
            await parse_ping(message)
        elif message.content.startswith('$help'):
            await parse_help(message)
        elif message.content.startswith('$version'):
            await parse_version(message)
        elif message.content.startswith('$MegaCorp'):
            await parse_megacorp(message)

client.run(os.environ['DISCORD_TOKEN'])

from collections import defaultdict
from typing import Dict, List
import os

import discord
from discord import Member
from discord.channel import TextChannel
from discord.guild import Guild
from discord.role import Role
from discord.message import Message
from discord.embeds import Embed

import topics


client: discord.Client = discord.Client()
queues: Dict[str, List[Member]] = defaultdict(list)


def get_all_topics(guild: Guild) -> List[str]:
    roles: List[Role] = guild.roles
    r: Role
    return [r.name[6:] for r in roles if r.name.startswith('Class-')]


async def showtopics(user: Member, channel: TextChannel) -> None:
    out = user.mention + " List of classes:\n"
    out += "\n".join(get_all_topics(channel.guild))
    await channel.send(out)


async def joinqueue(user: Member, channel: TextChannel, topic: str) -> None:
    if topic not in get_all_topics(channel.guild):
        await channel.send(
            user.mention + ' Topic {} does not exist.'.format(topic)
        )
        return

    if user in queues[topic]:
        queues[topic].remove(user)
        await channel.send(
            user.mention + ' has left the {} queue.'.format(topic)
        )
    else:
        queues[topic].append(user)
        await channel.send(
            user.mention + ' has joined the {} queue.'.format(topic)
        )


async def showqueue(caller: Member, channel: TextChannel, topic: str) -> None:
    user: Member
    if len(queues[topic]) == 0:
        await channel.send(
            '{} Queue "{}" is empty.'.format(caller.mention, topic)
        )
    else:
        out: str = '{} Members in "{}" queue:\n'.format(caller.mention, topic)
        for user in queues[topic]:
            out += user.display_name + '\n'
        await channel.send(out)


@topics.check_admin
async def ready(mentor: Member, channel: TextChannel, topic: str) -> None:
    student: Member = queues[topic].pop(0)
    await channel.send(
        mentor.mention + " is ready for " + student.mention + "."
    )


async def help(channel: TextChannel) -> None:
    embedVar = Embed(
        title="Help!",
        description="Possible commands:",
        color=0xf76902
    )
    embedVar.add_field(
        name="$joinqueue <topic>",
        value="Add yourself to an existing queue.",
        inline=False
    )
    embedVar.add_field(
        name="$showqueue <topic>",
        value="Show the people currently in queue.",
        inline=False
    )
    embedVar.add_field(
        name="$showtopics",
        value="Lists all topics.",
        inline=False
    )
    embedVar.add_field(
        name="$ready (admin only)",
        value="Move to the next person in the queue.",
        inline=False
    )
    embedVar.add_field(
        name="$maketopic <name> (admin only)",
        value="Create a topic.",
        inline=False
    )
    embedVar.add_field(
        name="$deletetopic <name> (admin only)",
        value="Deletes a topic.",
        inline=False
    )
    embedVar.add_field(
        name="$clear <topic> (admin only)",
        value="Clears the queue of the specified topic.",
        inline=False
    )
    await channel.send(embed=embedVar)


@client.event
async def on_ready() -> None:
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game("$help"))


@topics.check_admin
async def clear(caller: Member, channel: TextChannel, topic: str) -> None:
    queues[topic] = list()
    await channel.send(caller + " has cleared the queue for " + topic + ".")


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    if message.content.startswith('$'):
        tokens: List[str] = message.content[1:].split(' ')
        if tokens[0] == 'joinqueue':
            await joinqueue(message.author, message.channel, tokens[1])
        elif tokens[0] == 'showtopics':
            await showtopics(message.author, message.channel)
        elif tokens[0] == 'ready':
            await ready(message.author, message.channel, tokens[1])
        elif tokens[0] == 'showqueue':
            await showqueue(message.author, message.channel, tokens[1])
        elif tokens[0] == 'help':
            await help(message.channel)
        elif tokens[0] == 'maketopic':
            await topics.maketopic(message.author, message.channel, tokens[1])
        elif tokens[0] == 'deletetopic':
            await topics.deletetopic(
                message.author, message.channel, tokens[1]
            )
        elif tokens[0] == 'clear':
            await clear(message.author, message.channel, tokens[1])
        else:
            await message.channel.send(
                "Invalid command. Type $help if you need somebody."
            )


if __name__ == "__main__":
    client.run(os.getenv('LEHRBOT_API_KEY', ''))

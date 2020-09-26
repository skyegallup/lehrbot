from typing import List

import discord
from discord.user import User
from discord.message import Message


client = discord.Client()


async def joinqueue(user: User) -> None:
    print(user.name)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    if message.content.startswith('$'):
        tokens: List[str] = message.content[1:].split(' ')
        if tokens[0] == 'joinqueue':
            await joinqueue(message.author)
        await message.channel.send('Hello!')


client.run('NzU5NDU0ODE0NTUxMTQ2NTA2.X29vaQ.MuNF7XmF8mefy-_WzxB4vUYbAUM')

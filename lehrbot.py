from typing import List

import discord
from discord.user import User
from discord.message import Message


client = discord.Client()

queue = []

async def queue_list(command, user):
    if command == "joinqueue":
        queue.append(user)
    if command == "ready":
        queue.pop()

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
            cue_list(tokens[0], tokens[1])
            await joinqueue(message.author)
        await message.channel.send('Hello!')


client.run('NzU5NDU0ODE0NTUxMTQ2NTA2.X29vaQ.MuNF7XmF8mefy-_WzxB4vUYbAUM')

#!/usr/bin/env python3

import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = ''

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.content == '$bean':
        response = 'In progress'
        await message.channel.send(response)

    if message.content == '$beanbomb':
        response = 'Not yet'
        await message.channel.send(response)

    if message.content == '$beannuke':
        response = 'No.'
        await message.channel.send(response)

client.run(TOKEN)
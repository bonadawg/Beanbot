#!/usr/bin/env python3

import os
import discord
from dotenv import load_dotenv
import boto3
#from PIL import Image
import io
import aiohttp
import random

load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']

client = discord.Client()
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
b = 'beanimages'

aws_client = boto3.client('s3', aws_access_key_id=client_id, aws_secret_access_key=client_secret)

obj = aws_client.list_objects_v2(Bucket=b)

beans = obj['Contents']

def get_bean():

    pic_name = beans[random.randint(0, len(beans)-1)]['Key']

    base_url=f'https://{b}.s3.us-east-2.amazonaws.com/'

    img_data = base_url+pic_name

    return img_data

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.content == '$bean':
        img_data = get_bean()
        async with aiohttp.ClientSession() as session:
            async with session.get(img_data) as resp:
                if resp.status != 200:
                    return await channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, img_data))

    if message.content == '$beanbomb':
        s = set()
        for _ in range(5):
            curr = get_bean()
            while curr in s:
                curr = get_bean()
            s.add(curr)

            async with aiohttp.ClientSession() as session:
                async with session.get(curr) as resp:
                    if resp.status != 200:
                        return await channel.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await message.channel.send(file=discord.File(data, curr))

    if message.content == '$beannuke':
        response = 'No.'
        await message.channel.send(response)

    if message.content == '$beannihilate':
        s = set()
        for _ in range(15):
            curr = get_bean()
            while curr in s:
                curr = get_bean()
            s.add(curr)

            async with aiohttp.ClientSession() as session:
                async with session.get(curr) as resp:
                    if resp.status != 200:
                        return await message.author.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await message.author.send(file=discord.File(data, curr))


client.run(TOKEN)

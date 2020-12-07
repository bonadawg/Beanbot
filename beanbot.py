#!/usr/bin/env python3

import os
import discord
from dotenv import load_dotenv
import boto3
#from PIL import Image
import io
import aiohttp

load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']

client = discord.Client()
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
b = 'beanimages'

aws_client = boto3.client('s3', aws_access_key_id=client_id, aws_secret_access_key=client_secret)

aws_client.list_objects_v2(Bucket=b)

jpg = aws_client.get_object(Bucket=b,Key='bean.jpg')['Body']

base_url=f'https://{b}.s3.us-east-2.amazonaws.com/'

img_data = base_url+'bean.jpg'


#print(img_data)

#return Image.open(io.BytesIO(img_data))


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.content == '$bean':
        #response = img_data
        #await message.channel.send(response)
        #discord.Embed().set_image(url=img_data)
        async with aiohttp.ClientSession() as session:
            async with session.get(img_data) as resp:
                if resp.status != 200:
                    return await channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, 'cool_image.png'))

    if message.content == '$beanbomb':
        response = 'Not yet'
        await message.channel.send(response)

    if message.content == '$beannuke':
        response = 'No.'
        await message.channel.send(response)

client.run(TOKEN)

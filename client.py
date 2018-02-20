import discord
import json
import logging
import inspect
from discord.ext import commands
from nvidia import NvidiaGPUInfoBot

logging.basicConfig(level=logging.INFO)

with open('./config/auth.json') as data_file:
    auth = json.load(data_file)

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description='GPU Process Info Bot.')
gpuInfo = NvidiaGPUInfoBot(bot)
bot.add_cog(gpuInfo)

@bot.event
async def on_ready():
    logging.info('Logged in as:{0} (ID: {0.id})'.format(bot.user))

bot.run(auth['token'])

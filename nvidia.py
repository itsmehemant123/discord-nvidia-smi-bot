import discord
from discord.ext import commands
import logging
import subprocess

class NvidiaGPUInfoBot:

    def __init__(self, bot):
        logging.basicConfig(level=logging.INFO)
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def info(self, ctx):
        result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE)
        await self.bot.send_message(ctx.message.channel, result.stdout)
        

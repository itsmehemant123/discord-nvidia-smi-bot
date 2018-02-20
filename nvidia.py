import discord
from datetime import datetime
from dateutil import tz
from discord.ext import commands
import logging
import subprocess
from pynvml import *


class NvidiaGPUInfoBot:

    def __init__(self, bot):
        logging.basicConfig(level=logging.INFO)
        self.bot = bot
        self.to_zone = tz.gettz('America/Indianapolis')

    @commands.command(pass_context=True, no_pm=True)
    async def info(self, ctx):
        nvmlInit()
        
        deviceCount = nvmlDeviceGetCount()
        usage = discord.Embed(title='GPU Usage',
                              description='My Embed Content.', colour=0x00CC33, timestamp=datetime.now().astimezone(self.to_zone))

        status = ""

        for i in range(deviceCount):
            dHandle = nvmlDeviceGetHandleByIndex(i)

            gpuInfo = "*Device " + str(i) + "*\n"

            dName = nvmlDeviceGetName(dHandle).decode("utf-8")
            # dMemInfo = nvmlDeviceGetMemoryInfo(dHandle) #total, free, used
            dUtil = nvmlDeviceGetUtilizationRates(dHandle) # gpu, memory
            gpuInfo += "**GPU Usage**: " + \
                str(dUtil.gpu) + "%\n**Memory Usage**: " + \
                str(dUtil.memory) + "%\n"

            dFanSpeed = nvmlDeviceGetFanSpeed(dHandle) # print with %
            gpuInfo += "**Fan Speed**: " + str(dFanSpeed) + "%"
            if (dFanSpeed > 85):
                gpuInfo += "🔥"
            gpuInfo += "\n"

            dPerfState = nvmlDeviceGetPerformanceState(dHandle)
            gpuInfo += "**Perf. State**: " + str(dPerfState) + "\n"
            
            dGPUTemps = nvmlDeviceGetTemperature(dHandle, NVML_TEMPERATURE_GPU) # prints in Celcius
            gpuInfo += "**Temperature**: " + str(dGPUTemps) + "C"
            if (dGPUTemps > 80):
                gpuInfo += "🔥"
            gpuInfo += "\n"

            dCurrentWattage = nvmlDeviceGetPowerUsage(dHandle) # divide by 1000 to get wattage
            dMaxWattage = nvmlDeviceGetEnforcedPowerLimit(dHandle) # same as above
            gpuInfo += "**Wattage**: " + \
                str(dCurrentWattage / 1000) + "W / " + \
                str(dMaxWattage / 1000) + "W"
            if ((dCurrentWattage / dMaxWattage) > 90):
                gpuInfo += "⚡️"
            gpuInfo += "\n"

            # dProcs = nvmlDeviceGetComputeRunningProcesses(dHandle)

            status += "*Device " + str(i) + "*: " + dName
            if (dUtil.gpu == 0 and dUtil.memory == 0):
                status += "✅\n"
            else:
                status += "❌\n"

            usage.add_field(name=dName, value=gpuInfo, inline=True)
        
        nvmlShutdown()

        usage.description = "Make sure to check that both GPU and Memory Utilization are 0 before running a task.\n\n ✅ Indicates free GPU.\n ❌ Indicates GPU being used, do not pick this GPU to run your script.\n\n" + status
        
        await self.bot.send_message(ctx.message.channel, embed=usage)

    def shutdown(self):
        nvmlShutdown()
        

import discord
from discord.ext import commands, tasks

import sys, traceback, time, os





class SlaveBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(command_prefix='slave.', intents=intents, description='EleSlave - A submissive subject of Elephantic Enslaver')


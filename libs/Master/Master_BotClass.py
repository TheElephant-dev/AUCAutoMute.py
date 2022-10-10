import discord
from discord.ext import commands

import sys, traceback, time, os


class MasterEnslaverBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(command_prefix='master.', intents=intents, description='EleEnslaver - A re-write of MinElebot')

    async def setup_hook(self) -> None: # Presistent views
        # self.add_view(PersistentView())
        pass
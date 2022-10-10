import discord
from discord.ext import tasks, commands


import zmq
from .HandleMasterOrders import HandleMessage, HandleOrder
import re

from libs.General.Utils.ExternalLibRefunc.time.TimeTranslations import TimeStampString

class CommandListening(commands.Cog):
    def __init__(self, bot: commands.Bot, botID: int):
        self.bot = bot
        self.Port = botID
        self.Address = f"tcp://10.100.102.75:111{self.Port}"

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.setsockopt(zmq.RCVTIMEO, 500) #Timeout after 1.6 Seconds
        self.socket.bind(self.Address)
        print(f"    [{TimeStampString(Full=True)}] - SERVER: I am ready to listen on {self.Address} and...")

        self.StartListening.start()



    @tasks.loop(seconds=0.1)
    async def StartListening(self):
        # print(f"     SERVER: I am Listening on {self.Address} and...")

        #  Wait for next request from client
        try:
            RecvMessage = self.socket.recv()
            # print(f'         I have Recieved a new Order, "{order}"')
        except Exception as E:
            if str(E) == 'Resource temporarily unavailable':
                pass
            else:
                print(f'  ERROR AT WaitForOrders>CommandListening>StartListening>recv:\n    {E}')
        try:
            await HandleMessage(self.bot, RecvMessage.decode('utf-8'), self.socket)
        except Exception as E2:
            if str(E2) == 'BREAKOperation cannot be accomplished in current state':
                print(f'  ERROR AT WaitForOrders>CommandListening>StartListening>Handle:\n    {E2}')




import asyncio
from discord.ext import tasks, commands


from libs.Master.Networking.SendSlaveOrder import SendMessageToSlave
from libs.General.Utils.ExternalLibRefunc.time.TimeTranslations import TimeStampString
slavecount=0
Prev_slavecount = 0

AliveBotIDs = []

class TrackAliveBots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = bot.get_guild(1009915066402996307)
        self.slavecounter.start()

    @tasks.loop(seconds=10.0)
    async def slavecounter(self):
        c=0
        for member in self.guild.members:
            if 'ElephanticSlave_' in str(member):
                botID = str(member).split('_')[1].split('#')[0] # turns the DiscordName#1516 into a bot ID
                response = SendMessageToSlave(botID, 'CheckAlive')
                if response[0] == 'Y':
                    if int(botID) not in AliveBotIDs:
                        AliveBotIDs.append(int(botID))
                else:
                    if int(botID) in AliveBotIDs:
                        AliveBotIDs.remove(int(botID))
                    #bot not alive
                    # print(f'BotAlive checked alive state of {member} and got {response}')
                    pass

        global slavecount
        global Prev_slavecount
        if len(AliveBotIDs)!=slavecount:
            AliveBotIDs.sort()
            # print(f'Alive slave count has changed from {slavecount} to {len(AliveBotIDs)}!   -   {AliveBotIDs}')
        slavecount = len(AliveBotIDs)


        AliveBotString = f' [{TimeStampString(Full=True)}]     - Finished checking for alive bot count'
        if slavecount != 0:
            AliveBotString+=f', from {Prev_slavecount} to {slavecount} bots alive.\n                              - Alive Bot IDs are: {AliveBotIDs}'
        else:
            AliveBotString +=f'\n... all slaves dead.'

        # check if alive bot count changed.


        if slavecount != Prev_slavecount:
            print(AliveBotString)
            Prev_slavecount = slavecount


def GetAliveBotIDs():
    return AliveBotIDs

# def GetAliveSlaveCount():
#         return slavecount
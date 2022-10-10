
import discord
from discord.ext import commands, tasks

import json
import zmq
import time
import random
import asyncio
import datetime

from libs.Master.Networking.SendSlaveOrder import SendMessageToSlave
from libs.Master.Networking.keepTrackOfAliveBotCount import GetAliveBotIDs

from libs.General.Utils.ExternalLibRefunc.time.TimeTranslations import TimeStampString



CheckDelayMiliseconds = 1000
def askForAUCUpdate():
    # print(f'    requesting and update from CASO...')

    port = '12345'
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.RCVTIMEO, CheckDelayMiliseconds) #Timeout after 0.5 Seconds
    Address = f"tcp://10.100.102.25:{port}"
    # print(f' [{TimeStampString(Full=True)}] - Checking for AUCupdates on \t {Address} ... \t ', end='')
    socket.connect(Address)
    socket.send_string("GetUpdate")
    responseFromAUCUpdate = 'MissingresponseFromAUCUpdateResponse'

    try:
        responseFromAUCUpdate = socket.recv().decode('utf8')
        # print(f'     AUCUpdate responded with: "{responseFromAUCUpdate}"')

    except Exception as E:
        if str(E) == 'Resource temporarily unavailable':
            pass
        else:
            print(f'  --# Error in sending AskForAUCUpdate("HGetUpdate") to AUCUpdate with Error:\n{E}\n\n')
            responseFromAUCUpdate = f'AskForAUCUPdaete Errored upon responding.'

    socket.linger = 0
    context.destroy()
    return responseFromAUCUpdate





def GenerateDeadStateStateString(Mode, DeadStates):
    String = '\nIf the bot properly detected everyone.\n**It should have done the following actions:**\n'
    x=0
    if Mode in 'Tasks Meeting':


        if Mode in 'Tasks ':
            AliveSuffix = 'thus were **Muted** and **Deafened**'
            DeadSuffix = 'thus were **Unmuted** and **Undeafened**'

        elif Mode in 'Meeting':
            AliveSuffix = 'thus were **Unmuted** and **Undeafened**'
            DeadSuffix = 'thus were **Muted**'


        for Player in DeadStates.keys():
            if DeadStates[Player]: # if the player is dead
                x+=1
                String+=f'    - {x}.**{Player}** is **dead** {DeadSuffix}.\n'

            else:
                x+=1
                String+=f'    - {x}.**{Player}** is **alive** {AliveSuffix}.\n'


    else:
        for Player in DeadStates.keys():
            x += 1
            String += f'    - {x}.**{Player}** was **Unmuted** and **Undeafened**.\n'

    return String





async def CommitLobbyActions(bot, Mode: str, DeadStates: dict):
    try:
        guild = bot.get_guild(1009915066402996307) or None
    except:
        print(f'could not find guild')
        return


    try:
        Elephant = guild.get_member(134156783450062848) or None
    except:
        print(f'could not find Elephant Member')
        return


    try:
        channel = Elephant.voice.channel or None
    except:
        print(f"could not find Elephant's channel.")
        return


    SlaveCommands=[]
    CnlMembs = channel.members
    LogChannelMessage = f'**When Entering** ***{Mode}*** **Mode in <#{channel.id}>:**\n\n'
    LogChannelMessageDebug = '\n\n\n ***DEBUG:***\n'


    # Try to match up ingame names with discord tags or discord nicknames as ign_dis_link.
    ign_dis_link = []
    for member in CnlMembs:
        foundingame = False
        memberDeadState = None
        for ign in DeadStates.keys():
            if ign in str(member.nick) or ign in str(member):
                ign_dis_link.append([member, ign])
                foundingame = True
                break
        if foundingame == False:
            print(f'Failed to find {member} inside the game. setting them as "unknown IGN"')
            ign_dis_link.append([member, 'unknown IGN'])


    # print the game state recieved from AUC
    print(f'\n#####################################')
    print(f'Getting The Following {Mode} Update:')
    for playerD in ign_dis_link:
        print(f'    > {str(playerD[0])}\{str(playerD[0].nick)} is "{playerD[1]}"')
    print(f'#####################################\n')

    # for each player pair ign_dis_link Ex:[DiscordName, IngameName],  generate a command to set their state.
    for playerD in ign_dis_link:
        if 'unknown' in playerD[1]: # if no ingame name was found, skip!(leave them at their current state.)
            continue
        memberDeadState = DeadStates[playerD[1]]
        Mute=0
        Deafen=0
        if Mode == 'Tasks':
                if memberDeadState:  # if the member is dead
                    Mute=0
                    Deafen=0
                else: # if member is alive
                    Mute=1
                    Deafen=1

        elif Mode == "Meeting":
            if memberDeadState:  # if the member is dead
                Mute = 1
                Deafen = 0
            else:
                Mute=0
                Deafen=0

            if Mode in ['MainMenu', 'Lobby', 'GameOver']:
                Mute = 0
                Deafen = 0
                # await member.edit(mute=False, deafen=False)
                # UNMUTE AND UNDEAFEN THIS MEMBER

        if memberDeadState != 'Missing':
            SlaveCommands.append(f'{guild.id}|{channel.id}|Voice_User={playerD[0].id}_Mute={Mute}_Deafen={Deafen}'
                                 f'|resason: {playerD[1]}\{playerD[0]}Dead={memberDeadState} when Entering {Mode} Mode|')
            LogChannelMessageDebug += f'   - Mute={bool(Mute)} \t Deafen={bool(Deafen)} \t <@{member.id}> \n'
    LogChannelMessageDebug+='\n'


    print(f' [{TimeStampString(Full=True)}] - Generated all possible Slave Commands!')
    for commmand in SlaveCommands: # send each command to a random alive bot.
        confirmedbybot = False
        fc=0


        while confirmedbybot == False: # keep sending that command to bots untill you have a bot confirmed he got the command.
            fc+=1
            try:
                AliveBots = GetAliveBotIDs()
                x = random.choice(AliveBots)
                # print(f' [{TimeStampString(Full=True)}]   - Sending Command to Bot #{x}: "{commmand}"')
                print(f' [{TimeStampString(Full=True)}]   - Sending Command to Bot #{x}: "SHORTENED COMMAND"')

                # get a response from the slave and store it.
                responseFromSlave =SendMessageToSlave(str(x), commmand)
                if 'rder received' in responseFromSlave:
                    confirmedbybot = True


            # Handle "No slave bots found"
            except Exception as E:
                if 'list index out of range' in str(E):
                    print(f'  - Error Sending a command. no alive bots found.{AliveBots} defaulting to bot #99.')

            # Handle retrying to send the command after failing for any reason
            if fc > 3 and fc < 10:
                print(f'Failed {fc} times to send to bot #{x} command:\n{commmand}'
                      f'\nAs a result, i will wait a second before trying again.')
                await asyncio.sleep(1)
            else:
                print(f'   - Failed sending the command 10 times. to prevent an endless loop i stopped trying!')
                break


    # log who _Missing_ in discord
    for ign in DeadStates.keys():
        ignF = False
        for member in CnlMembs:
            if ign in str(member.nick) or ign in str(member):
                ignF=True
        if ignF == False:
            LogChannelMessageDebug += f' - **{ign}** \t _Missing_ \t  in **discord**.\n'
    LogChannelMessageDebug += '\n'

    # log who _Missing_ in game
    for member in CnlMembs:
        idisF = False
        for ign in DeadStates.keys():
            if ign in str(member.nick) or ign in str(member):
                idisF=True
        if idisF == False:
            LogChannelMessageDebug += f' - **{member}** \t _Missing_ \t  in **game**.\n'
    LogChannelMessageDebug += '\n'

    print(f' [{TimeStampString(Full=True)}] - Sending the log message..')




    ## SEND THE LOG MESSAGE
    logchannel = bot.get_guild(1009915066402996307).get_channel(1019270766216351804)
    embed = discord.Embed(title=f"AutoMuteLog - {TimeStampString(Full=True)}",
            description=LogChannelMessage + GenerateDeadStateStateString(Mode, DeadStates) + LogChannelMessageDebug,
            color=0x00ff00)


    file = discord.File(f"./Assets/Modes/{Mode}.png", filename="CurrentMode.png")
    embed.set_thumbnail(url="attachment://CurrentMode.png")
    await logchannel.send(file=file, embed=embed)











class CheckForAUCupdates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.CheckGetAUCupdate.start()

    @tasks.loop(seconds=CheckDelayMiliseconds/1000)
    async def CheckGetAUCupdate(self):
        # print(f'requesting game update...')
        response = askForAUCUpdate()
        if response != 'MissingresponseFromAUCUpdateResponse':
            DATA = json.loads(response)
            Mode = DATA["Mode"]
            Update = DATA["Update"]
            await CommitLobbyActions(self.bot, Mode, Update)







import re
from libs.General.Utils.ExternalLibRefunc.time.TimeTranslations import TimeStampString

async def HandleMessage(bot, Message, socket): #ORDER FORMAT:      "{PORTCONFIRM}|{OrderType}|{GuildID}|{ChannelID|}|{Action>ActParams}|{Misc}"
    if Message.split('|')[0] == 'CheckAlive':
        # print('           - Master was asking if im still alive...telling em im alive')

        #  Send reply back to client
        socket.send_string(f'Yes im alive.')
    else:

        # check if an order was found
        orderfinder = re.findall(re.compile(r'[0-9]{18,20}\|[0-9]{18,20}\|.*?\|.*?\|'), Message)
        if len(orderfinder) != 0:
            socket.send_string(f'Order received.')
            for order in orderfinder:
                await HandleOrder(bot, order)








async def HandleOrder(bot, order):

    # print(f'Attempting to apply Order: "{order}"')
    O=order.split('|')

    # guild = bot.get_guild(int(O[0]))
    # channel = bot.get_channel(int(O[1]))
    # member = guild.get_member(MemberID)
    if 'Voice' in O[2]:
        # print('  - master told me to do a voice action!')
        A = O[2].split('_')
        # for x in A:
        #     print(f'  {x}')
        MemberID = int(A[1].split('=')[1])
        Mute = bool(int(A[2].split('=')[1]))
        Deafen = bool(int(A[3].split('=')[1]))
        # print(f'MemberID     {MemberID} of type({type(MemberID)})')
        # print(f'Mute     {Mute} of type({type(Mute)})')
        # print(f'Deafen    {Deafen} of type({type(Deafen)})')

        guild = bot.get_guild(int(O[0]))
        member = guild.get_member(MemberID)
        print(f'[{TimeStampString(Full=True)}]    - Mute.{bool(Mute)} and Deafen.{bool(Deafen)} {member}{str(member.nick) + "."}')
        await member.edit(mute=Mute, deafen=Deafen)
    else:
        print(f'Order: "{order}" is an unknown order type.')

    return True












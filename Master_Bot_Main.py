import discord
from libs.Master.Master_BotClass import MasterEnslaverBot
from libs.Master.Networking.keepTrackOfAliveBotCount import TrackAliveBots, GetAliveBotIDs
from libs.Master.Networking.SendSlaveOrder import SendMessageToSlave

from libs.General.Utils.DiscordPy.auth.Tokens import GetMasterToken
from libs.General.Utils.DiscordPy.Debugging.Debug import testString


from libs.Master.Networking.CheckgameUpdates import CheckForAUCupdates
bot = MasterEnslaverBot()


@bot.command()
async def MsgSlave(ctx, botID, *, message):
    # print(f'i just got a MsgSlave command')
    response = SendMessageToSlave(botID, message)
    # print(f'bot#{botID} responded to me with: {response}')
    await ctx.send(f'bot#{botID} responded to me with: {response}')

@bot.command()
async def test(ctx, *, text = ''):
    await testString(ctx, f'   {bot.user}.DEBUG:{text}')





@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})\n---------------------------------------------------------------')
    #change_presence
    await bot.change_presence(status=discord.Status.do_not_disturb,
                              activity=discord.Game("Enforcing Elephant's Peace"))

    #add command listening cog
    bot.add_cog(CheckForAUCupdates(bot))
    bot.add_cog(TrackAliveBots(bot))

bot.run(GetMasterToken(), reconnect=True)



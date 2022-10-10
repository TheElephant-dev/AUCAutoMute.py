import discord
from discord.ext import tasks, commands


from libs.Slave.Slave_Botclass import SlaveBot
from libs.Slave.Networking.WaitForOrders import CommandListening

from libs.General.Utils.DiscordPy.auth.Tokens import GetSlaveToken
from libs.General.Utils.DiscordPy.Debugging.Debug import testString


SlaveID = input('SlaveID?: ')
# SlaveID = '0'
bot = SlaveBot()






@bot.command()
async def test(ctx, *, TEXT = ' test'):
    await testString(ctx, f'   {bot.user}.DEBUG:{TEXT}')




@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})\n---------------------------------------------------------------')
    #change_presence
    await bot.change_presence(status=discord.Status.do_not_disturb,
                              activity=discord.Game("with innocent lives..."))

    #add command listening cog
    bot.add_cog(CommandListening(bot, SlaveID))


bot.run(GetSlaveToken(SlaveID), reconnect=True)



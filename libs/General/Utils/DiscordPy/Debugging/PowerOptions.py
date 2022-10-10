
from ...ExternalLibRefunc.time.TimeTranslations import TimeStampString as TS
from ..auth.Tokens import GetSlaveToken, GetMasterToken
def turnon(ID: str):
    if ID == 'M':
        bot.run(GetMasterToken())
    elif type(int(ID) == 'int':
        bot.run(Ge)

    bot.run('MTAwOTE3MTkyNDcxNjM1OTY4MQ.Gj8sW1.2A92VQfTkwS2UUt1HsPYo_hyHoge43fmzyuQMg')  # MiniEleBot



async def shutdown(ctx):
    try:
        await ctx.send(f'**Shutting myself down** at {TS(Full=True)}\n'
                       f'As requested by <@{ctx.message.author.id}>\n'
                       f'Saving Shutdown request in local log files..')
        await ctx.bot.close()
        return -2
    except Exception as E:
        await ctx.send(f'shutdownError: "{E}"')


async def restart(ctx):
    try:
        await ctx.send(f'**Restarting** myself at {TS(Full=True)}\n'
                       f'As requested by <@{ctx.message.author.id}>\n'
                       f'Saving Restart request in local log files..')
        await ctx.bot.close()
        return -3
    except Exception as E:
        await ctx.send(f'restartError: "{E}"')



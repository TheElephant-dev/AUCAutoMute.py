import time
import os
def GetMasterToken():
    return 'PUT THE MASTER TOKEN HERE'

def GetSlaveToken(ID):
    # print(os.path.abspath(__file__))
    with open(f'{str(os.getcwd())}/libs/General/Utils/DiscordPy/auth/SlaveTokens.txt', 'r') as stFIle:
        Lines = stFIle.readlines()
        Token = Lines[int(ID)][:-1]
        return Token
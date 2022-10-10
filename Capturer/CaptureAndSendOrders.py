import zmq
import json
import asyncio
import websockets
from time import sleep







def SendDataToMainBot(Data):


    Address = f"tcp://127.0.0.0:12345"

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.setsockopt(zmq.RCVTIMEO, 100)  # Timeout after 0.1 Seconds
    socket.bind(Address)
    print(f" [{TimeStampString(Full=True)}] -  SERVER: I am ready to report back data on {Address} upon request from Master bot...")

    #  Wait for next request from client
    RecvMessage=''
    try:
        RecvMessage = socket.recv()
    except Exception as E:
        if str(E) == 'Resource temporarily unavailable':
            pass
        else:
            print(f'  ERROR AT Capturer>CaptureAndSendOrders>in getting the gae update request:\n    {E}')
    if 'GetUpdate' in str(RecvMessage):
        try:
            # print(f'Data = {Data}\n   of type({type(Data)})')
            socket.send(Data)
        except Exception as E2:
            print(f'  ERROR AT Capturer>CaptureAndSendOrders>in sending the update back:\n    {E2}')
































DeadState = {'Elephant': False}

def TurnDataStringIntoVars(DataString):
    # print(f'#######################################\n#######################################\nTurnDataStringIntoVars({DataString}')
    # print(f'####################################### get event string and turn it into usable data')


    DATA = json.loads(DataString)
    # print(f'DataString: {DATA}') # print contents of message itself.
    # for key in DATA.keys():
    #     print(f'  - DATA["{key}"] = {DATA[key]}')
        

    EventData = json.loads(DATA['EventData'])
    # print(f'EventData:\n{EventData}') # print contents of the event within the message.
    # for key in EventData.keys():
    #     print(f'  - EventData["{key}"] = {EventData[key]}')


    # print(f'####################################### filter usable data filter it and make it usable by the main bot')

    global DeadState
    def PrintStateOfDeadState():
        alivePs = []
        deadPs = []
        for key in DeadState.keys():
            if DeadState[key]:
                deadPs.append(key)
            else:
                alivePs.append(key)
        print('#############################\nAlive Players:')
        for x in alivePs:
            print(f'   - {x}')
        print('\n')

        print('Dead Players:')
        for x in deadPs:
            print(f'   - {x}')
        print('#############################\n')

    if "Action" in EventData:  ## if the event is a new key
        # print('\na player update!\n\n\n')

        # for key in EventData.keys():
        #     print(f'  - EventData["{key}"] = {EventData[key]}')
        Pname = EventData['Name']

        if EventData["Action"] not in [0, 1, 2, 3, 5, 6]:
            print(f' - = - EventData["Action"]={EventData["Action"]} - = -')


        if EventData["Action"] == 0: # player joined
            # print(f'{Pname} Joined.')
            DeadState[Pname] = False

        elif EventData["Action"] == 1:  # player left
            # print(f'     {Pname} Left.')
            if Pname in DeadState: # if player exists in DeadState dict
                del DeadState[Pname] # remove player from DeateState dict

        elif EventData["Action"] == 2:  # player left
            # print(f'     {Pname} Died.')
            DeadState[Pname] = True

        elif EventData["Action"] == 3:  # player changed color
            # print(f'         {Pname} changed their color.')
            pass

        elif EventData["Action"] == 5:  # player disconnected.
            # print(f'             {Pname} disconnected from the lobby.')
            if Pname in DeadState:  # if player exists in DeadState dict
                del DeadState[Pname]  # remove player from DeateState dict

        elif EventData["Action"] == 6:  # player voted out.
            # print(f'             {Pname} voted out of the game.')
            DeadState[Pname] = True



        # if EventData['Disconnected'] == True: # if player disconnected
        #     if Pname in DeadState: # if player exists in DeadState dict
        #         del DeadState[Pname] # remove player from DeateState dict





    elif "NewState" in EventData:  ## if the event is a new key
        # PrintStateOfDeadState()
        Mode = 'unknown mode'

        if EventData["NewState"] == 0:  # Lobby
            Mode = 'Lobby'
            DeadState = {'Elephant': False}

        elif EventData["NewState"] == 1:  # Tasks
            Mode = 'Tasks'

        elif EventData["NewState"] == 2:  # Meeting
            Mode = 'Meeting'

        elif EventData["NewState"] == 3:  # MainMenu
            Mode = 'MainMenu'
            DeadState = {'Elephant': False}

        elif EventData["NewState"] == 4:  # MainMenu
            Mode = 'GameOver'
            DeadState = {'Elephant': False}

        print(f'Detected a new state #{EventData["NewState"]}, Entered {Mode} mode!\n'
              f'   - With data:')
        for key in DeadState.keys():
            print(f'    - {key} Dead: {DeadState[key]}')

        # pass the data to master bot
        SendableData = {}
        SendableData['Mode'] = Mode
        SendableData['Update'] = DeadState
        SendDataToMainBot(bytes(json.dumps(SendableData), encoding='utf8'))















uri = "ws://localhost:42069/api"
async def WaitForData():
    try:
        async with websockets.connect(uri) as websocket:
            try:
                async for message in websocket:
                    TurnDataStringIntoVars(message)
            except Exception as E:
                if "no close frame received or sent" in str(E):
                    print(f'   - Error in reading data from game. maybe Captuerer Crashed?\n{E}')
    except Exception as E:
        if "The remote computer refused the network connection" in str(E):
            print(f'   - Error in reading data from game. maybe Captuerer wasnt opened when CASO ran?\n{E}')

while True:
    asyncio.get_event_loop().run_until_complete(WaitForData())
    asyncio.sleep(1)













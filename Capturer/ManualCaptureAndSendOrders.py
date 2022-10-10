import websockets, asyncio, json, zmq
from time import sleep







def SendDataToMainBot(Data):


    Address = f"tcp://10.100.102.25:12345"

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    # socket.setsockopt(zmq.RCVTIMEO, 3000)  # Timeout after 3000 Seconds
    socket.bind(Address)
    print(f"     SERVER: I am ready to send back on {Address} and...")

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







logFilePath = r'C:\Users\theel\AppData\Roaming\AmongUsCapture\logs\latest.log'
ModeTranslator = {0:'Lobby',
                  1:'Tasks',
                  2:'Meeting',
                  3:'MainMenu',
                  4:'GameOver'}







def DetectGameUpdateStateFromLogsFile(DataString):
    DeadState = {}

    EventData = json.loads(json.loads(DataString)['EventData'])
    if "NewState" in EventData:
        print('\n\n\n\n\n\n\n')
        print(f'Detected {EventData["NewState"]} state update')

        if EventData["NewState"] == 'LOBBY':  # Lobby
            DeadState = {}

        elif EventData["NewState"] == 'TASKS':  # Tasks
            pass

        elif EventData["NewState"] == 'DISCUSSION':  # Meeting
            pass

        elif EventData["NewState"] == 'MENU':  # MainMenu
            DeadState = {}

        elif EventData["NewState"] == 'ENDED':  # Game Over
            DeadState = {}

        sleep(1)
        ##### Filter the logs to the latest update
        logs = []
        with open(logFilePath, 'r', encoding="utf-8") as logFile:
            scnNS = False
            LogLines = logFile.readlines()
            for x in range(len(LogLines)):
                y = x*-1
                LL = LogLines[y][:-1]
                # print(f'line #{y} = {LL}')
                if 'Action' in LL:
                    logs.append(LL[45:])

                # look in the last 200 entries
                if x==200:
                    break


                # try to find latest update
                # if 'NewState' in LL:
                #     if scnNS:
                #         break
                #     scnNS = True

        ##### Filter the logs to remove stamps
        logs.reverse()
        for log in logs:
            log = json.loads(log)
            # print(f'log = {log} of type({type(log)})')

            Pname = log['Name']
            ###
            if log["Action"] not in ['Joined', 'Left', 'Died', 'ChangedColor', 'Disconnected', 'Exiled']:
                print(f' - unknown log["Action"]=   "{log["Action"]}"')

            if log["Action"] == 'Joined':  # player joined
                # print(f'  - {Pname} Joined.')
                DeadState[Pname] = False

            elif log["Action"] == 'Left':  # player left
                # print(f'  - {Pname} Left.')
                if Pname in DeadState:  # if player exists in DeadState dict
                    del DeadState[Pname]  # remove player from DeateState dict

            elif log["Action"] == 'Died':  # player Died
                # print(f'     {Pname} Died.')
                DeadState[Pname] = True

            elif log["Action"] == 'ChangedColor':  # player changed color
                # print(f'     - {Pname} changed their color.')
                pass

            elif log["Action"] == 'Disconnected':  # player disconnected.
                # print(f'  - {Pname} disconnected from the lobby.')
                if Pname in DeadState:  # if player exists in DeadState dict
                    del DeadState[Pname]  # remove player from DeateState dict

            elif log["Action"] == 'Exiled':  # player voted out.
                # print(f'   - {Pname} voted out of the game.')
                DeadState[Pname] = True


        print(f'Current State should be:')

        x=0
        for k in DeadState.keys():
            x += 1
            print(f'  -  {x}.{k} Dead/{DeadState[k]}')



        print(f'UPDATE THE MAIN BOT')
        SendableData = {}
        # SendableData['Mode'] = EventData['NewState']
        SendableData['Mode'] = ModeTranslator[EventData['NewState']]
        SendableData['Update'] = DeadState
        SendDataToMainBot(bytes(json.dumps(SendableData), encoding='utf8'))










uri = "ws://localhost:42069/api"
async def WaitForData():
    async with websockets.connect(uri) as websocket:
            async for message in websocket:
                DetectGameUpdateStateFromLogsFile(message)
        # try:
        #     async for message in websocket:
        #         DetectGameUpdateStateFromLogsFile(message)
        # except Exception as E:
        #     print(f'### ERROR ### error in reading game update data!\n{E}\n\n')

while True:
    try:
        asyncio.get_event_loop().run_until_complete(WaitForData())
        print(' > Crashed! restarting...')
    except Exception as E:
        print('############################################################################')
        if 'The remote computer refused the network connection' in str(E):
            print(f'Manual AUC Checker cannot run due to AUCapture likely not online')
        else:
            print(f'Manual AUC Checker crahsed due to:\n    {E}')
        print('############################################################################')




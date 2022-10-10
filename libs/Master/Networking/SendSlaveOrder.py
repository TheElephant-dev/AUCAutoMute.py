import zmq
from libs.General.Utils.ExternalLibRefunc.time.TimeTranslations import TimeStampString

def SendMessageToSlave(botID, Message):

    port = '111' + botID
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.RCVTIMEO, 10) #Timeout after 1.6 Seconds
    Address = f"tcp://10.100.102.75:{port}"
    if Message != 'CheckAlive':
        print(f' [{TimeStampString(Full=True)}]   - CLIENT: trying to send message to \t {Address}')
    socket.connect(Address)
    socket.send_string(f"{Message}")
    responseFromSlave = 'MissingresponseFromSlaveResponse'

    try:
        responseFromSlave = socket.recv().decode('ascii')
        # print(f'     Slave #{botID} responded with: "{responseFromSlave}"')

        # if port == portconfirm:
        #     print(f'port confirmed to match between {Address} and {portconfirm}')

    except Exception as E:
        if str(E) == "Resource temporarily unavailable":
            if Message != 'CheckAlive':
                print(f'  - {E}\n       -- Error in sending command("{Message}") to bot #{botID} with Error:\n       bot #{botID} did not respond.\n\n')
            responseFromSlave = f'bot #{botID} did not respond.'

        else:
            print(f'  -- Error in sending command("{Message}") to bot #{botID} with Error:\n{E}\n\n')
            responseFromSlave = f'bot #{botID} Erroed upon responding.'

    socket.linger = 0
    context.destroy()
    return responseFromSlave



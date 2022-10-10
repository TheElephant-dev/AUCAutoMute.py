import re

order = r'^master.MsgSlave 0 111946162697732126|806870725209096202|Voice_Mute=0_Deaden=1|MISCDATA|' \
         r'222946162697732126|806870725209096202|Voice_Mute=0_Deaden=1|MISCDATA|'

for x in re.findall(re.compile(r'[0-9]{18,20}\|[0-9]{18,20}\|.*?\|.*?\|'), order):
    print(x, type(x))

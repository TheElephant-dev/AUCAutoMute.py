import datetime

def TimeStampString(Str='%H:%M:%S', Full=False):
    if Full:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return datetime.datetime.now().strftime(Str)


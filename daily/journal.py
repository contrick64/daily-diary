import datetime

class Journal():
    def __init__(self,moodint:int,moods:list,entry:str):
        self.timestamp = datetime.now()
        self.moodint = moodint
        self.moods = moods
        self.entry = entry
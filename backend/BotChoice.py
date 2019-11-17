from Stacey.aiml.script.bot import *
from Noob import noobBot
from Mitsuku import mitsukuBot
import random

class randBot():

    def __init__(self):
        self.mode = random.randint(1,2)#4
        print(self.mode)
        if self.mode == 1:# Noob
            self.bot = noobBot()
            pass
        elif self.mode == 2: # Mitsuku
            self.bot = mitsukuBot()
            pass
        elif self.mode == 3:# Stacey
            self.bot = 1
            pass
        else: # Standard
            self.bot = 2
            pass
        return
        
    def sendMessage(self, message):
        return self.bot.sendMessage(message)

aa = randBot()
print(aa.bot)
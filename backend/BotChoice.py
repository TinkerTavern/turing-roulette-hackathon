from Stacey.aiml.script.bot import smarter()
from Noob import noobBot
from Mitsuku import mitsukuBot
import random

class randBot():

    bot = None

    def __init__(self):
        self.mode = 2#4
        print(self.mode)
        if self.mode == 1:# Noob
            self.bot = noobBot()
            pass
        elif self.mode == 2: # Mitsuku
            self.bot = mitsukuBot()
            pass
        elif self.mode == 3:# Stacey
            self.bot = smarter("")
            pass
        else: # Standard
            self.bot = smarter("standard")
            pass
        return
        
    def sendMessage(self, message):
        return self.bot.sendMessage(message)

aa = randBot()
print(aa.bot)
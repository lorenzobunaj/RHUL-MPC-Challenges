import math
import os

class Party1:
    def __init__(self, s):
        self.s = s

    def generatePositions(self):
        positions = []
        for p in range(len(self.s)):
            positions.append(round(pow(math.sin(p * math.pi / 2), 2)))

        return positions


    def generateMessages(self):
        messages = []
        positions = self.generatePositions()

        for i in range(0, len(self.s)):
            messages.append(
                [self.s[i].encode(), os.urandom(1)] if positions[i] == 1
                else [os.urandom(1), self.s[i].encode()])
            
        return messages

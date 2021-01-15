import Script
import Item
import abc

class Command():
    def __init__(self, aLine, aListOfInstructions,aBranch):
        self.line = aLine
        self.instructions = aListOfInstructions
        self.branch = aBranch

    @abc.abstractmethod
    def execute(self):
        print(self.line)
        for instruction in self.instructions:
            getattr(instruction, instruction[0])(instruction[1:])
        return self.branch
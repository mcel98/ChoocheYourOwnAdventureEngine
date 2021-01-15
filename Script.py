import Command
import Subject
import threading
import queue


class Script:
    def __init__(self,actor,stageInstance,map):
        self.stageInstance = stageInstance
        self.parentmap = map
        self.actor = actor
        self.lines = [{}]
        self.lines[self.actor.identify()]['idleBehavior'] = {}
        self.currLine = ''
        self.playTurn = threading.Semaphore(value=1)

    def commandDefinition(self,commandName, subject, line, actions ,aBranch):
        self.lines[subject.identify()][commandName] = Command.Command(line,actions,aBranch)

    def idleBehavior(self):
        threading.Thread(target=self.doIdleBehavior, args=())

    def play(self,subject,line):
        if self.currLine != 'endplay':
            self.currLine = line
            self.playTurn.acquire(blocking=True)
            subjectLine = self.lines[subject.identify()][line].execute() #dialogue / monologue / narration
            subject.interactWithSubject(self,subjectLine)
            self.playTurn.release()


    def stagePlay(self):
        return self.stageInstance

    def exitStage(self):
        self.actor.SetMap(self.parentmap)

    def doIdleBehavior(self):
        self.playTurn.acquire(blocking=True)
        while self.currLine == 'idleBehavior':
            self.playTurn.release()
            self.lines[self.actor.identify()]['idleBehavior'].execute()
            self.playTurn.acquire(blocking=True)

        self.playTurn.release()


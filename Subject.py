from abc import ABC, abstractmethod
from Script import Script
import map

class Status:
    def __init__(self):
        return


class Subject():

    def __init__(self,id, hp, inventory,position,map,stage, facing):
        self.id = id
        self.life = hp
        self.maxHP = hp
        self.inventory = inventory
        self.position = position
        self.script = Script(self, stage, map)
        self.status = Status()
        self.map = map
        self.facing = facing
        map.putSubjectAt(position,facing, self)

    def identify(self):
        return id

    def updatePosition(self, coordinates):
        self.position = coordinates

    def move(self, direction):
        if self.status != 'fighting':
            self.map.putSubjectAt(direction * self.facing, self)

    def posistion(self):
        return self.position

    def SetMap(self,map):
        self.map = map

    def hurt(self,damage,item):
        itemMod = item.attackModifier(self)
        self.life -= (damage + itemMod)
        if self.life <= 0:
            self.die()

    def heal(self, hp):
        new_hp = self.life + hp
        if new_hp <= self.maxHP and self.life > 0:
            self.life = new_hp

    def revive(self, hp):
        if  self.life <= 0:
            self.life = 1

    def die(self):
        if self.life > 0:
            self.life = 0
            self.script.play(self,'endplay')

    def startFight(self):
        self.status = 'fighting'
        self.map = self.script.stagePlay()

    def interactWithSubject(self,subject,line):
        command = line
        if subject is None:
            while command != 'endplay':
                self.script.play(subject,command)
            self.script.exitStage()


class EnemyPhase:

    def __init__(self, enemy, attackPatternList):
        self.enemy = enemy
        self.combatPattern = attackPatternList

    def attackPattern(self):
        for action in self.combatPattern:
            getattr(self.enemy, action[0])(action[1:])


class Enemy(Subject):

    def __init__(self,id,hp,inventory,position,map,stage,aggroRadius, facing):
        super().__init__(id, hp, inventory,position,map,stage, facing)
        self.phase = EnemyPhase(self, [])
        self.fightHistory = []
        self.aggroRange = aggroRadius

    def addPhase(self, attackPatternList):
        self.phase = EnemyPhase(self,attackPatternList)

    def attack(self,damage, subject, item):
        subject.hurt(damage,item)


    def castSpell(self,aSpell,item,subject):
        aSpell.castOnSubject(item,subject)


    def useItem(self,item,subject):
        item.use(self)


    def checkForEnemy(self, fovDegree, range):
        subjectFound = self.map.traverse(self.position, fovDegree, range)
        self.interactWithSubject(subjectFound ,'attack')

class Player(Subject):
    def __init__(self,id,hp,inventory,position,facing,map,stage,aggroRadius):
        super().__init__(id, hp, inventory,position,map,stage,facing)
        self.phase = EnemyPhase(self, [])
        self.fightHistory = []
        self.aggroRange = aggroRadius

    def attack(self,damage, subject, item):
        subject.hurt(damage,item)

    def castSpell(self,aSpell,item,subject):
        aSpell.castOnSubject(item,subject)

    def useItem(self,item,subject):
        item.use(self)



class NPC(Subject):
     def __init__(self,id, hp, inventory,position,facing,map,stage):
        super().__init__(id, hp, inventory,position,map,stage,facing)

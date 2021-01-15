import Subject
import numpy as np

class map:
    def __init__(self, width, height):
        np.zeros((height,width))
        self.grid = [[None] * width] * height
        self.height = height
        self.width = width

    def putSubjectAt(self,direction, subject):
        currPosition = subject.position()
        self.grid[currPosition[0]][currPosition[1]] = None
        newPosition = (currPosition[0] + direction[0],currPosition[1] + direction[1])
        #TODO: chequear posicion por objectos en la grid y deteccion de enemigos
        self.grid[newPosition[0]][newPosition[1]] = subject

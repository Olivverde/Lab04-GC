import pygame
import random

class life(object):
    def __init__(self, screen):
        _, _, self.height, self.width = screen.get_rect()
        self.screen = screen
        self.alive = []
        self.dead_aux = []
        self.alive_aux = []
        self.dead = []
        self.state = True
        self.limits = []
        self.frames = []
        self.flag = False
        self.bgColor = (0,0,0)
        for i in range(150):
            self.alive.append(list((random.randint(0, self.width),random.randint(0, self.height))))

    def copy(self):
        self.prev_gen = self.screen.copy()

    def limitsDef(self,x,y):
        '''
        11x11 sensitivity area
        '''
        for i in range(-4,5):
            for j in range(-4,5):
                if not ((x+i > self.width) or (x+i < 0) or (y+j > self.height) or (y+j < 0)):
                    self.limits.append(list((x+i,y+j)))

    '''
    3x3 cell
    4 displays
    1 sensitivity threshold pixel
    '''
    def spaceship(self,x,y):
    
        choosenDisplay = random.randint(0, 3)
        color = (255,255,255)
        nonColor = self.bgColor

        frames = [
            (x-1,y+1), (x,y+1), (x+1,y+1),
            (x-1,y), (x,y), (x+1,y),
            (x-1,y-1),(x,y-1),(x+1,y-1)
            ]
        
        self.frames = frames
        try:
            if self.state:
                if choosenDisplay == 0:
                    pattern = [
                                color, nonColor, nonColor,
                                nonColor, color, color,
                                color, color, color
                            ]

                elif choosenDisplay == 1:
                    pattern = [
                                nonColor, color, nonColor,
                                nonColor, nonColor, color,
                                color, color, color
                            ]
                
                elif choosenDisplay == 2:
                    pattern = [
                                nonColor, nonColor, color,
                                color, nonColor, color,
                                nonColor, color, color
                            ]

                elif choosenDisplay == 3:
                    pattern = [
                                color, nonColor, color,
                                nonColor, color, color,
                                nonColor, color, nonColor
                            ]
            else:
                pattern = [
                            nonColor, nonColor, nonColor,
                            nonColor, nonColor, nonColor,
                            nonColor, nonColor, nonColor
                            ]


            for i in range(len(frames)):
                if not ((frames[i][0] > self.width) or (frames[i][0] < 0) or (frames[i][1] > self.height) or (frames[i][1] < 0)):
                    self.screen.set_at(frames[i],pattern[i])  
            
            
        except:
            pass



    def pixel(self,x,y):
        self.screen.set_at((x,y),(255,255,255))

    def clear(self):
        self.screen.fill((0,0,0))

    def printOut(self):

        for i in self.alive:

            localFlag = 0
            self.x = i[0]
            self.y = i[1]
            
            self.spaceship(self.x, self.y)

            newX = self.x + random.randint(-1, 1)
            newY = self.y + random.randint(-1, 1)

            while True:
                if self.state:
                    if not ((newX > self.width) or (newX < 0) or (newY > self.height) or (newY < 0)):
                        i[0] = newX
                        i[1] = newY
                        break
                        
                    else:
                        newX = self.x + random.randint(-1, 1)
                        newY = self.y + random.randint(-1, 1)
                else:
                    break

    def render(self):

        if len(self.dead) != 0:
            for i in self.dead:
                localFlag = 0
                self.x = i[0]
                self.y = i[1]
                self.limitsDef(self.x, self.y)
                for cell in self.alive:
                    if (cell in self.limits):
                        localFlag += 1
                if (localFlag == 3):
                    self.dead_aux.append(i)
        

        if self.flag:

            for cell in self.alive:
                localFlag = 0
                self.x = cell[0]
                self.y = cell[1]
                self.limitsDef(self.x, self.y)

                for alive_cell in self.alive:
                    if (alive_cell in self.limits) and (cell != alive_cell) and not(alive_cell in self.alive_aux):
                        localFlag += 1
                
                if (localFlag < 2) or (localFlag > 3):
                    self.alive_aux.append(cell)
                
            
            for aux_cell in self.alive_aux:
                self.dead.append(aux_cell)
                self.alive.remove(aux_cell) 
            self.alive_aux = []
            self.limits = []

        #self.printOut()

        for dead_cell in self.dead_aux:
            self.alive.append(dead_cell)
            self.dead.remove(dead_cell)
        self.dead_aux = []
        self.limits = []

        self.printOut()
        self.flag = True
    
pygame.init()
screen =pygame.display.set_mode((100,100))

r = life(screen)

while True:

    pygame.time.delay(100)
    r.copy()
    r.clear()
    r.render()
    pygame.display.flip()
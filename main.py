import math

import pygame

import random

class vector:
    def __init__(self,_x,_y,_dirx,_diry):
        self.x = _x
        self.y = _y
        self.dirx = _dirx
        self.diry = _diry
    def DrawVector(self,screen,k) -> None:
        pygame.draw.line(screen,(0,255,0),(self.x,self.y),(self.x+self.dirx*k,self.y+(self.diry*k)))
    def lenWithK(self,k):
        return math.sqrt((self.x+self.dirx*k-self.x)**2+(self.y+self.diry*k-self.y)**2)
    def DrawLine(self,screen,x,y):
        pygame.draw.line(screen,(0,255,0),(self.x,self.y),(x,y))
    def normalize(self,mousePos):
        # https://www.fundza.com/vectors/normalize/
        l = math.sqrt((mousePos[0]-self.x)**2+(mousePos[1]-self.y)**2)
        if l == 0:
            l = 0.001
        self.dirx = (mousePos[0]-self.x)/l
        self.diry = (mousePos[1]-self.y)/l
    def get_copy(self):
        return vector(self.x,self.y,self.dirx,self.diry)

class boundarie:
    def __init__(self,_x1,_y1,_x2,_y2) -> None:
        self.x1 = _x1
        self.y1 = _y1
        self.x2 = _x2
        self.y2 = _y2
    def DrawLine(self,screen):
        pygame.draw.line(screen,(255,255,255),(self.x1,self.y1),(self.x2,self.y2))

def checkCollision(ray,wall):
    x1 = ray.x
    y1 = ray.y
    x2 = ray.x + ray.dirx * 1000
    y2 = ray.y + ray.diry * 1000

    x3 = wall.x1
    y3 = wall.y1
    x4 = wall.x2
    y4 = wall.y2

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if (den == 0):
        return False,-1,-1
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
    if t >= 0 and t <= 1 and u >= 0 and u <= 1:
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return True,x,y
    else:
        return False,-1,-1

def distance(ray,tuple):
    return math.sqrt((tuple[0]-ray.x)**2+(tuple[1]-ray.y)**2)

pygame.init()
screen = pygame.display.set_mode([800, 800])
running = True
clock = pygame.time.Clock()
mousePos = pygame.mouse.get_pos()

rays = []
rays.append(vector(160,150,-1,0))
rays.append(vector(160,150,-1,1))
rays.append(vector(160,150,-1,-1))
rays.append(vector(160,150,0,0))
rays.append(vector(160,150,0,1))
rays.append(vector(160,150,0,-1))
rays.append(vector(160,150,1,0))
rays.append(vector(160,150,1,1))
rays.append(vector(160,150,1,-1))

walls = []
#b1 = boundarie(300,100,300,200)
#b2 = boundarie(100,100,300,100)
#b3 = boundarie(100,100,100,200)
for i in range(4):
    walls.append(boundarie(random.randint(0,800),random.randint(0,800),random.randint(0,800),random.randint(0,800)))

distmin = 9999

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   
        if event.type == pygame.MOUSEMOTION:
            mousePos = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                walls.clear()
                for i in range(4):
                    walls.append(boundarie(random.randint(0,800),random.randint(0,800),random.randint(0,800),random.randint(0,800)))


    screen.fill((0,0,0))


    #v1.normalize(mousePos)
    #v2.normalize(mousePos)

    for ray in rays:
        ray.x = mousePos[0]
        ray.y = mousePos[1]

    for ray in rays:
        ray.DrawVector(screen,0)
    
    for wall in walls:
        wall.DrawLine(screen)

    for ray in rays:
        closest = None
        record = 9999999999
        for wall in walls:
            a = checkCollision(ray,wall)
            if a[0] == True:
                d = distance(ray,(a[1],a[2]))
                if d < record:
                    record = d
                    closest = (a[1],a[2])
        if closest:
            ray.DrawLine(screen,closest[0],closest[1])
                

    pygame.display.flip()

pygame.quit()

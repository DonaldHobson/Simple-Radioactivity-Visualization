
while True:
    try:
        halflife=float(input("Enter halflife >>"))
        if 0.1<=halflife<=60:
            break
        else:
            print("Halflife must be between 0.1 and 60")
    except ValueError:
        print("Halflife must be a number")

import sys, pygame
import time,math,random

pygame.init()

width, height = 400, 600
size = width*2, height
speed = [2, 2]
black = 0, 0, 0
framerate=30
time_sleep=1/framerate
decay_ratio=halflife/time_sleep
screen = pygame.display.set_mode(size)


p=pygame.Surface([10,10])
pygame.draw.circle(p,(255,255,0),(5,5),5)

class P(pygame.sprite.Sprite):
    bbox=pygame.Rect(0,0,width,height)
    group=pygame.sprite.Group()
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=self.Img
        self.rect=self.Img.get_rect().copy()
        self.rect.center=(x,y)
        P.group.add(self)
        self.group.add(self)
class Photon(P):
    psz=5
    Img=pygame.Surface([psz*2]*2)
    Img.set_colorkey((0,0,0))
    pygame.draw.circle(Img,(255,255,0),(psz,psz),psz)
    group=pygame.sprite.Group()
    def __init__(self,x,y,a=None):
        if a is None:
            a=random.random()*2*math.pi
        P.__init__(self,x,y)
        self.pos=(x,y)
        v=5
        self.vel=(math.sin(a)*v,math.cos(a)*v)
    def update(self):
        self.pos=tuple(i+j for i,j in zip(self.pos,self.vel))
        self.rect.center=self.pos
        if not self.rect.colliderect(P.bbox):
            self.kill()
class Ratom(P):
    psz=5
    Img=pygame.Surface([psz*2]*2)
    Img.set_colorkey((0,0,0))
    pygame.draw.circle(Img,(255,255,255),(psz,psz),psz)
    group=pygame.sprite.Group()
    def __init__(self,x,y,a=random.random()*2*math.pi):
        P.__init__(self,x,y)
        self.pos=(x,y)
    def update(self):
        self.rect.center=tuple(i+random.randint(-1,1) for i in self.pos)
        if random.random()>0.5**(1/decay_ratio):
            Photon(*self.pos)
            Datom(*self.pos)
            self.kill()
class Datom(P):
    psz=4
    Img=pygame.Surface([psz*2]*2)
    Img.set_colorkey((0,0,0))
    pygame.draw.circle(Img,(128,128,128),(psz,psz),psz)
    group=pygame.sprite.Group()
    def __init__(self,x,y,a=random.random()*2*math.pi):
        P.__init__(self,x,y)
        self.pos=(x,y)
    def update(self):
        pass
        #self.rect.center=tuple(i+random.randint(-1,1) for i in self.pos)
class Graph(pygame.sprite.Sprite):
    group=pygame.sprite.Group()
    bbox=bbox=pygame.Rect(width,0,width,height)
    def __init__(self,colour=(255,0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.data=[]
        self.colour=colour
        self.max=0
        self.rm=0
    def upd(self,x):
        self.max=max(self.max,x)
        self.data.append(x)
        if len(self.data)>self.bbox.width:
            self.data=self.data[1:]
            self.rm+=1
    def draw(self,surface):
        pygame.draw.rect(surface,(255,)*3,self.bbox)
        if len(self.data)<2:
            return
        left=self.bbox.left
        right=self.bbox.right
        width=right-left
        data=self.data
        height=self.bbox.height
        bottom=self.bbox.bottom-1
        for i in range(1,8):
            h=bottom-height*(0.5)**i
            pygame.draw.line(surface,(128,)*3,(left,h),(right,h))
        second_x=round(1/time_sleep)
        assert second_x>1, "Decaying too fast"
        for i in range(left-self.rm%second_x+second_x,right,second_x):
            pygame.draw.line(surface,(128,)*3,(i,self.bbox.top),(i,bottom))
        pygame.draw.aalines(surface,(200,)*3,False,tuple((i+left,bottom-(height*0.5**((i+self.rm)/decay_ratio))) for i in range(right-left)))
        
        pygame.draw.aalines(surface,self.colour,False,tuple((i,bottom-(height*j/self.max)) for i,j in zip(range(left,left+len(data)),data)))
Photon(10,20)

for i in range(10,width,10):
    for j in range(10,height,10):
        
        Ratom(i,j)
g=Graph()
clock = pygame.time.Clock()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
            #sys.exit()


    screen.fill(black)
    
    P.group.update()
    g.upd(len(Ratom.group))
    
    P.group.draw(screen)
    g.draw(screen)
    pygame.display.flip()
    clock.tick(framerate)

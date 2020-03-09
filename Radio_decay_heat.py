# Python 3
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
import time,math,random,itertools

pygame.init()
heat_amount=1.5
heat_insulate=4#must be positive
heat_colour_scale=2
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
    def __init__(self,x,y,c):
        P.__init__(self,x,y)
        self.pos=(x,y)
        self.c=c
    def update(self):
        h=oldheat[self.c[0]][self.c[1]]
        self.rect.center=tuple(i+random.normalvariate(.5,h) for i in self.pos)
        if random.random()>0.5**(1/decay_ratio):
            oldheat[self.c[0]][self.c[1]]+=heat_amount
            Photon(*self.pos)
            Datom(*self.pos,self.c)
            self.kill()
class Datom(P):
    psz=4
    Img=pygame.Surface([psz*2]*2)
    Img.set_colorkey((0,0,0))
    pygame.draw.circle(Img,(128,128,128),(psz,psz),psz)
    group=pygame.sprite.Group()
    def __init__(self,x,y,c):
        P.__init__(self,x,y)
        self.pos=(x,y)
        self.c=c
    def update(self):
        h=oldheat[self.c[0]][self.c[1]]
        self.rect.center=tuple(i+random.normalvariate(.5,h) for i in self.pos)
        
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
ggp=10
ranges=[range(10,width,ggp),range(10,height,ggp)]
gsz=[len(r) for r in ranges]
gszp2=[i+2 for i in gsz]
for i,j in itertools.product(*[enumerate(r) for r in ranges]):
        
        Ratom(i[1],j[1],(i[0]+1,j[0]+1))
oldheat=[[0]*gszp2[1] for i in range(gszp2[0])]
def heatflow(h1):
    n=[]
    for i,h2 in enumerate(h1):
        if i in (0,len(h1)-1):
            n.append([0]*len(h2))
        else:
            k=[]
            for j,h3 in enumerate(h2):
                if j in (0,len(h2)-1):
                    k.append(0)
                else:
                    k.append((h3*heat_insulate+h2[j-1]+h2[j+1]+h1[i-1][j]+h1[i+1][j])/(heat_insulate+4))
            n.append(k)
    return n

g=Graph()
def getCol(h):
    h=max(min(h/heat_amount*heat_colour_scale,1),0)
    h=int(h*128)
    return(h,0,128-h)
clock = pygame.time.Clock()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
            #sys.exit()


    screen.fill(black)
    
    P.group.update()
    oldheat=heatflow(oldheat)
    for i,j in itertools.product(*[enumerate(r) for r in ranges]):
        pygame.draw.rect(screen,getCol(oldheat[i[0]+1][j[0]+1]),pygame.Rect(i[1]-ggp//2,j[1]-ggp//2,ggp,ggp))
    g.upd(len(Ratom.group))
    
    P.group.draw(screen)
    g.draw(screen)
    pygame.display.flip()
    clock.tick(framerate)
    

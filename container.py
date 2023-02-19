import pygame
from resmgr import *

# 对PNG透明贴图到图层后再绘制到另一图层进行了处理，创建surface时使用参数pygame.SRCALPHA，不能设置colorkey
# 这种其实应该直接将图片绘制到目标层
# 当需要反复重绘某个图层时，该图层上已经贴了png图片，再将此图层贴到另外的层上，会出现黑边
class Container:
    def __init__(self, game) -> None:
        self.surf = None
        self.children = []
        self.evtCalls = {}
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.parent = None
        self.worldPos = [0, 0]
        self.bgcolor = COLOR_KEY
        self.bgImg = None
        self.game = game
        self.name = ''
        self.isredraw = True

    def Create(self, screen: pygame.Surface, pos=(0,0), size=None):
        if size != None:
            self.surf = pygame.Surface(size, pygame.SRCALPHA, screen)
            self.rect = pygame.Rect(pos, size)
        else:
            self.surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA, screen)
            w, h = screen.get_size()
            self.rect = pygame.Rect(pos[0], pos[1], w, h)

    def setBackground(self, imgpath):
        res = ResMgr()
        self.setBackgroundImg(res.getImage(imgpath))
    
    def setBackgroundImg(self, img: pygame.Surface):
        if img.get_width() != self.surf.get_width() or img.get_height() != self.surf.get_height():
            self.bgImg = pygame.transform.scale(img, (self.surf.get_width(), self.surf.get_height()))
        else:
            self.bgImg = img

        alphas = pygame.surfarray.array_alpha(self.bgImg)
        self.bgImg.lock()
        for i in range(len(alphas)):
            sz = len(alphas[i])
            for j in range(sz):
                if alphas[i][j] == 0:
                    self.bgImg.set_at([i,j], COLOR_KEY)
        self.bgImg.unlock()

    def onActive(self, args):
        pass

    def addEvtListener(self, evtType, func):
        self.evtCalls[evtType] = func

    def removeEvtListener(self, evtType):
        del self.evtCalls[evtType]

    def addChild(self, child):
        child.parent = self
        child.worldPos = [self.worldPos[0] + child.rect.left, self.worldPos[1] + child.rect.top]
        self.children.append(child)

    def removeChild(self, child):
        self.worldPos = [0, 0]
        child.parent = None
        if child in self.children:
            self.children.remove(child)

    def dispatchEvts(self, evts):
        for child in self.children:
            child.dispatchEvts(evts)

        for evt in evts:
            if evt.done:
                continue
            epos = evt.pos
            if evt.type == pygame.MOUSEBUTTONUP:
                print(f"evt.pos: {evt.pos} worldpos: {self.worldPos}")
                if self.parent != None:
                    epos = [evt.pos[0] - self.parent.worldPos[0], evt.pos[1] - self.parent.worldPos[1]]
                if epos[0] < 0 or epos[1] < 0 or not self.rect.collidepoint(epos):
                    print(f'{self.name} skip evt {evt.type}')
                    continue
            func = self.evtCalls.get(evt.type)
            if func != None:
                if evt.type == pygame.MOUSEBUTTONUP:
                    func(epos)
                else:
                    func(evt)
                evt.done = True

    def update(self):
        pass

    def _drawSelf(self):
        pass

    def redrawOnce(self):
        if self.bgImg:
            self.surf.blit(self.bgImg, (0, 0))
        self._drawSelf()
        self.isredraw = False

    def draw(self, surf: pygame.Surface):
        if self.isredraw:
            self.surf.fill(self.bgcolor)
            if self.bgImg:
                self.surf.blit(self.bgImg, (0, 0))
            self._drawSelf()
        surf.blit(self.surf, self.rect)
        for child in self.children:
            child.draw(surf)
        
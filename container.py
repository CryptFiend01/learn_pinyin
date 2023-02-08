import pygame

COLOR_KEY = pygame.Color(0, 1, 0)

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

    def Create(self, screen: pygame.Surface, pos=(0,0), size=None):
        if size != None:
            self.surf = pygame.Surface(size, 0, screen)
            self.rect = pygame.Rect(pos, size)
        else:
            self.surf = pygame.Surface(screen.get_size(), 0, screen)
            w, h = screen.get_size()
            self.rect = pygame.Rect(pos[0], pos[1], w, h)

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

    def draw(self, surf: pygame.Surface):
        self.surf.fill(self.bgcolor)
        if self.bgImg:
            self.surf.blit(self.bgImg)
        self._drawSelf()
        surf.blit(self.surf, self.rect)
        for child in self.children:
            child.draw(surf)
        
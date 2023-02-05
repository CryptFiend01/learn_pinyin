from container import *
from resmgr import ResMgr

class Button(Container):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.text = None
        self.pics = []
        self.redraw = False

    def Make(self, screen, pos, size, pics, txt, click):
        if len(pics) == 0:
            self.bgcolor = pygame.Color(50, 100, 200)
        else:
            res = ResMgr()
            for pic in pics:
                self.pics.append(res.getImage(pic))
            self.bgImg = self.pics[0]
        self.Create(screen, pos, size)
        self.setText(txt)
        self.addClick(click)

    def setText(self, txt):
        res = ResMgr()
        
        self.text = txt

    def _drawSelf(self):
        pos = [0, 0] # (self.surf.get_width() - self.text.get_width())/2
        # print(f'draw txt at {pos}')
        font = pygame.font.SysFont("Consolas", 32)
        txt = font.render(self.text, True, pygame.Color(0, 0, 0))
        self.surf.blit(txt, pos)

    def addClick(self, func):
        self.addEvtListener(pygame.MOUSEBUTTONUP, func)







































































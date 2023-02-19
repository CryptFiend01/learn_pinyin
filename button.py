from container import *
from resmgr import ResMgr

class Button(Container):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.text = None
        self.pics = []
        self.redraw = False

    def Make(self, screen, pos, size, pics, txt, click):
        self.Create(screen, pos, size)
        if len(pics) == 0:
            self.bgcolor = pygame.Color(50, 100, 200)
        else:
            res = ResMgr()
            for pic in pics:
                img = res.getImage("button/" + pic)
                if img.get_size() != self.surf.get_size():
                    img = pygame.transform.scale(img, self.surf.get_size())
                self.pics.append(img)
            self.bgImg = self.pics[0]
            self.redrawOnce()
        self.setText(txt)
        self.addClick(click)
        self.name = f'button[{txt}]'
        print(f"{self.name} rect: {self.rect}")

    def setText(self, txt):
        self.text = txt

    def _drawSelf(self):
        if self.bgImg is None:
            res = ResMgr()
            font = res.getFont("ui")
            txt = font.render(self.text, True, pygame.Color(180, 180, 180))
            pos = [(self.surf.get_width() - txt.get_width())/2, 3]
            # print(f'draw txt at {pos}')
            self.surf.blit(txt, pos)

    def addClick(self, func):
        self.addEvtListener(pygame.MOUSEBUTTONUP, func)







































































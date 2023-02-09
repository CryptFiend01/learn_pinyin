from container import *
from button import *
from const import *
import numpy as np

class HonorUI(Container):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.grids = []
        self.grayGrids = []
        self.renders = []
        self.name = "honor_ui"
        self.backBtn = Button(game)

    def Create(self, screen: pygame.Surface):
        super().Create(screen)
        # self.bgcolor = pygame.Color(255, 222, 198)
        self.setBackground("honor_bg.jpg")
        self.backBtn.Make(screen, (10, 10), (94, 94), ["general_btn_back_nor.png"], "<-", self.onBackMain)
        self.addChild(self.backBtn)

        res = ResMgr()
        for i in range(8):
            img = res.getImage(f"{i+1}.png")
            if img.get_width() != 70 or img.get_height() != 70:
                img = pygame.transform.scale(img, (70, 70))
            self.grids.append(img)
            self.grayGrids.append(self.toGray(img))

    def toGray(self, img: pygame.Surface):
        alphas = pygame.surfarray.array_alpha(img)
        arr = pygame.surfarray.array3d(img)
        avgs = [[(r*0.298 + g*0.587 + b*0.114) for (r,g,b) in col] for col in arr]
        tagarr = []
        for i, col in enumerate(avgs):
            colarr = []
            for j, avg in enumerate(col):
                if alphas[i][j] == 0:
                    colarr.append([0, 13, 0])
                else:
                    colarr.append([avg, avg, avg])
            tagarr.append(colarr)
        arr = np.array(tagarr) #np.array([[[avg,avg,avg] for avg in col] for col in avgs])
        surf = pygame.surfarray.make_surface(arr)
        surf.set_colorkey(COLOR_KEY)
        return surf

    def onBackMain(self, pos):
        self.game.ChangeGameState(GAME_START)

    def onActive(self, args):
        honor = self.game.GetHonor()
        self.renders = []
        for i in range(honor):
            self.renders.append(self.grids[i])
        if len(self.renders) < MAX_HONOR:
            for i in range(len(self.renders), MAX_HONOR):
                self.renders.append(self.grayGrids[i])
        
    def _drawSelf(self):
        for i in range(MAX_HONOR):
            x, y = 300 + int(i % 4) * 100, 200 + (i // 4) * 100
            self.surf.blit(self.renders[i], (x, y))
    
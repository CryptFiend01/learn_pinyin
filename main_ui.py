from container import *
from button import *
from const import *

class MainUI(Container):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.startBtn = Button(game)
        self.showBtn = Button(game)
        self.name = 'main_ui'

    def Create(self, screen):
        super().Create(screen)
        # self.bgcolor = pygame.Color(120, 200, 33)
        res = ResMgr()
        self.bgImg = res.getImage("background_0.png")
        self.bgImg = pygame.transform.scale(self.bgImg, (self.surf.get_width(), self.surf.get_height()))
        startPics = []
        self.startBtn.Make(screen, [440, 200], (200, 30), startPics, u"开始游戏", self.onStartGame)
        self.addChild(self.startBtn)
        showPics = []
        self.showBtn.Make(screen, [440, 400], (200, 30), showPics, u"查看徽章", self.onShow)
        self.addChild(self.showBtn)

        self.addEvtListener(pygame.MOUSEBUTTONUP, self.onClick)

    def onClick(self, pos):
        print(f"click main ui {pos}.")

    def onStartGame(self, pos):
        self.game.ChangeGameState(GAME_PLAY)

    def onShow(self, pos):
        self.game.ChangeGameState(GAME_HONOR)
    
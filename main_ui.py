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
        self.setBackground("background_0.png")
        startPics = ["anniu-kaishi.png", "anniu-kaishi_sel.png"]
        self.startBtn.Make(screen, [440, 200], (238, 84), startPics, u"开始游戏", self.onStartGame)
        self.addChild(self.startBtn)
        showPics = ["general_btn_share_nor.png", "general_btn_share_sel.png"]
        self.showBtn.Make(screen, [440, 400], (238, 84), showPics, u"查看徽章", self.onShow)
        self.addChild(self.showBtn)

        self.addEvtListener(pygame.MOUSEBUTTONUP, self.onClick)

    def onClick(self, pos):
        print(f"click main ui {pos}.")

    def onStartGame(self, pos):
        self.game.ChangeGameState(GAME_PLAY)

    def onShow(self, pos):
        self.game.ChangeGameState(GAME_HONOR)
    
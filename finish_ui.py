from container import *
from button import *
from const import *

class FinishUI(Container):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.name = "finish_ui"
        self.nextButton = Button(game)
        self.retryButton = Button(game)
        self.exitButton = Button(game)
        self.scoreSurf = None
        self.diamondIndex = 0
        self.diamondSkip = 0

    def Create(self, screen: pygame.Surface):
        super().Create(screen)

        # self.bgcolor = pygame.Color(202,71,15)
        self.setBackground("background_3.png")

        self.nextButton.Make(screen, [160, 600], (190, 68), ["anniu-xiayigua.png"], u"下一关", self.onNext)
        self.retryButton.Make(screen, [160, 600], (190, 68), ["anniu-chongwan.png"], u"再试一次", self.onRetry)
        self.exitButton.Make(screen, [780, 600], (190, 68), ["general_btn_back_main_nor.png"], u"退出", self.onExit)
        self.addChild(self.exitButton)

    def onActive(self, args):
        score = args['score']
        res = ResMgr()
        # font = res.getFont("finish")
        # self.scoreSurf = font.render(f'{score}', True, pygame.Color(254, 215, 78))
        self.scoreSurf = res.getFinishScoreNum(score)
        isFinish = args['finish']
        if isFinish:
            self.addChild(self.nextButton)
            self.removeChild(self.retryButton)
        else:
            self.addChild(self.retryButton)
            self.removeChild(self.nextButton)

    def onExit(self, pos):
        self.game.ChangeGameState(GAME_START)

    def onNext(self, pos):
        self.game.ChangeGameState(GAME_PLAY)

    def onRetry(self, pos):
        self.game.ChangeGameState(GAME_PLAY)

    def _drawSelf(self):
        self.surf.blit(self.scoreSurf, (480, 380))
        res = ResMgr()
        pic = res.getImage("101.png")
        x = (self.diamondIndex % 4) * 128 + 512
        y = (self.diamondIndex // 4) * 128 + 512
        self.surf.blit(pic, (280, 360), (x, y, 128, 128))
        self.diamondSkip += 1
        if self.diamondSkip >= 12:
            self.diamondSkip = 0
            self.diamondIndex += 1
            if self.diamondIndex >= 15:
                self.diamondIndex = 0
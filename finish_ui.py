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
        self.bgcolor = pygame.Color(202,71,15)
        self.scoreSurf = None

    def Create(self, screen: pygame.Surface):
        super().Create(screen)

        self.nextButton.Make(screen, [160, 600], (80, 30), [], u"下一关", self.onNext)
        self.retryButton.Make(screen, [160, 600], (80, 30), [], u"再试一次", self.onRetry)
        self.exitButton.Make(screen, [780, 600], (80, 30), [], u"退出", self.onExit)
        self.addChild(self.exitButton)


    def onActive(self, args):
        score = args['score']
        res = ResMgr()
        font = res.getFont("finish")
        self.scoreSurf = font.render(f'{score}', True, pygame.Color(254, 215, 78))
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
        self.game.AddGate()
        self.game.ChangeGameState(GAME_PLAY)

    def onRetry(self, pos):
        self.game.ChangeGameState(GAME_PLAY)

    def _drawSelf(self):
        self.surf.blit(self.scoreSurf, (480, 380))
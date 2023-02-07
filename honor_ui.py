from container import *
from button import *
from const import *

class HonorUI(Container):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.grids = []
        self.name = "honor_ui"
        self.backBtn = Button(game)

    def Create(self, screen: pygame.Surface):
        super().Create(screen)
        self.bgcolor = pygame.Color(255, 222, 198)
        self.backBtn.Make(screen, (10, 10), (50, 50), [], "<-", self.onBackMain)
        self.addChild(self.backBtn)

    def onBackMain(self, pos):
        self.game.ChangeGameState(GAME_START)
        
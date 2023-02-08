from container import *
from button import *

class FinishUI(Container):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.name = "finish_ui"
        self.nextButton = Button(game)
        self.retryButton = Button(game)

    def Create(self, screen: pygame.Surface):
        super().Create(screen)

    def onActive(self, args):
        score = args['score']
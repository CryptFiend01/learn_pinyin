from container import *

class PlayUI(Container):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.name = 'play_ui'

    def Create(self, screen):
        super().Create(screen)
        self.bgcolor = pygame.Color(150, 200, 0)
    
    def update(self):
        diff = 0
        speed = self.diff * 2 + 3

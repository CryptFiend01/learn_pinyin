from container import *
from pypinyin import pinyin, Style
from pevent import PyEvent
from resmgr import *

class PlayUI(Container):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.name = 'play_ui'
        self.input = ''
        self.word = ''
        self.pinyin = ''
        self.score = 0

    def Create(self, screen):
        super().Create(screen)
        self.bgcolor = pygame.Color(150, 200, 0)
    
    def update(self):
        diff = self.game.diff
        speed = diff * 2 + 3
        res = ResMgr()
        if self.word == '':
            self.word = res.getWord(diff)
            self.pinyin = pinyin(self.word, style=Style.TONE3, heteronym=True)

    def addScore(self):
        self.score += 10
        self.word = ''
        self.pinyin = ''
        self.input = ''

    def onKeyup(self, evt: PyEvent):
        s = "abcdefghijklmnopqrstuvwxyz"
        if evt.key >= pygame.K_a and evt.key <= pygame.K_z:
            self.input += s[evt.key - pygame.K_a]
            if self.input == self.pinyin:
                self.addScore()
        elif evt.key == pygame.K_BACKSPACE:
            self.input = self.input[:-1]
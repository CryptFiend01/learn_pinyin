from container import *
from pypinyin import pinyin, Style
from pevent import PyEvent
from resmgr import *
from button import *
from const import *
import random

class PlayUI(Container):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.name = 'play_ui'
        self.input = ''
        self.word = ''
        self.pinyin = ''
        self.wordScore = 0
        self.wordPos = [0, 0]
        self.wordColor = None
        self.score = 0
        self.gate = None
        self.wordCount = 0

        self.wordSurf = None
        self.pinyinSurf = None
        self.scoreSurf = None

    def Create(self, screen):
        super().Create(screen)
        self.bgcolor = pygame.Color(150, 200, 0)
        self.scoreSurf = pygame.Surface((200, 40), 0, screen)
        self.addEvtListener(pygame.KEYUP, self.onKeyup)
        self.redrawScore()

    def nextRound(self):
        self.input = ''
        self.word = ''
        self.pinyin = ''
        self.wordScore = 0
        self.wordPos = [0, 0]
        self.wordColor = None
        self.wordSurf = None
        self.pinyinSurf = None

    def onActive(self, args):
        self.score = 0
        res = ResMgr()
        self.gate = res.getGate(self.game.GetGate() + 1)
        self.wordCount = 0
        self.nextRound()
    
    def update(self):
        gate = self.game.GetGate()
        speed = gate + 0.5
        res = ResMgr()
        if self.word == '':
            self.word, self.wordScore = res.getWord(gate)
            if (gate + 1) % 3 != 0:
                self.pinyin = pinyin(self.word, style=Style.NORMAL, heteronym=True)
            else:
                self.pinyin = pinyin(self.word, style=Style.TONE3, heteronym=True)
            print(self.pinyin)
            self.wordPos[0] = random.randint(100, 900)
            self.wordColor = pygame.Color(random.randint(0, 130), random.randint(0, 130), random.randint(0, 130))
            font = res.getFont("word")
            font.set_bold(True)
            self.wordSurf = font.render(self.word, True, self.wordColor)
            self.wordCount += 1
        else:
            self.wordPos[1] += speed
            if self.wordPos[1] > 768:
                self.nextRound()

    def addScore(self):
        self.score += self.wordScore
        self.nextRound()
        self.redrawScore()
        if self.wordCount >= self.gate['word_count']:
            self.game.ChangeGameState(GAME_FINISH, {"score": self.score})

    def addKeyPinyin(self, k):
        self.input += k
        print(f"input: {self.input}")
        self.redrawPinyin()
        for i in range(len(self.pinyin[0])):
            if self.input == self.pinyin[0][i]:
                self.addScore()
                break

    def onKeyup(self, evt: PyEvent):
        alphas = "abcdefghijklmnopqrstuvwxyz"
        digist = "1234"
        # print(f'pygame.K_a: {pygame.K_a} pygame.K_z: {pygame.K_z} evt.key: {evt.key}')
        if evt.key >= pygame.K_a and evt.key <= pygame.K_z:
            self.addKeyPinyin(alphas[evt.key - pygame.K_a])
        elif evt.key >= pygame.K_1 and evt.key <= pygame.K_4:
            self.addKeyPinyin(digist[evt.key - pygame.K_1])
        elif evt.key == pygame.K_BACKSPACE:
            self.input = self.input[:-1]
            self.redrawPinyin()

    def redrawScore(self):
        self.scoreSurf.fill(pygame.Color(128, 128, 255))
        res = ResMgr()
        font = res.getFont("ui")
        font.set_bold(True)
        score = font.render(f"{self.score}", True, pygame.Color(254, 215, 78))
        self.scoreSurf.blit(score, (30, 0))

    def redrawPinyin(self):
        res = ResMgr()
        font = res.getFont("ui")
        font.set_bold(True)
        self.pinyinSurf = font.render(self.input, True, pygame.Color(0, 64, 128))

    def _drawSelf(self):
        if self.wordSurf != None:
            self.surf.blit(self.wordSurf, self.wordPos)
        if self.pinyinSurf != None:
            self.surf.blit(self.pinyinSurf, (10, 728))
        self.surf.blit(self.scoreSurf, (800, 724))
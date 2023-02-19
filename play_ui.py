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
        self.skip = 0
        self.state = STATE_PLAY
        self.pinyinPos = [490, 600]
        self.pinyinTarget = [810, 710]
        self.pinyinSpeed = [32, 11]
        self.addScoreStart = [930, 700]
        self.addScoreTarget = [930, 640]
        self.addScorePos = [self.addScoreStart[0], self.addScoreStart[1]]
        self.isDrawAddScore = False
        self.sounds = []

        self.wordSurf = None
        self.pinyinSurf = None
        self.scoreSurf = None
        self.gateSurf = None
        self.scorePanel = None
        self.addScoreSurf = None

    def Create(self, screen):
        super().Create(screen)
        # self.bgcolor = pygame.Color(150, 200, 0)
        self.setBackground("story_background.png")
        self.scoreSurf = pygame.Surface((200, 60), 0, screen)
        self.scoreSurf.set_colorkey(COLOR_KEY)
        self.scoreSurf.fill(COLOR_KEY)

        res = ResMgr()
        panel = res.getImage("smallPanel.png")
        self.scorePanel = pygame.transform.scale(panel, (self.scoreSurf.get_width(), self.scoreSurf.get_height()))
        
        self.addEvtListener(pygame.KEYUP, self.onKeyup)
        self.redrawScore()

        self.gateSurf = pygame.Surface((150, 36))
        self.gateSurf.set_colorkey(COLOR_KEY)
        self.gateSurf.fill(COLOR_KEY)

        self.addScoreSurf = pygame.Surface((100, 50), 0, screen)
        self.addScoreSurf.set_colorkey(COLOR_KEY)
        self.addScoreSurf.fill(COLOR_KEY)

        self.sounds.append(pygame.mixer.Sound("assets/sounds/snd_input.mp3"))
        self.sounds.append(pygame.mixer.Sound("assets/sounds/snd_score.mp3"))

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
        gate = self.game.GetGate() + 1
        self.gate = res.getGate(gate)
        self.wordCount = 0
        self.skip = 0
        self.state = STATE_PLAY

        bg = res.getImage("guanqia.png")
        self.gateSurf.fill(COLOR_KEY)
        self.gateSurf.blit(bg, (0, 0))
        gateNum = res.getGateNum(gate)
        x = 63 if gate < 10 else 53
        self.gateSurf.blit(gateNum, (x, 3))

        self.nextRound()
    
    def update(self):
        gate = self.game.GetGate()
        speed = self.gate['speed']
        res = ResMgr()
        if self.word == '':
            self.word, self.wordScore = res.getWord(gate)
            if (gate + 1) % 3 != 0:
                self.pinyin = pinyin(self.word, style=Style.NORMAL, heteronym=True)
            else:
                self.pinyin = pinyin(self.word, style=Style.TONE3, heteronym=True)
            print(self.pinyin)
            self.wordPos[0] = random.randint(100, 900)
            self.wordColor = res.randomColor()
            font = res.getFont("word")
            font.set_bold(True)
            self.wordSurf = font.render(self.word, True, self.wordColor)
            self.wordCount += 1
        else:
            if self.state == STATE_PLAY:
                self.skip += 1
                if self.skip == self.gate['skip']:
                    self.skip = 0
                    self.wordPos[1] += speed
                    if self.wordPos[1] > 768:
                        self.nextRound()
                        self.finishGate()
            elif self.state == STATE_PINYIN_DOWN:
                self.skip += 1
                if self.skip < 10:
                    return
                self.skip = 0
                if self.pinyinPos != self.pinyinTarget:
                    self.pinyinPos[0] += self.pinyinSpeed[0]
                    self.pinyinPos[1] += self.pinyinSpeed[1]
                else:
                    self.pinyinDownFinish()
        if self.isDrawAddScore:
            if self.addScorePos != self.addScoreTarget:
                self.addScorePos[1] -= 1
                alpha = self.addScoreSurf.get_alpha() or 255
                self.addScoreSurf.set_alpha(alpha - 4)
            else:
                self.isDrawAddScore = False
                self.addScorePos[0], self.addScorePos[1] = self.addScoreStart[0], self.addScoreStart[1]
                self.addScoreSurf.set_alpha(255)

    def finishGate(self):
        if self.wordCount >= self.gate['word_count']:
            isFinish = self.score >= self.gate['finish_score']
            res = ResMgr()
            nextGate = res.getGate(self.game.GetGate()+1)
            if isFinish and nextGate != None:
                self.game.AddGate()
            self.game.ChangeGameState(GAME_FINISH, {"score": self.score, "finish":isFinish})

    def addScore(self):
        self.score += self.wordScore
        self.isDrawAddScore = True
        self.redrawAddScore(self.wordScore)
        self.nextRound()
        self.redrawScore()
        self.finishGate()

    def pinyinSuccess(self, i):
        self.state = STATE_PINYIN_DOWN
        self.input = pinyin(self.word, style=Style.TONE, heteronym=True)[0][i]
        self.redrawPinyin()
        self.skip = 0

    def pinyinDownFinish(self):
        self.sounds[SND_SCORE-1].play()
        self.state = STATE_PLAY
        self.pinyinPos = [490, 600]
        self.addScore()

    def addKeyPinyin(self, k):
        self.input += k
        # print(f"input: {self.input}")
        self.redrawPinyin()
        for i in range(len(self.pinyin[0])):
            if self.input == self.pinyin[0][i]:
                self.pinyinSuccess(i)
                break

    def onKeyup(self, evt: PyEvent):
        if self.state != STATE_PLAY:
            return
        alphas = "abcdefghijklmnopqrstuvwxyz"
        digist = "1234"
        # print(f'pygame.K_a: {pygame.K_a} pygame.K_z: {pygame.K_z} evt.key: {evt.key}')
        self.sounds[SND_INPUT-1].play()
        if evt.key >= pygame.K_a and evt.key <= pygame.K_z:
            self.addKeyPinyin(alphas[evt.key - pygame.K_a])
        elif evt.key >= pygame.K_1 and evt.key <= pygame.K_4:
            self.addKeyPinyin(digist[evt.key - pygame.K_1])
        elif evt.key == pygame.K_BACKSPACE:
            self.input = self.input[:-1]
            self.redrawPinyin()

    def redrawScore(self):
        self.scoreSurf.fill(COLOR_KEY)        
        self.scoreSurf.blit(self.scorePanel, (0, 0))
        res = ResMgr()
        defen = res.getImage("defen.png")
        self.scoreSurf.blit(defen, (5, 5))
        # font = res.getFont("ui")
        # font.set_bold(True)
        # score = font.render(f"{self.score}", True, pygame.Color(254, 215, 78))
        score = res.getScoreNum(self.score)
        self.scoreSurf.blit(score, (120, 15))

    def redrawPinyin(self):
        res = ResMgr()
        font = res.getFont("pinyin")
        font.set_bold(True)
        self.pinyinSurf = font.render(self.input, True, pygame.Color(230, 184, 108))

    def redrawAddScore(self, score):
        res = ResMgr()
        add = res.getImage("zuanshi+.png")
        self.addScoreSurf.fill(COLOR_KEY)
        self.addScoreSurf.blit(add, (0, 2))
        scoreimg = res.getScoreNum(score)
        self.addScoreSurf.blit(scoreimg, (45, 10))

    def _drawSelf(self):
        if self.wordSurf != None:
            self.surf.blit(self.wordSurf, self.wordPos)
        self.surf.blit(self.scoreSurf, (810, 714))
        if self.pinyinSurf != None:
            self.surf.blit(self.pinyinSurf, self.pinyinPos)

        if self.isDrawAddScore:
            self.surf.blit(self.addScoreSurf, self.addScorePos)

        x = (self.surf.get_width() - self.gateSurf.get_width()) / 2
        self.surf.blit(self.gateSurf, (x, 20))
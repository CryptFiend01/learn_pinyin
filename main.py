import pygame
from xpinyin import Pinyin

GAME_START = 1
GAME_PLAY = 2
GAME_PAUSE = 3
GAME_FINISH = 4

class PinyinGame:
    def __init__(self) -> None:
        self.screen = None
        self.surface = None
        self.scoreSurf = None   # 积分板
        self.wordSurf = None    # 汉字显示
        self.pinyinSurf = None  # 拼音显示
        self.isPause = False
        self.pauseSurf = None   # 暂停界面
        self.enterSurf = None   # 开始界面
        self.gameSurf = None    # 游戏界面
        self.finishSurf = None  # 过关结算界面
        self.gamestate = GAME_START

    def Init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768), 0, 32)
        self.surface = pygame.surface.Surface((1024, 768), 0, self.screen)
        self.enterSurf = pygame.surface.Surface((1024, 768), 0, self.screen)

    def draw(self):
        self.surface.fill(pygame.Color(0, 0, 0))
        if self.gamestate == GAME_START:
            self.drawEnterSurf()
        self.screen.blit(self.surface, (0, 0))

    def drawEnterSurf(self):
        if self.gamestate == GAME_START:
            self.enterSurf.fill(pygame.Color(200, 100, 0))
            self.surface.blit(self.enterSurf, (0, 0))

    def switchPause(self):
        self.isPause = not self.isPause

    def Run(self):
        fpsClock = pygame.time.Clock()

        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                elif evt.type == pygame.K_ESCAPE:
                    self.switchPause()
                
                self.draw()
                pygame.display.update()
                fpsClock.tick(10)
def main():
    game = PinyinGame()
    game.Init()
    game.Run()

if __name__ == '__main__':
    main()
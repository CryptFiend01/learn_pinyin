import pygame
import json
import sys
from xpinyin import Pinyin
from container import *
from resmgr import *
from main_ui import *
from pause_ui import *
from finish_ui import *
from honor_ui import *
from play_ui import *
from const import *
from pevent import PyEvent

@Singleton
class PinyinGame:
    def __init__(self) -> None:
        self.gamestate = GAME_START
        self.screen = None
        self.surface = None
        self.diff = 0
        self.scenes = []

    def Init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size(), 0, self.screen)
        self.surface.set_colorkey(COLOR_KEY)

        res = ResMgr()
        if not res.Init():
            return False

        mainUI = MainUI(self)
        mainUI.Create(self.screen)
        self.scenes.append(mainUI)
        playUI = PlayUI(self)
        playUI.Create(self.screen)
        self.scenes.append(playUI)
        pauseUI = PauseUI(self)
        pauseUI.Create(self.screen)
        self.scenes.append(pauseUI)
        finishUI = FinishUI(self)
        finishUI.Create(self.screen)
        self.scenes.append(finishUI)
        honorUI = HonorUI(self)
        honorUI.Create(self.screen)
        self.scenes.append(honorUI)
        return True

    def draw(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        self.surface.fill(COLOR_KEY)
        ui = self.scenes[self.gamestate - 1]
        ui.draw(self.surface)
        self.screen.blit(self.surface, (0, 0))

    def ChangeGameState(self, state):
        self.gamestate = state

    def Run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(100)
            evts = []
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    e = PyEvent(evt.type)
                    if evt.type == pygame.MOUSEBUTTONUP:
                        print(f"mouseup {evt.pos}")
                        e.pos[0], e.pos[1] = evt.pos[0], evt.pos[1]
                    elif evt.type == pygame.KEYDOWN:
                        e.key = evt.key
                    evts.append(e)
            self.scenes[self.gamestate-1].dispatchEvts(evts)
            self.scenes[self.gamestate-1].update()
            self.draw()
            pygame.display.flip()

def main():
    game = PinyinGame()
    if game.Init():
        game.Run()

main()
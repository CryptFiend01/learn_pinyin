import pygame
import json
import random

def Singleton(cls):
    _instance = {}

    def instance():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return instance

@Singleton
class ResMgr:
    def __init__(self) -> None:
        self.imgs = {}
        self.fonts = {}

    def Init(self):
        try:
            self.difficults = json.load(open('gate.json', 'r', encoding='utf-8'))
        except Exception as e:
            print(f"load gate.json error: {str(e)}")
            return False
        return True

    def getImage(self, name) -> pygame.Surface:
        img = self.imgs.get(name)
        if not img:
            img = pygame.image.load("assets/" + name).convert_alpha()
            self.imgs[name] = img
        return img

    def getFont(self, name) -> pygame.font.Font:
        font = self.fonts.get(name)
        if not font:
            font = pygame.font.SysFont("Consolas", 32)
            self.fonts[name] = font
        return font
        
    def getWord(self, difficult):
        if difficult == 1:
            g = self.difficults[0]
            i = random.randint(1, len(g))
            return g[i]
        else:
            return self.difficults[difficult-1][0]
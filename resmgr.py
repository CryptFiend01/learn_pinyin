import pygame
import json
import random

COLOR_KEY = pygame.Color(0, 13, 0)

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
        self.fontNames = {"ui":["fangsong", 24], "word":["fangsong", 36], "pinyin":["fangsong", 48], "finish":["fangsong", 80]}

    def Init(self):
        if not self.loadWords():
            return False

        if not self.loadGates():
            return False
        return True

    def loadWords(self):
        try:
            self.words = json.load(open('assets/word.json', 'r', encoding='utf-8'))
            print(self.words)
        except Exception as e:
            print(f"load word.json error: {str(e)}")
            return False
        return True

    def loadGates(self):
        try:
            self.gates = json.load(open("assets/gate.json", "r", encoding='utf-8'))
        except Exception as e:
            print(f"load gate.json error: {str(e)}")
            return False
        return True

    def getImage(self, name) -> pygame.Surface:
        img = self.imgs.get(name)
        if not img:
            img = pygame.image.load("assets/pics/" + name).convert_alpha()
            if name == 'num-daojushu.png':
                img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
            self.imgs[name] = img
        return img

    def getScoreSurf(self, num, pic):
        sn = str(num)
        imgNum = self.getImage(pic)
        w = imgNum.get_width() / 10
        h = imgNum.get_height()
        length = len(sn)
        surf = pygame.Surface((w * length, h))
        surf.set_colorkey(COLOR_KEY)
        surf.fill(COLOR_KEY)
        for i in range(length):
            n = int(sn[i])
            surf.blit(imgNum, (i*w, 0, w, h), (n*w, 0, w, h))
        return surf

    def getScoreNum(self, num):
        return self.getScoreSurf(num, "score.png")

    def getGateNum(self, num):
        return self.getScoreSurf(num, "score_green.png")

    def getFinishScoreNum(self, num):
        return self.getScoreSurf(num, "num-daojushu.png")

    def getFont(self, name) -> pygame.font.Font:
        fontType = self.fontNames.get(name)
        if fontType == None:
            return None

        font = self.fonts.get(name)
        if not font:
            font = pygame.font.SysFont(fontType[0], fontType[1])
            self.fonts[name] = font
        return font
        
    def getWord(self, difficult):
        d = 0
        if difficult <= 0 or difficult > len(self.words):
            d = random.randint(0, len(self.words)-1)
        else:
            # 根据难度距离difficult远近来决定权重
            weights = [1] * len(self.words)
            # 指定位置权重最高，离得越远权重越低
            rateadds = [10, 5, 2, 1, 0]
            for i in range(len(self.words)):
                n = abs(i + 1 - difficult)
                weights[i] += rateadds[n]
            # 根据权重随机难度组
            total = sum(weights)
            rd = random.randint(1, total)
            w = 0
            for i in range(len(weights)):
                w += weights[i]
                if w >= rd:
                    d = i
                    break
        # 根据难度组随机汉字，并返还该字对应的分数
        g = self.words[d]
        i = random.randint(1, len(g)) - 1
        return g[i], (d + 1) * 10

    def getGate(self, gate):
        if gate < 1 or gate > len(self.gates):
            return None
        return self.gates[gate - 1]

    def randomColor(self):
        main = random.randint(200, 255)
        idx = random.randint(1, 3)
        color = [0, 0, 0]
        color[idx-1] = main
        for i in range(3):
            if color[i] == 0:
                color[i] = random.randint(0, 255)
        return pygame.Color(color[0], color[1], color[2])
class PyEvent:
    def __init__(self, t) -> None:
        self.type = t
        self.pos = [0, 0]
        self.key = 0
        self.done = False

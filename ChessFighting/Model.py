import main, pygame, Chess

class Player:
    def __init__(self, consciousness):
        self.consciousness = consciousness
        self.time = 300
        self.fighter = None
        self.move_time = 30
    def update_time(self):
        self.move_time = int(self.consciousness*0.3)
        if self.move_time>self.time:
            self.move_time = self.time

class Game:
    def __init__(self):
        self.round = 1
        self.p1 = Player(100)
        self.p2 = Player(100)
        self.board = Chess.Board()
        self.winner = None



if __name__ == "__main__":
    main.main()
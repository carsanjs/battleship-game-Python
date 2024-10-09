class Game:
    def __init__(self, pk):
        self.id = pk
        self.both_connected = False
        self.turn = "0"
        self.boards = [None, None]
        self.winner = False

    def is_winner(self):
        """Summing all sinked fields of the board for checking win condition."""
        sum1 = sum(1 if field.sinked else 0 for row in self.boards[0].fields for field in row)
        sum2 = sum(1 if field.sinked else 0 for row in self.boards[1].fields for field in row)
        if sum1 == 20:
            self.winner = "1"
            return True
        elif sum2 == 20:
            self.winner = "0"
            return True
        return False

    def __str__(self):
        return "Game {}".format(self.id)

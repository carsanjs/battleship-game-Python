from field import Field


class Board:
    x_axis = list(range(10))
    y_axis = list(range(10))

    def __init__(self, x=50, y=100):
        self.x = x
        self.y = y
        self.fields = [[Field(i, j, self.x, self.y) for i in self.x_axis] for j in self.y_axis]
        self.is_active = False

    def draw(self, win):
        self.update()
        for row in self.fields:
            for field in row:
                field.draw(win)

    def update(self):
        for row in self.fields:
            for field in row:
                field.x = self.x + field.col * field.width
                field.y = self.y + field.row * field.width
                field.rect = (field.x, field.y, field.width, field.height)

    def reset_board(self, ships):
        for row in self.fields:
            for field in row:
                field.ship = False
                field.shipAvaiable = True
                field.active = True
                field.hitted = False
                field.sinked = False
        for ship in ships:
            ship.reset()

    def surrounding_fields(self, row, col):
        surrounding = [(r, c) for r in range(row - 1, row + 2) for c in range(col - 1, col + 2)]
        surrounding = [f for f in surrounding if (f[0] >= 0 and f[0] <= 9 and f[1] >= 0 and f[1] <= 9)]
        return set(surrounding)

    def looking_ship(self, shot_row, shot_col):
        """Marking ensured fields with no ship during the shooting.
        If player sunk entire ship, marking all surrounding fields around ship as hitted."""
        ship_fields = {(shot_row, shot_col)}
        ship_len = 1
        surrounding = self.surrounding_fields(shot_row, shot_col) - ship_fields

        for f in surrounding:
            if f[0] != shot_row and f[1] != shot_col:
                self.fields[f[0]][f[1]].active = False
                self.fields[f[0]][f[1]].hitted = True

        while True:
            for f in surrounding:
                if self.fields[f[0]][f[1]].ship:
                    ship_fields.add(f)
            if ship_len != len(ship_fields):
                for ship_field in ship_fields:
                    surrounding = surrounding | self.surrounding_fields(ship_field[0], ship_field[1])
                surrounding = surrounding - ship_fields
                ship_len = len(ship_fields)
            else:
                break

        if all(self.fields[f[0]][f[1]].sinked for f in ship_fields):
            for f in surrounding:
                self.fields[f[0]][f[1]].active = False
                self.fields[f[0]][f[1]].hitted = True

    def is_ready(self):
        """Checking for placing all ships on the board."""
        ship_count = sum(1 if f.ship else 0 for row in self.fields for f in row)
        if ship_count == 22:
            return True
        return False

    def __repr__(self):
        return "Board x: {} y: {}".format(self.x, self.y)

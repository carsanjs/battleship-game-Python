import pygame


class Field:
    width = 40
    height = 40
    border_color = (0, 0, 0)
    lines_color = (255, 0, 0)
    color = (255, 255, 255)
    circle_color = (0, 0, 0)

    def __init__(self, col, row, start_x, start_y):
        self.col = col
        self.row = row
        self.start_x = start_x
        self.start_y = start_y
        self.x = self.start_x + self.col * self.width
        self.y = self.start_y + self.row * self.width
        self.rect = (self.x, self.y, self.width, self.height)
        self.active = True
        self.hitted = False
        self.ship = False
        self.shipAvaiable = True
        self.sinked = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.rect(win, self.border_color, self.rect, 1)
        if self.sinked:
            pygame.draw.line(win, self.lines_color, (self.x, self.y), (self.x + self.width, self.y + self.height), 4)
            pygame.draw.line(win, self.lines_color, (self.x, self.y + self.height), (self.x + self.width, self.y), 4)
        elif self.hitted:
            pygame.draw.circle(win, self.circle_color, (round(self.x + self.width/2), round(self.y + self.height/2)), 5)

    def click(self):
        pos = pygame.mouse.get_pos()
        if self.x < pos[0] < self.x + self.width and self.active:
            if self.y < pos[1] < self.y + self.height:
                if self.ship:
                    self.sinked = True
                else:
                    self.hitted = True
                self.active = False
                return True
        return False

    def isShipPoss(self, ship):
        """Constraints for setting up ships on the board. Ships can't go out of the board."""
        if ship.position == "horizontal":
            if self.col + ship.mast <= 10:
                return True
            return False
        else:
            if self.row + ship.mast <= 10:
                return True
            return False

    def __repr__(self):
        return "Field ({}, {})".format(self.col, self.row)

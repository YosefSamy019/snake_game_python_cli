class Position:
    def __init__(self, x, y):
        assert type(x) is int and type(y) is int

        self.x = x
        self.y = y

    def __str__(self):
        return f"X:{self.x}, Y:{self.y}"

    def copy(self):
        return Position(self.x, self.y)

    def __add__(self, other):
        assert type(other) is Position

        return Position(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        if type(other) is Position:
            return self.x == other.x and self.y == other.y
        return False

    def limit(self, window_width, window_height):
        while self.x < 0:
            self.x = self.x + window_width

        while self.x >= window_width:
            self.x = self.x - window_width

        while self.y < 0:
            self.y = self.y + window_height

        while self.y >= window_height:
            self.y = self.y - window_height

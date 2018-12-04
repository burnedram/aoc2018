from parse import parse

class Claim:
    def __init__(self, line):
        (self.id, self.x, self.y, self.w, self.h) = map(int, parse("#{} @ {},{}: {}x{}", line))

    def __str__(self):
        return "#{} @ {},{}: {}x{}".format(self.id, self.x, self.y, self.w, self.h)

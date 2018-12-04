from parse import parse

class Entry:
    def __init__(self, line):
        (self.month, self.day, self.hour, self.minute, self.action) = parse("[1518-{}-{} {}:{}] {}", line)
        (self.month, self.day, self.hour, self.minute) = map(int, (self.month, self.day, self.hour, self.minute))

    def __lt__(self, other):
        return ((self.month, self.day, self.hour, self.minute) <
                (other.month, other.day, other.hour, other.minute))

    def __str__(self):
        return "[1518-{:02d}-{:02d} {:02d}:{:02d}] {}".format(self.month, self.day, self.hour, self.minute, self.action)

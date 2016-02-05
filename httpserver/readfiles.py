# -*- coding: utf-8 -*-
import sys
import random

class Bilibili:
    def __init__(self, filename):
        self.content = []
        for line in open(filename):
            self.content.append(line.strip('\n'))
        self.septLen = len(self.content)

    def pick(self):
        p = random.randint(0, self.septLen-1)
        return self.content[p]


if __name__ == '__main__':
    hs = Bilibili(sys.argv[1])
    print hs.pick()

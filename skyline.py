"""
#!/usr/bin/env python3.7
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import random as rnd
import functools
import heapq as hq
import numpy as np
from matplotlib.pyplot import figure, show
from matplotlib.ticker import MaxNLocator
# import heap
# import heapq27


class Skyline:
    buildings = []
    area = 0
    height = 0

    def __init__(self, inputBuildings=[]):
        self.buildings = inputBuildings
        self.compact()

    def updateStats(self):
        self.area, self.height = 0, 0
        for b in self.buildings:
            self.area += b.height*(b.end - b.start)
            self.height = max(self.height, b.height)

    def draw(self, fileName):
        res = self.buildings
        """
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        lo = _x[0]
        hi = _x[-1] + _width[-1]
        ax.set_xticks([x for x in range(lo,hi+1)])
        ax.set_yticks(np.arange(0, 81, 10))
        """
        # mpl.rcParams.update(mpl.rcParamsDefault)
        # plt.style.use('default')
        ax = figure().gca()
        _x = [b.start for b in res]
        _height = [b.height for b in res]
        _width = [b.end - b.start for b in res]
        ax.bar(x=_x, height=_height, width=_width, color='r', align='edge')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.savefig(fileName)

    def stats(self):
        return "area: " + str(self.area) + "\nheight: " + str(self.height)

    def __mul__(self, other):
        res = []
        if isinstance(other, int):
            if self.buildings == []:
                return Skyline([])
            dist = self.buildings[-1].end - self.buildings[0].start
            res = []
            for i in range(other):
                she = [x.attList() for x in self.buildings]
                res.extend([Building(a+i*dist, h, b+i*dist)
                            for a, h, b in she])
            return Skyline(res)
        self.compact()
        other.compact()
        i, j = 0, 0
        while i < len(self.buildings) and j < len(other.buildings):
            print(i, j)
            istart, iheight, iend = self.buildings[i].attList()
            jstart, jheight, jend = other.buildings[j].attList()
            if istart > jend:
                print("nope1")
                j += 1
            elif jstart > iend:
                print("nope2")
                i += 1
            else:
                res.append(Building(max(istart, jstart), min(
                    iheight, jheight), min(iend, jend)))
                if iend == jend:
                    i += 1
                    j += 1
                elif jend < iend:
                    j += 1
                else:
                    i += 1
        # print(res)
        return Skyline(res)

    def __add__(self, other):
        if isinstance(other, int):
            res = [Building(a+other, h, b+other)
                   for a, h, b in [x.attList() for x in self.buildings]]
            return Skyline(res)
        else:
            return Skyline(self.buildings + other.buildings)

    # def __radd__(self,other):
    #     return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            return self.__add__(-other)

    def __neg__(self):
        if self.buildings == []:
            return Skyline([])
        else:
            low = self.buildings[0].start
            high = self.buildings[-1].end
            newBuildings = []
            for b in self.buildings:
                d1 = b.start - low
                d2 = high - b.end
                diff = d2 - d1
                newBuildings.append(
                    Building(b.start + diff, b.height, b.end + diff))
            return Skyline(newBuildings)

    def __repr__(self):
        return ','.join([str(x) for x in self.buildings])

    def addBuildings(self, newBuildings):
        self.buildings = self.buildings + newBuildings
        self.compact()

    def generate(self, n, h, w, xmin, xmax):
        self.buildings = []
        if xmin >= xmax:
            return
        heights = [rnd.randint(0, h) for _ in range(n)]
        widths = [rnd.randint(1, w) for _ in range(n)]
        starts = [rnd.randint(xmin, xmax) for _ in range(n)]
        for h, w, s in zip(heights, widths, starts):
            if h > 0:
                self.buildings.append(Building(s, h, min(xmax, s+w)))
            else:
                print(h, w, s)
        self.compact()

    @staticmethod
    def merge(self, s2):
        self.buildings = self.buildings + s2.buildings

    def compact(self):
        if self.buildings == []:
            return
        tmp = []
        for build in self.buildings:
            # False means we open the interval
            tmp.append((build.start, False, build.height))
            # True means we close the interval
            tmp.append((build.end, True, build.height))
        tmp.sort()
        h = []
        hi = dict()
        res = []
        st = tmp[0][0]
        curH = tmp[0][2]
        for i, (pos, close, height) in enumerate(tmp):
            if close:
                if height == curH:
                    if st <= pos-1:
                        if len(res) > 0 and curH == res[-1].height \
                                and st == res[-1].end:
                            res[-1].end = pos
                        else:
                            res.append(Building(st, curH, pos))
                    st = pos

                hi[height] -= 1
                while len(h) > 0 and hi[-h[0]] == 0:
                    hq.heappop(h)
                """
                if hi[height] == 0:
                    del hi[height]
                """

            else:
                hq.heappush(h, -height)
                if height > curH:
                    if curH > 0 and st <= pos-1:
                        if len(res) > 0 and curH == res[-1].height \
                                and st == res[-1].end:
                            res[-1].end = pos
                        else:
                            res.append(Building(st, curH, pos))
                    st = pos
                if height not in hi:
                    hi[height] = 0
                hi[height] += 1
                while hi[-h[0]] == 0:
                    hq.heappop(h)
            if len(h) > 0:
                curH = -h[0]
            else:
                curH = -1
        self.buildings = res
        self.updateStats()


class Building:
    def __init__(self, start, height, end):
        self.start = start
        self.height = height
        self.end = end

    def attList(self):
        return [self.start, self.height, self.end]

    def __eq__(self, other):
        return ((self.start, self.end) == (other.start, other.end))

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        if self.start != other.start:
            return self.start < other.start
        return self.end < other.end

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __repr__(self):
        return " S-E = (%s-%s) H = %s" % (self.start, self.end, self.height)


def testing(s1, s2):
    tmp = s1 + s2
    t2 = []
    for build in tmp:
        # False means we open the interval
        t2.append((build.start, False, build.height))
        # True means we close the interval
        t2.append((build.end, True, build.height))
    t2.sort()
    return t2


def dsk(n, h, w, xmin, xmax):
    sk = Skyline(n, h, w, xmin, xmax)
    print(sk.buildings)
    draw(sk)


if __name__ == "__main__":
    g = [(5, True, 10), (7, True, 10), (1, True, 3), (15, False, 3)]
    # g = [(5, True, 10), (5, False, 10)]
    l1 = [Building(1, 3, 10), Building(12, 4, 15)]
    l2 = [Building(3, 5, 8), Building(4, 7, 5)]

    a = Skyline([Building(1, 1, 2), Building(3, 3, 5), Building(6, 7, 10)])
    b = Skyline([Building(1, 1, 2), Building(2, 2, 3), Building(3, 3, 4)])
    a.draw()

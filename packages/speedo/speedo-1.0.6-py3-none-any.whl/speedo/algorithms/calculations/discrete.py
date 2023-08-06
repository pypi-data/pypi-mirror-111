""" convention
underscore notation and self-changing method
for example:
    boundary1.union(boundary2) returns boundary1 which is modified
    boundary1.union_(boundary2) returns a new boundary object
"""
from speedo.algorithms.calculations.common import one_d


class Boundary:
    def __len__(self):
        return 1

    def __init__(self, rep):
        if rep is None:
            self.front = False
            self.low = float('-inf')
            self.back = False
            self.high = float('inf')
        elif isinstance(rep, Boundary):
            # concat
            self.front = rep.front
            self.low = rep.low
            self.high = rep.high
            self.back = rep.back
        elif isinstance(rep, tuple):
            self.front = False
            self.low = rep[0]
            self.high = rep[1]
            self.back = False
        elif isinstance(rep, list):
            self.front = True
            self.low = rep[0]
            self.high = rep[1]
            self.back = True
        elif isinstance(rep, str):
            exp = rep.replace(' ', '')
            left, right = exp.split(',')
            front, low = left[0], left[1:]
            high, back = right[:-1], right[-1]
            self.low = float(low)
            self.high = float(high)
            if front == '[':
                # include front
                self.front = True
            else:
                self.front = False
            if back == ']':
                self.back = True
            else:
                self.back = False
        else:
            raise TypeError('only str, tuple, list objects allowed')

    def concat(self):
        return Boundary(self)

    @staticmethod
    def parsable_str(text):
        try:
            arr = text.split(',')
            return len(arr) == 2
        except:
            return False

    def __contains__(self, x):
        if self.front:
            # [
            if self.back:
                # ]
                if x < self.low or x > self.high:
                    return False
            else:
                # )
                if x < self.low or x >= self.high:
                    return False
        else:
            # (
            if self.back:
                # ]
                if x <= self.low or x > self.high:
                    return False
            else:
                # )
                if x <= self.low or x >= self.high:
                    return False
        return True

    # self change
    def slice_left(self, low):
        if self.high == low:
            if not self.back:
                # exclude high
                raise ValueError(f'Boundary<{self}> cannot slice left to {low}')
        elif self.high < low:
            raise ValueError(f'Boundary<{self}> cannot slice left to {low}')
        self.front = True
        self.low = low
        return self

    # return new
    def slice_left_(self, low):
        return Boundary(self).slice_left(low)

    def slice_right(self, high):
        if self.low == high:
            if not self.back:
                # exclude high
                raise ValueError(f'Boundary<{self}> cannot slice right to {high}')
        elif self.low > high:
            raise ValueError(f'Boundary<{self}> cannot slice right to {high}')
        self.back = True
        self.high = high
        return self

    def slice_right_(self, high):
        return Boundary(self).slice_right(high)

    """
    str returns exact values
    express(None) returns initial values
    """

    def expression(self, rit=None):
        if self.front:
            front = '['
        else:
            front = '('
        if self.back:
            back = ']'
        else:
            back = ')'
        if isinstance(rit, int):
            if rit == 0:
                try:
                    low = int(round(self.low, rit))
                except OverflowError:
                    low = '-\u221e'
                try:
                    high = int(round(self.high, rit))
                except OverflowError:
                    high = '\u221e'
            else:
                try:
                    low = round(self.low, rit)
                except OverflowError:
                    low = '-\u221e'
                try:
                    high = round(self.high, rit)
                except OverflowError:
                    high = '\u221e'
        else:
            if self.low == float('-inf'):
                low = '-\u221e'
            else:
                low = self.low
            if self.high == float('inf'):
                high = '\u221e'
            else:
                high = self.high
        return f'{front}{low}, {high}{back}'

    def __str__(self):
        return self.expression(0)

    def __repr__(self):
        # variables
        return f'front [{self.front}]\tlow [{self.low}]\thigh [{self.high}]\tback[{self.back}]'

    def has_infinity(self):
        return self.low == float('-inf') or self.high == float('inf')

    def infinity_both(self):
        return self.low == float('-inf') and self.high == float('inf')

    # bool
    def infinity_left(self):
        return self.low == float('-inf')

    # self change
    def union(self, boundary):
        if isinstance(boundary, Boundary):
            # left
            if self.low > boundary.low:
                self.low = boundary.low
                self.front = boundary.front
            elif self.low == boundary.low:
                if self.front or boundary.front:
                    self.front = True
            # right
            if self.high < boundary.high:
                self.high = boundary.high
                self.back = boundary.high
            elif self.high == boundary.high:
                if self.back or boundary.back:
                    self.back = True
        elif isinstance(boundary, Lim):
            nlim = Lim(boundary)
            nlim.union(self)
            self.low = None
            self.high = None
            self.front = None
            self.back = None
            self.__class__ = Lim
            self.boundaries = nlim.boundaries
        return self

    def touch_on_left(self, boundary):
        return ((self.back and not boundary.front) or (not self.back and boundary.front)) and (self.high == boundary.low)

    def touch_on_right(self, boundary):
        return ((self.front and not boundary.back) or (not self.front and boundary.back)) and (self.low == boundary.high)

    # self change
    def merge_to_left(self, boundary):
        self.high = boundary.high
        self.back = boundary.back
        return self

    def merge_to_right(self, boundary):
        self.low = boundary.low
        self.front = boundary.front
        return self

    def merge_to_left_(self, boundary):
        return Boundary(self).merge_to_left(boundary)

    def merge_to_right_(self, boundary):
        return Boundary(self).merge_to_right(boundary)

        # return bool
    def has_intersect_with(self, domain):
        dm = domain_initializer(domain)
        if isinstance(dm, Boundary):
            # self is on the left of boundary
            if self.low < dm.low:
                if self.high == dm.low:
                    return self.back and dm.front
                return self.high > dm.low
            # self is on the right of boundary
            elif self.low > dm.high:
                if self.low == dm.high:
                    return self.front and dm.back
                return self.low < dm.high
            # self right touches on boundary left
            elif self.high == dm.low:
                return self.back and dm.front
            # self left touches on boundary right
            elif self.low == dm.high:
                return self.front and dm.back
            # self is in the middle of boundary
            return True
        elif isinstance(dm, Lim):
            for bd in dm.boundaries:
                if self.has_intersect_with(bd):
                    return True
            return False
        else:
            raise TypeError('<Boundary> has_intersect_with only accept Boundary or Lim')

    # self change
    def intersect(self, boundary):
        if isinstance(boundary, Boundary):
            # left
            if self.low < boundary.low:
                self.low = boundary.low
                self.front = boundary.front
            elif self.low == boundary.low:
                if (not self.front) or (not boundary.front):
                    self.front = False
            # right
            if self.high > boundary.high:
                self.high = boundary.high
                self.back = boundary.back
            elif self.high == boundary.high:
                if (not self.back) or (not boundary.back):
                    self.back = False
        elif isinstance(boundary, Lim):
            nlim = Lim(boundary)
            nlim.intersect(self)
            self.__class__ = Lim
            self.low = None
            self.high = None
            self.front = None
            self.back = None
            self.boundaries = nlim.boundaries
        return self

    # create new
    def union_(self, boundary):
        return Boundary(self).union(boundary)

    # create new
    def intersect_(self, boundary):
        return Boundary(self).intersect(boundary)

    def length(self):
        return self.high - self.low + 1

    def linespace(self, n):
        # include edge value
        if self.low == self.high:
            return [self.low]
        step = (self.high - self.low) / (n - 1)
        res = []
        for ii in range(n):
            res.append(self.low + step * ii)
        if not self.front:
            # (
            res[0] += step / 5
        if not self.back:
            # )
            res[-1] -= step / 5
        return res

    # solid or empty dot to indicate front and back
    def marker(self):
        res = {'solid': [], 'empty': []}
        if self.front:
            res['solid'].append(self.low)
        else:
            res['empty'].append(self.low)
        if self.back:
            res['solid'].append(self.high)
        else:
            res['empty'].append(self.high)
        return res

    def __add__(self, other):
        nbd = Boundary(self)
        nbd += other
        return nbd

    def __iadd__(self, other: int or float):
        self.low += other
        self.high += other
        return self

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        nbd = Boundary(self)
        nbd -= other
        return nbd

    def __isub__(self, other):
        self.low -= other
        self.high -= other
        return self

    # support negative multiplication, division, exponential
    def ensure(self, v1, v2):
        if v1 < v2:
            self.low = v1
            self.high = v2
        else:
            self.low = v2
            self.high = v1
        return self

    def __mul__(self, other):
        nbd = Boundary(self)
        nbd *= other
        return nbd

    def __imul__(self, other):
        return self.ensure(self.low * other, self.high * other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        nbd = Boundary(self)
        nbd /= other
        return nbd

    def __itruediv__(self, other):
        return self.ensure(self.low / other, self.high / other)

    def __floordiv__(self, other):
        nbd = Boundary(self)
        nbd //= other
        return nbd

    def __ifloordiv__(self, other):
        return self.ensure(self.low // other, self.high // other)

    def __pow__(self, power, modulo=None):
        nbd = Boundary(self)
        nbd **= power
        return nbd

    def __ipow__(self, other):
        return self.ensure(self.low ** other, self.high ** other)

    @property
    def left(self):
        if self.front:
            return self.low + 0.01 * (self.high - self.low)
        else:
            return self.low

    @property
    def right(self):
        if self.back:
            return self.high - 0.01 * (self.high - self.low)
        else:
            return self.high

    def filter(self, xs, *yl):
        xn = []
        ynl = [[] for ys in yl]
        for ii, xx in enumerate(xs):
            if xx in self:
                xn.append(xx)
                for jj in range(len(yl)):
                    ynl[jj].append(yl[jj][ii])
        return [xn, ynl]

    # pass in asymptote to exclude in domain
    def exclude_one(self, val):
        if val in self and self.low != val and self.high != val:
            lft, rgt = self.expression().split(',')
            if self.has_infinity():
                if self.infinity_both():
                    lft, rgt = '(-inf', 'inf)'
                elif self.infinity_left():
                    lft = '(-inf'
                else:
                    rgt = 'inf)'
            nlim = Lim(Boundary(lft + ',' + str(val) + ')'), Boundary('(' + str(val) + ',' + rgt))
            self.low = None
            self.high = None
            self.front = None
            self.back = None
            self.__class__ = Lim
            self.boundaries = nlim.boundaries
        return self

    def exclude_boundary(self, boundary):
        bds = []
        if not self.has_intersect_with(boundary):
            return Lim(self)
        else:
            if self.low < boundary.low:
                if boundary.front:
                    br = ')'
                else:
                    br = ']'
                bds.append(Boundary(self.expression().split(',')[0] + ', ' + str(boundary.low) + br))
            elif self.low == boundary.low:
                if self.front and not boundary.front:
                    # [ exclude (
                    bds.append(Boundary([self.low, self.low]))

            if self.high > boundary.high:
                if boundary.back:
                    br = '('
                else:
                    br = '['
                bds.append(Boundary(br + str(boundary.high) + ', ' + self.expression().split(',')[1]))
            elif self.high == boundary.high:
                if self.back and not boundary.back:
                    # ] exclude )
                    bds.append(Boundary([self.high, self.high]))
        nlim = Lim(*bds)
        self.low = None
        self.high = None
        self.front = None
        self.back = None
        self.__class__ = Lim
        self.boundaries = nlim.boundaries
        return self

    def exclude_lim(self, li):
        for bd in li.boundaries:
            self.exclude_boundary(bd)
        return self

    def exclude(self, *val):
        for va in val:
            if isinstance(va, list) or isinstance(va, tuple):
                for vv in va:
                    self.exclude_one(vv)
            elif isinstance(va, int) or isinstance(va, float):
                self.exclude_one(va)
            elif isinstance(va, Boundary):
                self.exclude_boundary(va)
            elif isinstance(va, Lim):
                self.exclude_lim(va)
            else:
                unp = domain_initializer(va)
                if isinstance(unp, Boundary):
                    self.exclude_boundary(unp)
                elif isinstance(unp, Lim):
                    self.exclude_lim(unp)
        return self


class Lim:
    # discrete boundary
    def __init__(self, *args):
        self.boundaries = []
        if len(args) == 1 and isinstance(args[0], Lim):
            # concat
            for bd in args[0].boundaries:
                self.boundaries.append(Boundary(bd))
        else:
            for arg in args:
                if isinstance(arg, Lim):
                    for bd in arg.boundaries:
                        self.append(bd)
                else:
                    self.append(arg)

    def __len__(self):
        return len(self.boundaries)

    def concat(self):
        return Lim(self)

    def __contains__(self, x):
        for bd in self.boundaries:
            if x in bd:
                return True
        return False

    def expression(self, rit=None):
        res = ''
        for bd in self.boundaries:
            res += bd.expression(rit)
            res += ' U '
        return res[:-3]

    def __str__(self):
        def str_mapper(bd):
            return str(bd)
        return ' U '.join(map(str_mapper, self.boundaries))

    def __repr__(self):
        res = '<Lim \n'
        for bd in self.boundaries:
            res += '\t' + repr(bd) + '\n'
        return res + '>\n'

    def has_infinity(self):
        for bd in self.boundaries:
            if bd.has_infinity():
                return True
        return False

    def infinity_both(self):
        self.simple()
        left = False
        right = False
        for bd in self.boundaries:
            if bd.low == float('-inf'):
                left = True
            if bd.high == float('inf'):
                right = True
        return left and right

    def infinity_left(self):
        for bd in self.boundaries:
            if bd.infinity_left():
                return True
        return False

    def slice_left(self, low):
        self.simple().sort()
        most = self.boundaries[-1]
        if most.high < low:
            raise ValueError(f'Lim<{self}> cannot slice left to {low}')
        elif most.high == low:
            if not most.back:
                raise ValueError(f'Lim<{self}> cannot slice left to {low}')
        bds = []
        flag = False
        for bd in self.boundaries:
            if flag:
                bds.append(bd)
            elif not (low > bd.high or (low == bd.high and not bd.back)):
                flag = True
                bd.slice_left(low)
                bds.append(bd)
        if not flag:
            raise ValueError(f'Lim<{self}> cannot slice left to {low}')
        self.boundaries = bds
        return self.simple().sort()

    def slice_left_(self, low):
        return Lim(self).slice_left(low)

    # slice right
    # set flag = False
    # count from last to first, if value is on left on bd, remove bd
    # if a bd satisfy condition, change it, set flag to True
    # end of iteration, if flag is False, raise error
    def slice_right(self, high):
        self.simple().sort()
        least = self.boundaries[0]
        if least.low > high:
            raise ValueError(f'Lim<{self}> cannot slice right to {high}')
        elif least.low == high:
            if not least.front:
                raise ValueError(f'Lim<{self}> cannot slice right to {high}')
        bds = []
        flag = False
        for bd in reversed(self.boundaries):
            if flag:
                bds.append(bd)
            elif not (high < bd.low or (high == bd.low and not bd.front)):
                flag = True
                bd.slice_right(high)
                bds.append(bd)
        if not flag:
            raise ValueError(f'Lim<{self}> cannot slice right to {high}')
        self.boundaries = bds
        return self.simple().sort()

    def slice_right_(self, high):
        return Lim(self).slice_right(high)

    '''
    self.boundaries.append direct add to boundaries list
    self.append check if any existing boundary is union-able (has intersect) with new one
    '''

    # self change
    def append(self, boundary):
        unioned = False
        for bd in self.boundaries:
            if boundary.has_intersect_with(bd):
                bd.union(boundary)
                unioned = True
            elif bd.touch_on_left(boundary):
                bd.merge_to_left(boundary)
                unioned = True
            elif bd.touch_on_right(boundary):
                bd.merge_to_right(boundary)
                unioned = True
        if not unioned:
            self.boundaries.append(boundary)
        return self

    # create new
    def append_(self, boundary):
        return Lim(self).append(boundary)

    # self change
    def sort(self):
        def find_min(bds):
            lows = []
            for bd in bds:
                lows.append(bd.low)
            return bds.pop(lows.index(min(lows)))
        self.boundaries = [find_min(self.boundaries) for ii in range(len(self.boundaries))]
        return self

    # create new
    def sort_(self):
        return Lim(self).sort()

    def length(self):
        return sum([bd.length() for bd in self.boundaries])

    def linespace(self, n):
        res = []
        length = self.length()
        for bd in self.boundaries:
            portion = round(n * bd.length() / length)
            if portion < 2:
                portion = 2
            res.append(bd.linespace(portion))
        return res

    def marker(self):
        res = {'solid': [], 'empty': []}
        for bd in self.boundaries:
            mk = bd.marker()
            for solid in mk['solid']:
                res['solid'].append(solid)
            for empty in mk['empty']:
                res['empty'].append(empty)
        res['solid'].sort()
        res['empty'].sort()
        return res

    # self change
    def simple(self):
        boundaries = [bd for bd in self.boundaries]
        self.boundaries = []
        for bd in boundaries:
            self.append(bd)
        return self.sort()

    def has_intersect_with(self, domain):
        dm = domain_initializer(domain)
        if isinstance(dm, Boundary):
            for bd in self.boundaries:
                if bd.has_intersect_with(dm):
                    return True
            return False
        elif isinstance(dm, Lim):
            for bd in self.boundaries:
                for ld in dm.boundaries:
                    if bd.has_intersect_with(ld):
                        return True
            return False
        else:
            raise TypeError('<Lim> has_intersect_with only accept Boundary or Lim')

    # self change
    def intersect(self, domain):
        bds = []
        if isinstance(domain, Boundary):
            for bd in self.boundaries:
                if bd.has_intersect_with(domain):
                    bds.append(bd.intersect_(domain))
        elif isinstance(domain, Lim):
            for bd1 in self.boundaries:
                for bd2 in domain.boundaries:
                    if bd1.has_intersect_with(bd2):
                        bds.append(bd1.intersect_(bd2))
        self.boundaries = []
        for bd in bds:
            self.append(bd)
        return self

    # return new
    def intersect_(self, domain):
        return Lim(self).intersect(domain)

    # self change
    def union(self, domain):
        if isinstance(domain, Boundary):
            self.append(domain)
        elif isinstance(domain, Lim):
            for bd in domain.boundaries:
                self.append(bd)
        return self.simple()

    # return new
    def union_(self, domain):
        return Lim(self).union(domain)

    def __add__(self, other):
        nlim = Lim(self)
        nlim += other
        return nlim

    def __iadd__(self, other):
        for bd in self.boundaries:
            bd += other
        return self.simple()

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        nlim = Lim(self)
        nlim -= other
        return nlim

    def __isub__(self, other):
        for bd in self.boundaries:
            bd -= other
        return self.simple()

    def __mul__(self, other):
        nlim = Lim(self)
        nlim *= other
        return nlim

    def __imul__(self, other):
        for bd in self.boundaries:
            bd *= other
        return self.simple()

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        nlim = Lim(self)
        nlim /= other
        return nlim

    def __itruediv__(self, other):
        for bd in self.boundaries:
            bd /= other
        return self.simple()

    def __floordiv__(self, other):
        nlim = Lim(self)
        nlim //= other
        return nlim

    def __ifloordiv__(self, other):
        for bd in self.boundaries:
            bd //= other
        return self.simple()

    def __pow__(self, power, modulo=None):
        nlim = Lim(self)
        nlim **= power
        return nlim

    def __ipow__(self, other):
        for bd in self.boundaries:
            bd **= other
        return self.simple()

    @property
    def left(self):
        return self.simple().sort().boundaries[0].left

    @property
    def right(self):
        return self.simple().sort().boundaries[-1].left

    def filter(self, xs, *yl):
        self.simple()
        rx = []
        ryl = [[] for ys in yl]
        for bd in self.boundaries:
            xr, ylr = bd.filter(xs, *yl)
            rx += xr
            for ii in range(len(ylr)):
                ryl[ii] += ylr[ii]
        return [rx, ryl]

    def exclude_boundary(self, boundary):
        nlim = Lim(*one_d([lm.boundaries for lm in one_d([bd.exclude_boundary(boundary) for bd in self.boundaries])]))
        self.boundaries = nlim.boundaries
        return self.simple().sort()

    def exclude_lim(self, lim):
        for bd in lim.boundaries:
            self.exclude_boundary(bd)
        return self

    def exclude_one(self, va):
        nbd = [bd.exclude(va) for bd in self.boundaries]
        self.boundaries = []
        nlim = Lim(*nbd)
        self.boundaries = [bd for bd in nlim.boundaries]
        return self

    def exclude(self, *val):
        for va in val:
            if isinstance(va, list) or isinstance(va, tuple):
                for vv in va:
                    self.exclude_one(vv)
            elif isinstance(va, int) or isinstance(va, float):
                self.exclude_one(va)
            elif isinstance(va, Boundary):
                self.exclude_boundary(va)
            elif isinstance(va, Lim):
                self.exclude_boundary(va)
            else:
                unp = domain_initializer(va)
                if isinstance(unp, Boundary):
                    self.exclude_boundary(unp)
                elif isinstance(unp, Lim):
                    self.exclude_lim(unp)
        return self


def domain_initializer(unparsed):
    try:
        if isinstance(unparsed, Boundary) or isinstance(unparsed, Lim):
            return unparsed
        elif (isinstance(unparsed, list) or isinstance(unparsed, tuple)) and (isinstance(unparsed[0], list) or isinstance(unparsed[0], tuple) or Boundary.parsable_str(unparsed[0])):
            # init as Lim
            return Lim(*[Boundary(bd) for bd in unparsed])
        else:
            # init as Boundary
            return Boundary(unparsed)
    except:
        raise TypeError('Boundary object must be inited by a string, a list, or tuple, or a nested list represents discrete union set')


if __name__ == '__main__':
    pass
    # print(domain_initializer([1, 2]))
    # b1 = Boundary('[-10, 2)')
    # l1 = Lim(b2, b1)
    # print(l1.sort().boundaries[0])
    # print(l1.sort().boundaries[1])
    # print(l1.calculations(None))
    # print(repr(l1))
    # print(b2.union_(b1).calculations(0))
    # print(b2.has_intersect_with(b1))
    # print(l1.linespace(10))
    # print(l1.marker())
    # b3 = b1 * 3
    # print(b3)
    # print(l1)
    # l2 = l1 ** 2
    # print(l2)

    # b1 = domain_initializer(['[-4, 5)', [6, 10]])
    # b2 = Boundary([2, 10])

    # b1 = Boundary([-4, 10])
    # b2 = Boundary([7, 10])

    # print(b1)
    # print(b2 ** -2)
    # print(b1)
    # print(domain_initializer('[-inf, 1)'))

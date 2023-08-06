import random
from speedo.algorithms.regression.mono import Mono


class DataFrame:
    """
        {
            0: [  [ [x..], [y..] ], [ [x..], [y..] ] ..  ],
            1: ..
        }
    """

    def __init__(self):
        self.di = {}
        # ind auto increment, used as key of di
        self.ind = None
        # index for access parent level, always 1 less than ind
        self.at = 0

    # illustrate self.di
    def __str__(self):
        kk = list(self.di.keys())
        vv = list(self.di.values())
        st = '<DataFrame>'
        for ii, dd in enumerate(kk):
            st += f'\n\t{dd} <{len(vv[ii])}-{len(vv[ii][0])}>:\t{vv[ii]}'
        st += '\n'
        return st

    # instance is treated as dictionary
    def __getitem__(self, item):
        return self.di[item]

    # modifiable value
    def __setitem__(self, key, value):
        self.di[key] = value

    # ind = which is the length of the xy vars minus one
    # call with ind at once, then call without ind
    def new(self, ind=None):
        if ind is not None:
            self.ind = ind
            self.at = ind + 1
        else:
            if self.ind is None:
                raise ValueError('DataFrame new method must be initialized with a value at start')
            elif self.ind == 0:
                raise OverflowError('DataFrame dictionary value exceeded to be negative')
            self.ind -= 1
        self.di[self.ind] = []

    # add new array to the dictionary by key entry
    def add(self, arr):
        if arr not in self.di[self.ind]:
            self.di[self.ind].append(arr)

    # add last array to the dictionary by key entry
    # callbacks map x y values onto generated natural indices
    def finish(self, arr, x_callback, y_callback):
        if arr not in self.di[self.ind]:
            self.di[self.ind].append(arr)
            x_callback(arr)
            y_callback(arr)

    # at di parent level
    # yields last finished-adding array
    def parent(self):
        self.at -= 1
        for item in self.di[self.at]:
            yield item

    # clear variables of instance to release storage
    def destruct(self):
        self.di = {}
        self.ind = None
        self.at = 0


class Slicer:
    """ generate minimum vertexes for regression """

    # generates array of (length - 1) items
    # natural number representing indices
    @staticmethod
    def avoid(length):
        for d in range(length):
            res = [xx for xx in range(length)]
            res.remove(d)
            yield res

    # pass in length n array, yields n arrays with length of n - 1
    @staticmethod
    def escape(arr):
        for arg in arr:
            res = [xx for xx in arr]
            res.remove(arg)
            yield res

    # convert x or y values based on natural indices rule
    @staticmethod
    def after(rule, val):
        return [val[xx] for xx in rule]

    # [0, 1, 2, 3, 4] -> [0, 4, 1, 3, 2] ?rev-> [2, 3, 1, 4, 0]
    # normalize sparse data
    # reversed: from center to edge
    @staticmethod
    def tail(arr, rev):
        res = []
        ii = -1
        while ii != int((len(arr) - 1) / 2):
            ii += 1
            res.append(arr[ii])
            res.append(arr[-1 - ii])

        if len(arr) % 2 != 0:
            res.pop()

        if rev:
            return list(reversed(res))
        else:
            return res

    # params: x values, y values, grouping length
    def __init__(self, x_val, y_val, required):
        if len(x_val) != len(y_val):
            raise ValueError(f'Length InConsistent: x_val<{len(x_val)}> | y_val<{len(y_val)}>')
        if required < 1 or required > len(x_val):
            raise ValueError(f'required less than 2 or larger than array length<{len(x_val)}>')
        self.x_val = x_val
        self.y_val = y_val
        self.required = required

        self.length = len(x_val)
        self.demand = len(x_val)
        self.gen = Slicer.avoid(self.length)
        self.data = DataFrame()
        self.x = []
        self.y = []

    # pass in rule, add actual values in x and y
    def x_callback(self, rule):
        self.x.append(Slicer.after(rule, self.x_val))

    def y_callback(self, rule):
        self.y.append(Slicer.after(rule, self.y_val))

    # CORE: get vertex array
    # rev<True>: from center to edge
    def initialize(self, rev):
        # first iteration of data adding
        # initialize data frame by passing ind to self.data
        self.demand -= 1
        self.data.new(self.length - 1)
        if self.demand == self.required:
            for a in self.gen:
                self.data.finish(a, self.x_callback, self.y_callback)
        else:
            for a in self.gen:
                self.data.add(a)

        if self.demand != self.required:
            # main iteration
            while self.demand != self.required + 1:
                self.demand -= 1
                self.data.new()
                for b in self.data.parent():
                    self.gen = Slicer.escape(b)
                    for c in self.gen:
                        self.data.add(c)

            # last iteration of data adding
            self.demand -= 1
            self.data.new()
            for b in self.data.parent():
                self.gen = Slicer.escape(b)
                for c in self.gen:
                    # finish differs from add
                    # takes two more callbacks as collector of self x_val and y_val
                    self.data.finish(c, self.x_callback, self.y_callback)

        # clear storage by destruct data frame
        self.data.destruct()

        # taking set from equal distance to the center
        self.x = Slicer.tail(self.x, rev)
        self.y = Slicer.tail(self.y, rev)

    # GENERATOR, yield [[x1, x2..], [y1, y2..]] of equal length of required at each time
    # rev<True>: from center to edge
    # rev<False>: from edge to center
    def slicer(self, rev):
        if self.required == self.length:
            for i in range(1):
                yield [[xx for xx in self.x_val], [yy for yy in self.y_val]]
        else:
            self.initialize(rev)
            for ii, xx in enumerate(self.x):
                yy = self.y[ii]
                yield [xx, yy]


class Brief(Slicer):
    """ extract most representative data from raw """

    @staticmethod
    def factorial(num):
        if num == 0:
            return 1
        val = 1
        for i in range(num):
            val *= i + 1
        return val

    @staticmethod
    def reduce(row, col):
        return int(Brief.factorial(row) / (Brief.factorial(col) * Brief.factorial(row - col)))

    # estimate a suitable row as extract amount of raw data
    @staticmethod
    def estimate(required, many):
        ii = -1
        while True:
            ii += 1
            if Brief.reduce(ii, required) > many:
                return ii - 1

    # estimate where should step up by one as insertion
    @staticmethod
    def fit_index(larger, smaller):
        if smaller == 0:
            return []
        stp = larger / smaller
        hst = round(0.5 * stp)
        res = []
        for ii in range(smaller):
            res.append(int((ii + 1) * stp - hst))
        return res

    # condense array into a length of row
    @staticmethod
    def extract(array, row, avg):
        if len(array) <= row:
            return array
        left = len(array) % row
        stp = round((len(array) - left) / row)
        res = []
        fit_in = Brief.fit_index(row, left)
        acc = 0
        for i in range(row):
            try:
                if i == fit_in[acc]:
                    acc += 1
            except IndexError:
                pass
            if avg:
                res.append(sum(array[i * stp + acc:(i + 1) * stp + acc]) / stp)
            else:
                res.append(array[i * stp + acc])

        return res

    # many: data length
    # if avg is True, take average of data
    # otherwise select from raw data
    def __init__(self, x_val, y_val, required, many, avg):
        # pascals triangle, find row with known col and max result
        self.many = many
        self.row = Brief.estimate(required, many)
        super(Brief, self).__init__(
            Brief.extract(x_val, self.row, avg),
            Brief.extract(y_val, self.row, avg),
            required,
        )


class Param:
    def __init__(self, specified, **kwargs):
        self.specified = specified
        self.kwargs = kwargs

    def set(self, **kwargs):
        self.kwargs = kwargs

    def get(self, key):
        return self.kwargs[key]

    def param(self):
        di = {}
        for kk, vv in self.kwargs.items():
            if kk not in self.specified:
                di[kk] = vv
        return di


class Vector:
    """
    x and v values versus dots

    properties
        * x values: [x1, x2 ..]
        * y values: [y1, y2 ..]
        * dots: [[x1, y1], [x2, y2] ..]
        * centroid: [x, y]
    """

    # convert x y to dots
    @staticmethod
    def to_dots(x_val, y_val):
        dots = []
        for i, d in enumerate(x_val):
            dots.append([d, y_val[i]])
        return dots

    # convert dots to x y
    @staticmethod
    def to_xy(dots):
        x_val = []
        y_val = []
        for dt in dots:
            x_val.append(dt[0])
            y_val.append(dt[1])
        return [x_val, y_val]

    # params two dimensional dots [[x, y], [x, y]...]
    # return centroid [x, y]
    @staticmethod
    def centroid(dots):
        rx = 0
        ry = 0
        for dot in dots:
            rx += dot[0]
            ry += dot[1]
        return [float(rx) / len(dots), float(ry) / len(dots)]

    # either initialize by x and y values or dots
    def __init__(self, x_val=None, y_val=None, dots=None):
        # graphs
        self.kwargs = Param(['label_shift_xy', 'xy_up', 'xy_down'], label_shift_xy=(0, 0), xy_up=(0, 0),
                            xy_down=(0, 0))  # passed into plt.graph, set by set
        if [x_val, y_val].count(None) == 1 or \
                [x_val, y_val, dots].count(None) == 3 or \
                [x_val, y_val, dots].count(None) == 0:
            raise ValueError('Vector: Either pass in x and y values or dots')
        if dots is None:
            self.x_val = x_val
            self.y_val = y_val
            self.dots = Vector.to_dots(x_val, y_val)
        else:
            self.x_val, self.y_val = Vector.to_xy(dots)
            self.dots = dots

    # set kwargs to pass into plotting graph
    def set(self, **kwargs):
        self.kwargs.set(**kwargs)
        return self

    def get(self, key):
        return self.kwargs.get(key)

    def round(self, rit):
        self.x_val = [round(xx, rit) for xx in self.x_val]
        self.y_val = [round(yy, rit) for yy in self.y_val]
        self.dots = [[round(xx, rit), round(self.y_val[ii], rit)] for ii, xx in enumerate(self.x_val)]
        return self

    @property
    def center(self):
        return Vector.centroid(self.dots)

    def concat(self):
        return Vector(x_val=[xx for xx in self.x], y_val=[yy for yy in self.y])

    def __str__(self):
        st = '<Vector>'
        for ss, vv in [
            ['x_val', self.x_val],
            ['y_val', self.y_val],
            ['dots', self.dots],
        ]:
            st += f'\n\t.{ss}: {vv}'
        st += '\n'
        return st

    def __len__(self):
        return len(self.x_val)

    @property
    def x(self):
        return [xx for xx in self.x_val]

    @property
    def y(self):
        return [xx for xx in self.y_val]

    @property
    def dt(self):
        return [[xx, yy] for xx, yy in self.dots]

    # return Vector that sum xs eq sum ys eq 100
    def percent(self):
        return Vector(
            x_val=[xe / sum(self.x_val) * 100 for xe in self.x_val],
            y_val=[ye / sum(self.y_val) * 100 for ye in self.y_val],
        )

    def sample(self, n):
        if n > len(self.x_val):
            n = len(self.x_val)
        each = len(self.x_val) / n
        rdt = [[self.dots[0][0], self.dots[0][1]]]
        for ii, dd in enumerate(self.dots):
            if round(each) == ii:
                rdt.append([dd[0], dd[1]])
                each += each
        return Vector(dots=rdt)

    # get rid of duplicated dots, return a new Vector
    def single(self):
        dots = []
        for dt in self.dots:
            if dt not in dots:
                dots.append(dt)
        return Vector(dots=dots)

    def mono(self, operate='<', x=True, y=True):
        if x:
            m1 = Mono(array=self.x, operate=operate, along=self.y).mono
            self.x_val = m1['array']
            self.y_val = m1['along']
        if y:
            m1 = Mono(array=self.y, operate=operate, along=self.x).mono
            self.y_val = m1['array']
            self.x_val = m1['along']
        return self

    def __iter__(self):
        for dt in self.dots:
            yield dt

    def min(self, x=False, y=False):
        if x:
            return min(self.x_val)
        elif y:
            return min(self.y_val)
        else:
            raise ValueError('<Vector> min or max must have either x or y set to True')

    def max(self, x=False, y=False):
        if x:
            return max(self.x_val)
        elif y:
            return max(self.y_val)
        else:
            raise ValueError('<Vector> min or max must have either x or y set to True')

    def average(self, x=False, y=False):
        if x:
            return sum(self.x_val) / len(self.x_val)
        elif y:
            return sum(self.y_val) / len(self.y_val)
        else:
            raise ValueError('<Vector> average must have either x or y set to True')


class Preset:
    """ Monotone both x and y values """

    # return either > or <
    @staticmethod
    def linear_trend_operate(arr):
        le = 0
        ge = 0
        for ii in range(len(arr) - 1):
            if arr[ii] < arr[ii + 1]:
                le += 1
            elif arr[ii] > arr[ii + 1]:
                ge += 1
        if le > ge:
            return '<'
        else:
            return '>'

    # take vector as arg, return vector
    # x|y_mono -> bool: decide whether to regulate x|y monotonicity
    def __init__(self, x_mono, y_mono, x_val=None, y_val=None, dots=None):
        vector = Vector(x_val=x_val, y_val=y_val, dots=dots)
        if not x_mono:
            self.vector = vector
        else:
            x_op = Preset.linear_trend_operate(vector.x)
            mo = Mono(array=x_val, operate=x_op, along=y_val).mono
            x_nv = mo['array']
            y_nv = mo['along']

            if y_mono:
                y_op = Preset.linear_trend_operate(y_nv)
                mon = Mono(array=y_nv, operate=y_op, along=x_nv).mono

                y_res = mon['array']
                x_res = mon['along']

                self.vector = Vector(x_val=x_res, y_val=y_res)
            else:
                self.vector = Vector(x_val=x_nv, y_val=y_nv)


class Regression(Preset):
    """
    Similarities of all regression:
        * the line is assumed to always passes the center
    """

    @staticmethod
    def store(x_val, y_val, dots):
        vt = Vector(x_val=x_val, y_val=y_val, dots=dots)
        xs = vt.x
        ys = vt.y
        if Expression.DATA is None:
            if isinstance(Expression.SIZE, int):
                if Expression.SIZE >= len(vt):
                    Expression.DATA = vt.concat()
                else:
                    Expression.DATA = Vector(
                        x_val=Brief.extract(array=xs, row=Expression.SIZE, avg=False),
                        y_val=Brief.extract(array=ys, row=Expression.SIZE, avg=False),
                    )
            elif isinstance(Expression.DATA, float):
                if Expression.SIZE < 0 or Expression.SIZE > 1:
                    raise ValueError(
                        '\n'.join([
                            "Sample Size as a float representing what's the percentage of data take into account",
                            f"It can't be out of domain [0, 1], invalid value {Expression.SIZE},",
                            "call set_sample_size() before regression to change it"
                        ])
                    )
                siz = int(Expression.SIZE * len(vt))
                Expression.DATA = Vector(
                    x_val=Brief.extract(array=xs, row=siz, avg=False),
                    y_val=Brief.extract(array=ys, row=siz, avg=False),
                )
            else:
                raise TypeError(
                    '\n'.join([
                        'Sample Size can either be a float which is percentage or an int which is exact number',
                        'it is used in result matching calculation, smaller number makes quicker calculation',
                        'Default to 20',
                    ])
                )

    @staticmethod
    def initial(vt):
        if vt:
            Expression.INITIAL = vt.concat()

    # rev<True>: from center to edge
    # rev<False>: from edge to center
    # x_mono -> false: no regulation
    # y_mono -> true: y_reg(x_reg(val))
    # y_mono -> false: x_reg(val)
    # avg -> true: take average of data
    # avg -> false: select from raw data
    def __init__(
            self,
            required,
            many,
            centered,
            avg,
            x_mono,
            y_mono,
            x_val=None,
            y_val=None,
            dots=None,
            rev=False,
            initial_vector=None,  # help inverse exponential
    ):
        # store data in Expression class variable for finish comparison usage
        Regression.initial(initial_vector)
        Regression.store(x_val=x_val, y_val=y_val, dots=dots)
        super().__init__(
            x_mono=x_mono,
            y_mono=y_mono,
            x_val=x_val,
            y_val=y_val,
            dots=dots,
        )
        self.required = required
        if centered:
            req = self.required - 1
        else:
            req = self.required
        self.slice = Brief(
            x_val=self.vector.x,
            y_val=self.vector.y,
            required=req,
            many=many,
            avg=avg,
        ).slicer(rev)
        self.centered = centered

    # params
    #  xy -> [[x1, x2..], [y1, y2..]]
    #  cen -> [x, y]
    # return
    #  vector -> [[x1, x2, x..], [y1, y2, y..]] | [[x, y], [x1, y1], [x2, y2]..]
    @staticmethod
    def join(xy, cen):
        x_vars = [xx for xx in xy[0]]
        x_vars.append(cen[0])
        y_vars = [yy for yy in xy[1]]
        y_vars.append(cen[1])
        return Vector(x_val=x_vars, y_val=y_vars)

    # generate vector object of required length
    # notice dots always contains center
    def eject(self):
        if self.centered:
            for sl in self.slice:
                yield Regression.join(sl, self.vector.center)
        else:
            for sl in self.slice:
                yield Vector(
                    x_val=[xx for xx in sl[0]],
                    y_val=[yy for yy in sl[1]],
                )


class Comparison:
    """ static class as variable collector """

    EXPRESSIONS = []

    def __init__(self, expression):
        Comparison.EXPRESSIONS.append(expression)

    # return the most accurate regressed calculations obj
    # should be called after regression are done and all expressions are evaluated
    @staticmethod
    def compare():
        return min(Comparison.EXPRESSIONS)

    @staticmethod
    def forget():
        Comparison.EXPRESSIONS = []


class Expression:
    """ formula representing regressed data """
    DATA = None
    INITIAL = None
    SIZE = 20
    SAMPLE_RATE = 10

    # evaluating percentage of similarity
    @staticmethod
    def discrete(arr):
        length = float(len(arr))
        mean = sum(arr) / length
        dif = 0
        for ar in arr:
            dif += abs(ar - mean)
        return dif / length

    # Expression is inited when we got kwargs as, for example,
    # {hook:<func>, a:[1, 2], b: [3, 4], pro:1, y_exp:1}
    # coefficients are solitary alphabet
    # after separation, use each set of dots to work out y value,
    # compare it to what it should be from sample data
    # get an efficiency, the lower, the more matching
    def __init__(self, **kwargs):
        self.category = None  # e.g. Linear
        effect = None
        su = None
        self.coe = {}
        # avg: {k: 2, b: 3}
        self.recorders = {}
        # all data: {k: [1, 2, 3], b: [2, 3, 4]}
        self.param_error = {}
        self.length = 0
        self.variables = []
        self.hook = kwargs['hook']
        del kwargs['hook']
        del_keys = []
        if Expression.INITIAL:
            initial_vector = Expression.INITIAL.sample(Expression.SAMPLE_RATE)
        else:
            initial_vector = Expression.DATA.sample(Expression.SAMPLE_RATE)
        for kk in kwargs.keys():
            if len(kk) != 1:
                del_keys.append(kk)
                self.variables.append(kwargs[kk])
        for kk in del_keys:
            del kwargs[kk]
        for uk in range(len(list(kwargs.values())[0])):
            sub = {}
            for lk in kwargs.keys():
                sub[lk] = kwargs[lk][uk]
            fo = self.inspect(list(sub.values()) + self.variables)
            eum = 0
            for ii, xv in enumerate(initial_vector.x):
                try:
                    eum += abs(initial_vector.y[ii] - fo(xv))
                except ZeroDivisionError:
                    pass
            evg = eum / Expression.SAMPLE_RATE
            if effect is None or evg < effect:
                effect = evg
                su = sub
        self.coe = su
        self.sum_param_error = sum(self.param_error.values())
        self.efficiency = effect

    def set_category(self, category):
        self.category = category
        return self

    def __str__(self):
        st = '<Expression>'
        for ss, vv in [
            ['category', self.category],
            ['coe', self.coe],
            ['recorders', self.recorders],
            ['param_error', self.param_error],
            ['length', self.length],
            ['sum_param_error', self.sum_param_error],
            ['efficiency', self.efficiency],
        ]:
            st += f'\n\t.{ss}: {vv}'
        st += '\n'
        return st

    """ support <sort> <min> <max> """

    # == equal to
    def __eq__(self, other):
        if isinstance(other, Expression):
            return self.efficiency == other.efficiency
        return self.efficiency == other

    # != not equal to
    def __ne__(self, other):
        if isinstance(other, Expression):
            return self.efficiency != other.efficiency
        return self.efficiency != other.efficiency

    # < less than
    def __lt__(self, other):
        if isinstance(other, Expression):
            return self.efficiency < other.efficiency
        return self.efficiency < other

    # > greater than
    def __gt__(self, other):
        if isinstance(other, Expression):
            return self.efficiency > other.efficiency
        return self.efficiency > other

    # <= less than or equal to
    def __le__(self, other):
        if isinstance(other, Expression):
            return self.efficiency <= other.efficiency
        return self.efficiency <= other

    # >= greater than or equal to
    def __ge__(self, other):
        if isinstance(other, Expression):
            return self.efficiency >= other.efficiency
        return self.efficiency >= other

    def inspect(self, li):
        return self.hook(*li)

    # param sequence of regression hook must correspond to pass in sequence coe
    @property
    def formula(self):
        return self.hook(*list(self.coe.values()), *self.variables)

    def __setitem__(self, key, value):
        if key == 'write':
            self.wrote = value

    def __getitem__(self, item):
        if item == 'write':
            return self.wrote

    @property
    def write(self):
        return self.wrote

    def set_write(self, callback):
        self.__setitem__('write', callback(list(self.coe.values())))

    def set_write_variable(self, callback):
        self.__setitem__('write', callback(list(self.coe.values()) + self.variables))


# decorator before each regression
def ready(regress_func):
    def wrapper(*args, **kwargs):
        Comparison.EXPRESSIONS = []
        Expression.DATA = None
        Expression.SIZE = 20
        Expression.INITIAL = None
        return regress_func(*args, **kwargs)
    return wrapper


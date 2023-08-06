import string

from speedo.algorithms.regression.modules import *
from speedo.algorithms.regression.constants import Plane


NAMESPACE = 'regress_func'
UNIQUE_ID = -1


def get_unique():
    global UNIQUE_ID
    UNIQUE_ID += 1
    return UNIQUE_ID


def get_title():
    return NAMESPACE + str(get_unique())


class Linear(Regression):
    """
        How does linear regression differ from others
            1/ simplest y=kx+b
            2/ both x and y are ensured to be in mono trend, others only enforce x monotonicity
            3/ due to pascal triangle row evaluation, many is limited to be under 15,
                any larger cause machine to overstress
    """

    def __init__(self, many=15, x_val=None, y_val=None, dots=None, rev=False):
        # 2 minimum dots to find y = kx + b
        if many > 15:
            print(f'Warning: <Linear>: many {many} larger than 15 is gonna slow down the process\nsuggested value 10')
        Regression.__init__(
            self,
            many=many,
            required=2,
            centered=True,
            x_mono=True,
            y_mono=True,
            x_val=x_val,
            y_val=y_val,
            dots=dots,
            rev=rev,
            avg=True,
        )
        # recorder
        self.k = []
        self.b = []

    # regress takes an vector of length 2 and returns void
    # continue by Regression.eject, append one to each recorder
    def regress(self, vector):
        try:
            k = (vector.dt[1][1] - vector.dt[0][1]) / float(vector.dt[1][0] - vector.dt[0][0])
            self.k.append(k)
            self.b.append(vector.dt[0][1] - k * vector.dt[0][0])
        except ZeroDivisionError:
            pass

    # archive eject to regress
    def induce(self):
        for vector in self.eject():
            self.regress(vector)

    # return calculations, as callback that will be passed into calculations
    @staticmethod
    def hook(k, b):
        # pass in x return y
        title = get_title()
        exec(f'def {title}(x):    return {k} * x + {b}')
        return locals()[title]

    # finalize linear regress, establish result as calculations object
    def deduce(self):
        Comparison(Expression(
            hook=self.hook,
            k=self.k,
            b=self.b,
        ).set_category(Linear))
        return Comparison.compare()


class Parabola(Regression):
    """
    Although Parabola is duplicated to <Exponential> when exp=2, it's not deleted
    because
        1/ it's practical for those who's not interested to learn the algorithm works
        2/ provides an easy pathway for interested people to better understand the code
    """
    def __init__(self, many=15, x_val=None, y_val=None, dots=None, rev=False):
        # 3 minimum dots to find y = ax^2 + bx + c
        Regression.__init__(
            self,
            many=many,
            required=3,
            centered=False,
            x_mono=True,
            y_mono=False,
            x_val=x_val,
            y_val=y_val,
            dots=dots,
            rev=rev,
            avg=False
        )
        # recorder
        self.a = []
        self.b = []
        self.c = []

    # regress takes an vector of length 3 and returns void
    # continue by Regression.eject, append one to each recorder
    def regress(self, vector):
        try:
            plane = Plane(vector)
            coe = plane.formulate()
            self.a.append(coe[0])
            self.b.append(coe[1])
            self.c.append(coe[2])
        except ZeroDivisionError:
            pass

    # archive eject to regress
    def induce(self):
        for vector in self.eject():
            self.regress(vector)

    # return calculations, as callback that will be passed into calculations
    @staticmethod
    def hook(a, b, c):
        # pass in x return y
        exec(f'def parabola_regression(x):    return {a} * x ** 2 + {b} * x + {c}')
        return locals()['parabola_regression']

    # finalize linear regress, establish result as calculations object
    def deduce(self):
        Comparison(Expression(
            hook=self.hook,
            a=self.a,
            b=self.b,
            c=self.c,
        ).set_category(Parabola))
        return Comparison.compare()


class ExponentialParabola(Regression):
    """
        regress exponential function
        for example, when init with 2, it solves function such that:
        2 * x ** 2 + 3 * x + 1
        the exponential can be infinitely large, even
        2 * x^100 ...
        however, for a power of n, requires n + 1 vectors to resolve the function
    """

    ALPHABET = string.printable[10:36]

    @staticmethod
    # 4 ->  + a * x ** 4 + b * x ** 3 + c * x ** 2 + d * x ** 1
    def write(eps):
        ss = ''
        for ii, dd in enumerate(eps):
            ss += ' + ' + str(dd) + ' * x ** ' + str(len(eps) - 1 - ii)
        return ss

    def __init__(self, exp, many=15, x_val=None, y_val=None, dots=None, rev=False):
        # if exp == 1:
        #     raise ValueError('<Exponential> init, if exponent is 1, please use <Linear> instead')
        if exp + 1 > len(x_val):
            raise ValueError('\n'.join([
                '<Exponential> init, not enough vectors for regressing',
                f'to perform x^{exp} regression, need at least {exp - 1} vectors,',
                f'only {len(x_val)} detected, need {exp + 1 - len(x_val)} more',
            ]))
        self.length = exp + 2

        Regression.__init__(
            self,
            many=many,
            required=exp + 1,
            centered=False,
            x_mono=True,
            y_mono=False,
            x_val=x_val,
            y_val=y_val,
            dots=dots,
            rev=rev,
            avg=False
        )

        # {a:1, b:2 ..}
        self.rk = ExponentialParabola.ALPHABET[:self.length-1]
        self.eps = []
        self.recorders = {}
        for rk in self.rk:
            self.recorders[rk] = []

    def regress(self, vector):
        try:
            plane = Plane(vector)
            coe = plane.formulate()
            for ii, dd in enumerate(coe):
                self.recorders[self.rk[ii]].append(dd)
        except ZeroDivisionError:
            pass

    def induce(self):
        for vector in self.eject():
            self.regress(vector)

    @staticmethod
    def hook(*args):
        # use id to append function at local scope, which can be renamed
        title = get_title()
        written = 'def ' + title + '(x):\treturn ' + ExponentialParabola.write(args)
        exec(written)
        return locals()[title]

    # finalize linear regress, establish result as calculations object
    def deduce(self):
        Comparison(Expression(
            hook=self.hook,
            **self.recorders,
        ).set_category(ExponentialParabola))
        return Comparison.compare()


class InverseExponentialParabola(ExponentialParabola):
    """
        y^power = k / x power calculations, power and k can varies
        for example, when
            y_power = 2,
            x power calculations = 4x^2 - 4x + 1
            k = 2,
        y^2 = 2 / (4x^2 - 4x + 1)

        supported by exponential matrix transformation algorithm
        y transformation such as power of 2 and coe of 2 is accomplished by data and result pre-processing
    """

    def __init__(self, pro, y_exp, x_exp, many=15, x_val=None, y_val=None, dots=None, rev=False):
        xs = []
        ys = []
        for ii, dd in enumerate(y_val):
            if dd != 0:
                xs.append(x_val[ii])
                ys.append(pro / dd ** y_exp)
        self.pro = pro
        self.y_exp = y_exp
        Regression.initial(Vector(x_val, y_val))
        super(InverseExponentialParabola, self).__init__(
            exp=x_exp,
            many=many,
            x_val=xs,
            y_val=ys,
            dots=dots,
            rev=rev,
        )

    @staticmethod
    def hook(*args):
        # use id to append function at local scope, which can be renamed
        title = get_title()
        # [a, b, c ... pro, y_exp]
        pro = args[-2]
        y_exp = args[-1]
        written = 'def ' + title + '(x):\treturn ' + str(pro) + ' / (' + ExponentialParabola.write(args[:-2]) + ')'
        exec(written)
        return locals()[title]

    # finalize linear regress, establish result as calculations object
    def deduce(self):
        Comparison(Expression(
            hook=self.hook,
            **self.recorders,
            pro=self.pro,
            y_exp=self.y_exp,
        ).set_category(InverseExponentialParabola))
        return Comparison.compare()


if __name__ == '__main__':
    pass
    """
        testing instruction
            each block referred by line indentation, must be tested individually
            since modules.Comparison only evaluate from the same data
            if you un-hash all code and run at once, error will definitely occur
            because they are based on different data sample, Comparison always
            returns the one with least efficiency which is the most matching
    """

    # # x = 2y + 20
    # xs = [x for x in range(10)]
    # ys = [2 * y + 20 for y in range(10)]
    # reg = Linear(
    #     x_val=xs,
    #     y_val=ys,
    #     many=10
    # )
    # reg.induce()
    # calculations = reg.deduce()
    # func = calculations.formula
    # # print(func(2))

    # # y = 2x^3 + x^2 + 4x + 8
    # lo = ExponentialParabola(
    #     exp=3,
    #     x_val=[x for x in range(20)],
    #     y_val=[2 * x ** 3 + x ** 2 + 4 * x + 8 for x in range(20)],
    # )
    #
    # lo.induce()
    # express = lo.deduce()
    # fun = express.formula
    # print(fun(-1))

    # # y^2 = 2 / (4x^2 - 4x + 1)
    # lo = InverseExponentialParabola(
    #     pro=2,
    #     y_exp=1,
    #     x_exp=2,
    #     x_val=[x for x in range(20)],
    #     y_val=[2 / (4 * x ** 2 - 4 * x + 1) for x in range(20)],
    # )
    # lo.induce()
    # express = lo.deduce()
    # # print(express)
    # fun = express.formula
    # # print(2 / fun(-2))
    # print(fun(-2))

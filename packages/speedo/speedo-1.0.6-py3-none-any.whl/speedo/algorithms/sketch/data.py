import numpy as np
from sympy import *
from sympy import core
from matplotlib import pyplot as plt
import matplotlib
from math import *
matplotlib.use('TkAgg')

# data.py
from mpl_toolkits.axisartist import SubplotZero
from speedo.algorithms.sketch.outliers import graph as outlier_graph
from speedo.algorithms.calculations.common import linespace, string_list, merge, roll, one_d

# expression.py
from speedo.algorithms.calculations.common import pascal, round_dict
from speedo.algorithms.calculations.discrete import Boundary, domain_initializer

# funcs.py
from speedo.algorithms.regression.regress import *

from speedo.algorithms.calculations.common import commute, either, coe_decode, exponents
from speedo.algorithms.sketch.theme import Theme

from speedo.algorithms.regression.bezier import sketch as bezier_sketch, illustrate as bezier_illustrate, draw as bezier_draw


class List(list):
    def __init__(self, iterable):
        super(List, self).__init__(iterable)
        self.kwargs = Param(['label_shift_xy', 'xy_up', 'xy_down'], label_shift_xy=(0, 0), xy_up=(0, 0), xy_down=(0, 0))  # passed into plt.graph, set by set

    # set kwargs to pass into plotting graph
    def set(self, **kwargs):
        self.kwargs.set(**kwargs)
        return self

    def get(self, key):
        return self.kwargs.get(key)


class Data:
    def inspect(self, ys):
        if self.x is None:
            return
        if len(self.x) != len(ys):
            raise TypeError(f'y must be the same size as x, unmatched <x: {self.x}> <y: {ys}>')

    def append(self, ys):
        self.inspect(ys)
        self.ys.append(ys)

    def __init__(self, x, y_or_ys):
        self.x = x
        self.ys = []
        if isinstance(y_or_ys[0], list) or isinstance(y_or_ys[0], tuple):
            for ys in y_or_ys:
                if isinstance(ys, List):
                    self.append(ys)
                else:
                    self.append(List(ys))
        else:
            if isinstance(y_or_ys, List):
                self.append(y_or_ys)
            else:
                self.append(List(y_or_ys))
        if x is None:
            self.x = [ii for ii in range(len(self.ys))]
        self.formulas = []

    def concat(self):
        return Data([xx for xx in self.x], [[yy for yy in ys] for ys in self.ys])

    def __str__(self):
        ss = f'<Data\n\tx: {self.x}\n\ty: [\n'
        for ys in self.ys:
            ss += f'\t\t{ys}\n'
        ss += f'\t]\n>'
        return ss

    def regress(self, auto_domain=True, padding=0):
        return RegressData(self.x, self.ys, auto_domain=auto_domain, padding=padding)

    # return ys
    def average(self):
        ys = []
        for ii in range(len(self.ys[0])):
            col = []
            for yy in self.ys:
                col.append(yy[ii])
            ys.append(sum(col) / len(col))
        return Data(self.x, ys)

    def graph(self, fig=None, ax=None, cartesian=False):
        return GraphData(self, fig, ax, cartesian)

    def outliers(
        self,
        title=None,
        xlabel=None,
        ylabel=None,
        legends=None,
        left_shift=0,
        upper_shift=0,
        shift_rate=0,
        average_color='blue',
        average_fill='cyan',
    ):
        outlier_graph(self.x, self.ys, title, xlabel, ylabel, legends, left_shift, upper_shift, shift_rate, average_color, average_fill)

    # support std in regress
    def variance(self, error):
        ndt1 = self.concat()
        ndt2 = self.concat()
        length = len(self.ys[0])
        for jj in range(len(ndt1.ys)):
            for ii, err in enumerate(linespace([-error, error], length)):
                ndt1.ys[jj][ii] += err
                ndt2.ys[jj][ii] -= err
        return [ndt1, ndt2]

    # return dict with labels as keys nad ys as values
    def labels(self, labels):
        if len(labels) != len(self.ys):
            raise ValueError('<Data> tag require a list of length ' + str(len(self.ys)))
        di = {}
        for ii, label in enumerate(labels):
            di[label] = self.ys[ii]
        return di

    # return Data object with each ys in percentage
    def percent(self):
        return Data(
            [xe / sum(self.x) * 100 for xe in self.x],
            [[ye / sum(yy) * 100 for ye in yy] for yy in self.ys]
        )

    def domain(self):
        return Boundary([min(self.x), max(self.x)])

    def mono(self, operate='<', x=True, y=True):
        if x:
            m1 = Mono(array=self.x, operate=operate, along=self.ys).mono
            self.x = m1['array']
            self.ys = m1['along']
        if y:
            ll = len(self.ys)
            for ii in range(ll):
                m1 = Mono(array=self.ys.pop(0), operate=operate, along=[self.x] + self.ys).mono
                for jj, aa in enumerate(m1['along']):
                    if jj == 0:
                        self.x = aa
                    else:
                        self.ys[0] = aa
                self.ys.append(m1['array'])
        return self


class RegressData(Data):
    def __init__(self, x, y_or_ys, auto_domain=True, padding=0):
        self.auto_domain = auto_domain
        self.padding = padding
        self.caches = []
        super(RegressData, self).__init__(x=x, y_or_ys=y_or_ys)

    # do not call it outside of class, it is used to record procedure for std variance
    def add_cache(self, val):
        self.caches.append(val)

    def clean_cache(self):
        self.caches = []

    def simulate(self, other):
        for di in self.caches:
            kk = list(di.keys())[0]
            vv = list(di.values())[0]
            kk(other, *vv['args'], **vv['kwargs'])
        return self

    def record(foo):
        def wrapper(self, *args, **kwargs):
            self.add_cache({foo: {'args': args, 'kwargs': kwargs}})
            return foo(self, *args, **kwargs)
        wrapper._origin = foo
        return wrapper

    def add_formula(self, func):
        if self.auto_domain:
            func.set_domain([min(self.x) - self.padding, max(self.x) + self.padding])
        self.formulas.append(func)

    @record
    def linear(self, least_square=True):
        #  y = ax + b
        self.formulas = []
        if least_square:
            for yy in self.ys:
                self.add_formula(least_square_alg(Vector(x_val=self.x, y_val=yy)))
        else:
            for yy in self.ys:
                coe = linear_regression(
                    x=self.x,
                    y=yy,
                ).coe
                self.add_formula(Func({1: coe['k'], 0: coe['b']}))
        return self

    @record
    def parabola(self, depth=8):
        # y = ax^2 + bx + c
        for ys in self.ys:
            coe = parabola_regression(x=self.x, y=ys, depth=depth).coe
            self.add_formula(Func({2: coe['a'], 1: coe['b'], 0: coe['c']}))
        return self

    @record
    def cubic(self, depth=8):
        # y = ax^3 + bx^2 + cx + d
        for ys in self.ys:
            coe = cubic_regression(x=self.x, y=ys, depth=depth).coe
            self.add_formula(Func({3: coe['a'], 2: coe['b'], 1: coe['c'], 0: coe['d']}))
        return self

    @record
    def quadratic(self, depth=8):
        # y = ax^4 + bx^3 + cx^2 + dx + e
        for ys in self.ys:
            coe = quadratic_regression(x=self.x, y=ys, depth=depth).coe
            self.add_formula(Func({4: coe['a'], 3: coe['b'], 2: coe['c'], 1: coe['d'], 0: coe['e']}))
        return self

    @record
    def exponential(self, x_exp, depth=8):
        # y = ax^n + bx^(n-1) + cx^(n-2) ...
        for ys in self.ys:
            coe = exponential_parabola_regression(x_exp=x_exp, x=self.x, y=ys, depth=depth).coe
            self.add_formula(Func(coe_decode(coe)))
        return self

    # y^k = product / (ax^n + bx^(n-1) + cx^(n-2) + ...)
    @record
    def inverse_exponential(self, product, y_exp, x_exp, depth=8):
        for ys in self.ys:
            expr = inverse_exponential_regression(product=product, y_exp=y_exp, x_exp=x_exp, x=self.x, y=ys, depth=depth)
            self.add_formula(Func(expr.write))
        return self

    # x = None,
    # y = None,
    # dots = None,
    # x_power_range = (1, 2, 3, 4),
    # y_power_range = (1, 2, 3, 4),
    # product_range = (1, 2, 3, 4),
    @record
    def regression(
            self,
            x_power_range=(1, 2, 3, 4),
            y_power_range=(1, 2, 3, 4),
            product_range=(1, 2, 3, 4),
    ):
        for ys in self.ys:
            expr = regression(x=self.x, y=ys, x_power_range=x_power_range, y_power_range=y_power_range, product_range=product_range)
            if expr.category == InverseExponentialParabola:
                self.add_formula(Func(expr.write))
            else:
                self.add_formula(Func(coe_decode(expr.coe)))
        return self


def new_graph(fig=None, ax=None, cartesian=False, square=False):
    if fig and ax:
        fig_ = fig
        ax_ = ax
    elif cartesian:
        fig_ = plt.figure()
        ax_ = SubplotZero(fig_, 111)
        fig_.add_subplot(ax_)

        for direction in ["xzero", "yzero"]:
            ax_.axis[direction].set_axisline_style("-|>")
            ax_.axis[direction].set_visible(True)

        for direction in ["top", "bottom", "left", "right"]:
            ax_.axis[direction].set_visible(False)
    else:
        fig_, ax_ = plt.subplots()
    if square:
        fig_.gca().set_aspect('equal', adjustable='box')
    return fig_, ax_


# static graph property mix-in
class GraphStatic:
    def __init__(self, fig=None, ax=None, cartesian=False, square=False):
        self.fig, self.ax = new_graph(fig=fig, ax=ax, cartesian=cartesian, square=square)
        self.themes = []
        self.cartesian = cartesian
        self.cache = []

    def add_cache(self, cache):
        self.cache.append(cache)

    def clean_cache(self):
        self.cache = []

    def add_theme(self, *theme):
        for tm in theme:
            self.themes.append(tm)
        return self

    def title(self, title, **kwargs):
        self.ax.set_title(title, **kwargs)
        return self

    def xlabel(self, xlabel, xy=None, **kwargs):
        if xy:
            self.ax.text(s=xlabel, x=xy[0], y=xy[1], **kwargs)
        else:
            self.ax.set_xlabel(xlabel)
        return self

    def ylabel(self, ylabel, xy=None, **kwargs):
        if xy:
            self.ax.text(s=ylabel, x=xy[0], y=xy[1], **kwargs)
        else:
            self.ax.set_ylabel(ylabel, **kwargs)
        return self

    def xticks(self, xs, ticks, **kwargs):
        self.ax.set_xticks(xs)
        self.ax.set_xticklabels(ticks, **kwargs)
        return self

    def yticks(self, ys, ticks, **kwargs):
        self.ax.set_yticks(ys)
        self.ax.set_yticklabels(ticks, **kwargs)
        return self

    # return the ii th theme populated to length of n
    def get_color(self, ii, n):
        try:
            self.themes[ii]
        except IndexError:
            try:
                return self.themes[0].active(n)
            except IndexError:
                return Theme().default().active(n)
        if self.themes[ii].is_empty():
            self.themes[ii].default()
        return self.themes[ii].active(n)

    def xlim(self, xs):
        plt.xlim(xs)
        return self

    def ylim(self, ys):
        plt.ylim(ys)
        return self

    def lim(self, arr):
        return self.xlim(arr).ylim(arr)

    def fill_between(self, xs, ys1, ys2, **kwargs):
        self.ax.fill_between(xs, ys1, ys2, **kwargs)
        return self

    def grid(self, **kwargs):
        self.ax.grid(**kwargs)
        return self

    def xkcd(self, **kwargs):
        plt.xkcd(**kwargs)
        return self

    def legend(self, *args, **kwargs):
        self.ax.legend(*args, **kwargs)
        return self

    def show(self, *args, **kwargs):
        plt.show(*args, **kwargs)
        return self


class GraphData(GraphStatic):
    ROUND = 2

    def __init__(self, data, fig=None, ax=None, cartesian=False, square=False):
        super(GraphData, self).__init__(fig=fig, ax=ax, cartesian=cartesian, square=square)
        self.data = data

    def __get_xlim(self):
        return [min(self.data.x), max(self.data.x)]

    def xlim(self, xs=None, padding=0):
        if xs is None:
            xs = self.__get_xlim()
            xs[0] -= padding
            xs[1] += padding
        plt.xlim(xs)
        return self

    def __get_ylim(self):
        yys = []
        for yy in self.data.ys:
            yys.append(min(yy))
            yys.append(max(yy))
        return [min(yys), max(yys)]

    def ylim(self, ys=None, padding=0):
        if ys is None:
            ys = self.__get_ylim()
            ys[0] -= padding
            ys[1] += padding
        plt.ylim(ys)
        return self

    def lim(self, arr=None, padding=0):
        return self.xlim(xs=arr, padding=padding).ylim(ys=arr, padding=padding)

    def label(self, xy=(0, 0)):
        for yy in self.data.ys:
            for ii in range(len(self.data.x)):
                x_ = self.data.x[ii]
                y_ = yy[ii]
                self.ax.text(s=f"({round(x_, GraphData.ROUND)}, {round(y_, GraphData.ROUND)})", x=x_+xy[0], y=y_+xy[1])
        return self

    def fill_between(self, ind1, ind2, **kwargs):
        return super(GraphData, self).fill_between(self.data.x, self.data.ys[ind1], self.data.ys[ind2], **kwargs)

    def bar(self, width, label=False, xy_up=(0, 0), xy_down=(0, 0), **kwargs):
        n = len(self.data.ys)
        for ii, shift in enumerate(commute(width, n)):
            yy = self.data.ys[ii]
            di = {'color': self.get_color(ii, len(yy))}
            di.update(yy.kwargs.param())
            di.update(kwargs)
            vertical = self.ax.bar([xx + shift for xx in self.data.x], yy, width=width, **di)
            if label:
                GraphData.auto_label_bar(vertical_=vertical, colors=di['color'], xy_up=xy_up, xy_down=xy_down)
        return self

    def errorbar(self, error, label=True, label_shift_xy=(0, 0), **kwargs):
        for ii, yy in enumerate(self.data.ys):
            di = {'color': self.get_color(ii, 1)[0]}
            di.update(yy.kwargs.param())
            di.update(kwargs)
            self.ax.errorbar(self.data.x, yy, yerr=error, **kwargs)
            if label:
                for jj, x_ in enumerate(self.data.x):
                    y_ = yy[jj]
                    self.ax.text(s=f"({round(x_, GraphData.ROUND)}, {round(y_, GraphData.ROUND)})", x=x_ + label_shift_xy[0], y=y_+ label_shift_xy[1], color=di['color'])
        return self

    def plot(self, labels=None, color=None, **kwargs):
        if labels is None:
            labels = [None for ii in range(len(self.data.ys))]
        for ii, yy in enumerate(self.data.ys):
            try:
                label = labels[ii]
            except KeyError:
                label = None
            di = {}
            if color is None:
                di['color'] = self.get_color(ii, 1)[0]
            di.update(yy.kwargs.param())
            di.update(kwargs)
            if color is None:
                self.ax.plot(self.data.x, yy, label=label, **di)
            else:
                self.ax.plot(self.data.x, yy, label=labels[ii], **di)
        return self

    def average_line(self, color=None, label='avg', linestyle='-.', **kwargs):
        if color is None:
            color = Theme().random_medium().active(1)[0]
        data_avg = self.data.average()
        ym = sum(data_avg.ys[0]) / len(data_avg.ys[0])
        if label:
            self.axhline(ym, color=color, linestyle=linestyle, label=label + str(round(ym, GraphData.ROUND)), **kwargs)
        else:
            self.axhline(ym, color=color, linestyle=linestyle, **kwargs)
        return self

    def average_plot(self, color=None, label=None, linestyle='-.', **kwargs):
        if color is None:
            color = Theme().random_medium().active(1)[0]
        if label is None:
            label = 'average'
        self.data.average().graph(fig=self.fig, ax=self.ax, cartesian=self.cartesian).plot(labels=[label], linestyle=linestyle, color=color, **kwargs)
        return self

    def scatter(self, color=None, labels=None, **kwargs):
        if labels is None:
            labels = [None for ii in range(len(self.data.ys))]
        for ii, yy in enumerate(self.data.ys):
            di = {}
            if color is None:
                di['color'] = self.get_color(ii, len(yy))
            di.update(yy.kwargs.param())
            di.update(kwargs)
            if color is None:
                self.ax.scatter(self.data.x, yy, label=labels[ii], **di)
            else:
                self.ax.scatter(self.data.x, yy, label=labels[ii], **di)
        return self

    def axhline(self, y, color, linestyle, label=None, **kwargs):
        self.ax.axhline(y=y, color=color, linestyle=linestyle, label=label, **kwargs)
        return self

    def axvline(self, x, color, linestyle, label=None, **kwargs):
        self.ax.axvline(x=x, color=color, linestyle=linestyle, label=label, **kwargs)
        return self

    @staticmethod
    def auto_label_bar(vertical_, colors, xy_up=(0, 0), xy_down=(0, 0)):
        if isinstance(colors, str) or (isinstance(colors, tuple) and len(colors) == 3):
            colors = [colors for ii in range(len(vertical_))]
        for index, rectangle in enumerate(vertical_):
            height = rectangle.get_height()
            x_value = rectangle.get_x()
            width = rectangle.get_width()
            if height < 0:
                height = height - width * 2
                plt.text(x_value + width / 2. + xy_down[0], height + xy_down[1], str(round(height, GraphData.ROUND)), color=colors[index], ha="center", va="bottom")
            else:
                plt.text(x_value + width / 2. + xy_up[0], height + xy_up[1], str(round(height, GraphData.ROUND)), color=colors[index], ha="center", va="bottom")

    def suit_bezier(self):
        return SuitDataBezier(self.data, self.fig, self.ax)

    def suit_linear(self):
        return SuitDataLinear(self.data, self.fig, self.ax)

    def suit_regress(self):
        return SuitDataRegress(self.data, self.fig, self.ax)


class SuitDataBezier(GraphData):
    def static(self, color=None, n=100):
        if color is None:
            color = Theme().random_negative().active(1)[0]
        for yy in self.data.ys:
            bezier_draw(self.fig, self.ax, points=Vector(x_val=self.data.x, y_val=yy).dots, n=n, color=color)
        return self

    def animate(self, color=None, n=100):
        if color is None:
            color = Theme().random_negative().active(1)[0]
        for yy in self.data.ys:
            self.add_cache(bezier_sketch(fig=self.fig, points=Vector(x_val=self.data.x, y_val=yy).dots, n=n, color=color))
        return self

    def animate_partial(self, depth, n=100, interval=50):
        for yy in self.data.ys:
            vt = Vector(x_val=self.data.x, y_val=yy)
            self.add_cache(bezier_illustrate(fig=self.fig, points=vt.dots, interval=interval, n=n, depth=depth))
        return self

    def animate_full(self, n=100, interval=50):
        for yy in self.data.ys:
            vt = Vector(x_val=self.data.x, y_val=yy)
            self.add_cache(bezier_illustrate(fig=self.fig, points=vt.dots, interval=interval, n=n, depth=len(vt)))
        return self


class SuitDataLinear(GraphData):
    def linear(self, error, label=True, label_shift_xy=(0, 0)):
        self.themes = []
        self.grid()
        for ii, func in enumerate(self.data.regress().linear().formulas):
            yy = self.data.ys[ii]
            xs = [self.data.x[0], self.data.x[-1]]
            Data(xs, [func.formula(xx) for xx in xs]).graph(self.fig, self.ax).add_theme(Theme().gradient_negative(0)).plot(labels=[func.abbr(2)])
            self.add_theme(Theme().gradient_negative(30)).errorbar(error=error, label=label, label_shift_xy=label_shift_xy)
            # up to down
            oblique1 = oblique([self.data.x[0], yy[0] + error], [self.data.x[-1], yy[-1] - error])
            # down to up
            oblique2 = oblique([self.data.x[0], yy[0] - error], [self.data.x[-1], yy[-1] + error])
            Data([self.data.x[0], self.data.x[-1]], [yy[0] + error, yy[-1] - error]).graph(self.fig, self.ax).add_theme(Theme().gradient_positive(0)).plot(labels=[oblique1.abbr(2)], linestyle='-.')
            Data([self.data.x[0], self.data.x[-1]], [yy[0] - error, yy[-1] + error]).graph(self.fig, self.ax).add_theme(Theme().gradient_positive(0)).plot(labels=[oblique2.abbr(2)], linestyle='-.')
        return self

    def bar(self, width, label=False, xy_up=(0, 0), xy_down=(0, 0), **kwargs):
        self.themes = []
        themes = either(Theme().gradient_positive(-10), Theme().gradient_negative(10), n=len(self.data.ys))
        for theme in themes:
            self.add_theme(theme)
        super(SuitDataLinear, self).bar(width=width, label=label, xy_up=xy_up, xy_down=xy_down, **kwargs)
        return self

    def barh(self, tags, labels):
        if isinstance(labels, str):
            labels = string_list(labels, len(self.data.ys))
        if len(labels) != len(self.data.ys):
            raise ValueError('barh labels must have a length of ' + str(len(self.data.ys[0])))
        if isinstance(tags, str):
            tags = string_list(tags, len(self.data.ys[0]))
        data_tag = self.data.labels(labels)
        array = np.array(list(data_tag.values()))
        data_cum = array.cumsum(axis=1)
        theme = Theme().complementary()
        category_colors = theme.active(array.shape[1])

        # fig, ax = plt.subplots(figsize=(9.2, 5))
        self.fig.set_figwidth(9.2)
        self.fig.set_figheight(5)
        self.ax.invert_yaxis()
        self.ax.xaxis.set_visible(False)
        self.ax.set_xlim(0, np.sum(array, axis=1).max())

        for i, (colname, color) in enumerate(zip(tags, category_colors)):
            widths = array[:, i]
            starts = data_cum[:, i] - widths
            rects = self.ax.barh(labels, widths, left=starts, height=0.5,
                            label=colname, color=color)
            if len(color) == 3:
                r, g, b = color
            else:
                r, g, b, a = color
            text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
            self.ax.bar_label(rects, label_type='center', color=text_color)
        self.ax.legend(ncol=len(labels), bbox_to_anchor=(0, 1),
                  loc='lower left', fontsize='small')

        return self

    def scatter(self, labels=None, label_hline='avg', label_avg_plot=None):
        self.themes = []
        if labels is None:
            labels = [None for ii in range(len(self.data.ys))]
        self.add_theme(*either(Theme().gradient_positive(-10), Theme().gradient_negative(10), n=len(self.data.ys)))
        super(SuitDataLinear, self).scatter(labels=labels).average_line(label=label_hline).average_plot(label=label_avg_plot)
        data_avg = self.data.average()
        fill_color = Theme().random_positive().active(1)
        self.ax.fill_between(self.data.x, sum(data_avg.ys[0]) / len(data_avg.ys[0]), data_avg.ys[0], color=fill_color, alpha=0.3)
        return self


class SuitRegress:
    def linear(self, error=0, n=100, x_start=None, x_end=None, label=True, label_shift_xy=(0, 0), rit=2):
        self.themes = []
        self.add_theme(*[Theme().gradient_negative(75) for ii in range(len(self.data.formulas))])
        dt_var1, dt_var2 = self.data.variance(error=error)
        dt_reg1, dt_reg2 = dt_var1.regress(), dt_var2.regress()
        self.data.simulate(dt_reg1)
        self.data.simulate(dt_reg2)
        for ii, [func, func1, func2] in enumerate(zip(self.data.formulas, dt_reg1.formulas, dt_reg2.formulas)):
            colors = self.get_color(ii, 3)
            self.errorbar(error=error, label=label, label_shift_xy=label_shift_xy)
            func.sample(n=n, x_start=x_start, x_end=x_end).graph(fig=self.fig, ax=self.ax).plot(color=colors[1], labels=func.expression(rit))
            func1.sample(n=n, x_start=x_start, x_end=x_end).graph(fig=self.fig, ax=self.ax).plot(color=colors[2], labels=func1.expression(rit), linestyle='-.')
            func2.sample(n=n, x_start=x_start, x_end=x_end).graph(fig=self.fig, ax=self.ax).plot(color=colors[2], labels=func2.expression(rit), linestyle='-.')
        return self

    def bar(self, width, n=100, x_start=None, x_end=None, label=False, xy_up=(0, 0), xy_down=(0, 0), rit=2):
        self.themes = []
        self.add_theme(*either(Theme().gradient_positive(-10), Theme().gradient_negative(10), n=len(self.data.ys)))
        for ii, func in enumerate(self.data.formulas):
            func.sample(n=n, x_start=x_start, x_end=x_end).graph(fig=self.fig, ax=self.ax).plot(color=self.get_color(ii, 0)[0], labels=[func.expression(rit)])
        type(self).__bases__[-1].bar(self, width, label=label, xy_up=xy_up, xy_down=xy_down)
        return self

    def scatter(self, n=100, x_start=None, x_end=None, labels=None, label_hline='avg', label_avg_plot=None, rit=2):
        self.themes = self.suit_linear().scatter(labels=labels, label_hline=label_hline, label_avg_plot=label_avg_plot).themes
        for ii, func in enumerate(self.data.formulas):
            func.sample(n=n, x_start=x_start, x_end=x_end).graph(fig=self.fig, ax=self.ax).plot(color=self.get_color(ii, 0)[0], labels=[func.expression(rit)])
        return self


class SuitDataRegress(SuitRegress, GraphData):
    pass


# funcs.py
class Vectors:
    def __init__(self, *args):
        self.vectors = []
        for arg in args:
            if (not isinstance(arg, Vector)) and (not isinstance(arg, Vectors)):
                raise TypeError('<Vectors> inits with Vector(s) objects')
            self.append(arg)
        self.cache = []
        self.themes = []
        self.formulas = []

    def round(self, rit):
        for vt in self.vectors:
            vt.round(rit)
        return self

    def concat(self):
        return Vectors(*[vector.concat() for vector in self.vectors])

    def __str__(self):
        ss = '<Vectors\n'
        for ii, vt in enumerate(self.vectors):
            ss += '\t' + str(ii + 1) + '. ' + str(vt) + '\n'
        return ss.rstrip() + '\n>'

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.vectors[item]

    def __setitem__(self, key, value):
        if isinstance(key, int) and isinstance(value, Vector):
            self.vectors[key] = value

    def __iter__(self):
        for vt in self.vectors:
            yield vt

    def append(self, vector):
        if isinstance(vector, Vector):
            self.vectors.append(vector)
        elif isinstance(vector, Vectors):
            for vt in vector:
                self.vectors.append(vt)
        else:
            raise TypeError('<Vectors> inits with Vector objects')

    @property
    def xs(self):
        return [vt.x for vt in self.vectors]

    @property
    def ys(self):
        return [vt.y for vt in self.vectors]

    def regress(self):
        return RegressFunc(*self.vectors)

    def graph(self, fig=None, ax=None, cartesian=False):
        return GraphVectors(self, fig, ax, cartesian)

    def average(self):
        xs = []
        ys = []
        for ii in range(len(self.xs[0])):
            row = []
            col = []
            for jj in range(len(self.xs)):
                row.append(self.xs[jj][ii])
                col.append(self.ys[jj][ii])
            xs.append(sum(row) / len(row))
            ys.append(sum(col) / len(col))
        return Vectors(Vector(x_val=xs, y_val=ys))

    def variance(self, error):
        ndt1 = self.concat()
        ndt2 = self.concat()
        length = len(self.ys[0])
        for jj in range(len(ndt1.ys)):
            for ii, err in enumerate(linespace([-error, error], length)):
                ndt1.vectors[jj].y_val[ii] += err
                ndt2.vectors[jj].y_val[ii] -= err
        # update y_val does not refresh dots, but concat
        return [ndt1.concat(), ndt2.concat()]

    # return vectors that each x or y array sum to 100
    def percent(self):
        return Vectors(
            *[vector.concat().percent() for vector in self.vectors]
        )

    def domain(self):
        xs = []
        for xx in self.xs:
            xs += xx
        return Boundary([min(xs), max(xs)])

    def mono(self, operate='<', x=True, y=True):
        for vector in self.vectors:
            vector.mono(operate=operate, x=x, y=y)
        return self


# support negative
class Func:
    NAMESPACE = 'irregular_func'
    UNIQUE_ID = 0

    class IrregularError(Exception):
        def __init__(self, name):
            super(Func.IrregularError, self).__init__(f'illegal practice on method {name}, you can only do it in regular function')

    @staticmethod
    def write(di):
        if di == {}:
            return ' 0 '
        s = ''
        for kk, vv in di.items():
            if vv == 1:
                if kk == 1:
                    s += f'+ x '
                else:
                    s += f'+ x ** {kk} '
            else:
                if kk == 1:
                    s += f'+ {vv} * x '
                else:
                    if kk == 0:
                        s += f'+ {vv} '
                    else:
                        s += f'+ {vv} * x ** {kk} '
        return s[2:]

    @staticmethod
    def scope(exp):
        Func.UNIQUE_ID += 1
        exec(f'def {Func.NAMESPACE}{Func.UNIQUE_ID}(x):\n\treturn {exp}')
        return locals()[f'{Func.NAMESPACE}{Func.UNIQUE_ID}']

    def __init__(self, expr=None, domain=None):
        self.kwargs = Param(['label_shift_xy', 'xy_up', 'xy_down'], label_shift_xy=(0, 0), xy_up=(0, 0), xy_down=(0, 0))  # passed into plt.graph, set by set
        self.discontinuities = []
        if expr is None:
            self.written = None
            self.di = {0: 0}
        elif isinstance(expr, dict):
            self.written = None
            self.di = expr
        elif isinstance(expr, list) or isinstance(expr, tuple):
            self.written = None
            self.di = {}
            for ii, dd in enumerate(expr):
                self.di[len(expr) - ii - 1] = dd
        elif isinstance(expr, int) or isinstance(expr, float):
            self.written = None
            self.di = {0: expr}
        else:
            self.written = str(expr)
            self.formulae = Func.scope(exp=self.written)
        if domain:
            self.domain = domain_initializer(domain)
        else:
            self.domain = Boundary((float('-inf'), float('inf')))

    # have not effect if self is regular polynomials
    def simplify(self):
        if not self.written:
            return self
        self.written = simplify(self.written).evalf(3)
        self.formulae = Func.scope(exp=self.written)
        return self

    def get_domain(self):
        return self.domain

    def set_domain(self, domain):
        self.domain = domain_initializer(domain)
        return self

    @property
    def coe(self):
        if self.written:
            raise Func.IrregularError('coe')
        self.full()
        self.sort()
        self.reverse()
        return list(self.di.values())

    def __str__(self):
        if self.written:
            expr = str(self.written) + ' '
        else:
            expr = 'f(x) = ' + Func.write(self.di)
        return expr[:-1] + ', f(x) \u2192 ' + self.domain.expression(2)

    def expression(self, rit):
        if self.written:
            return self.written
        di = {}
        if rit:
            for kk, vv in self.di.items():
                di[kk] = round(vv, rit)
        else:
            di = self.di
        return Func.write(di)

    def abbr(self, rit):
        if self.written:
            return str(self.written)
        else:
            return Func.write(round_dict(self.di, rit))

    def concat(self):
        if self.written:
            return Func(self.written, domain=domain_initializer(self.domain))
        else:
            di = {}
            for kk, vv in self.di.items():
                di[kk] = vv
            return Func(di, domain=domain_initializer(self.domain))

    def assign(self, other):
        if other.written:
            self.di = []
            self.written = other.written
            self.formulae = Func.scope(exp=self.written)
        else:
            ndi = {}
            for kk, vv in other.di.items():
                ndi[kk] = vv
            self.di = ndi

    # return each term as Func object
    def __iter__(self):
        if self.written:
            raise Func.IrregularError('__iter__')
        for kk, vv in self.di.items():
            yield Func({kk: vv}, domain=domain_initializer(self.domain))

    # self change
    # add 0 until reaches maximum index
    def full(self):
        if self.written:
            return
        self.part()
        if len(list(self.di.keys())) == 0:
            return self
        kks = list(self.di.keys())
        mk = max(kks)
        for ii in range(mk):
            ind = mk - ii - 1
            try:
                self.di[ind]
            except KeyError:
                self.di[ind] = 0
        return self

    def sort(self):
        if self.written:
            return
        self.di = dict(sorted(self.di.items()))
        return self

    def reverse(self):
        if self.written:
            return
        self.di = dict(reversed(self.di.items()))
        return self

    # self change
    # remove index 0 terms
    def part(self):
        if self.written:
            return
        di = {}
        for kk, vv in self.di.items():
            if vv != 0:
                di[kk] = vv
        self.di = di
        return self

    def is_constant(self):
        if self.written:
            raise Func.IrregularError('is_constant')
        # if is_constant, then is_single must be True
        self.part()
        kks = list(self.di.keys())
        return len(kks) == 1 and kks[0] == 0

    def is_single(self):
        if self.written:
            raise Func.IrregularError('is_single')
        self.part()
        ll = len(list(self.di.keys()))
        return ll == 1 or ll == 0

    def single(self):
        if self.written:
            raise Func.IrregularError('single')
        # only call when is_single == True
        kk = list(self.di.keys())[0]
        return [kk, self.di[kk]]

    def is_zero(self):
        # y = 0
        if self.written:
            return self.written.strip() == '0'
        return self.is_single() and self.di == {}

    def leading_term(self):
        # return the one with maximum index
        if self.written:
            raise Func.IrregularError('leading_term')
        mk = max(list(self.di.keys()))
        return Func({mk: self.di[mk]})

    def ending_term(self):
        if self.written:
            raise Func.IrregularError('ending_term')
        lk = min(list(self.di.keys()))
        return Func({lk: self.di[lk]})

    def pop(self):
        if self.written:
            raise Func.IrregularError('pop')
        self.part()
        et = self.ending_term()
        self.assign(self - et)
        return et

    def __eq__(self, other):
        if self.written or other.written:
            return str(self) == str(other)
        else:
            return self.coe == other.coe

    # compare leadinng exponential
    def __gt__(self, other):
        if self.written or other.written:
            return max(exponents(str(self))) > max(exponents(str(other)))
        else:
            return len(self.coe) > len(other.coe)

    def __lt__(self, other):
        if self.written or other.written:
            return max(exponents(str(self))) < max(exponents(str(other)))
        else:
            return len(self.coe) < len(other.coe)

    def __add__(self, other):
        nfu = self.concat()
        nfu += other
        return nfu

    def __iadd__(self, other):
        if isinstance(other, Func):
            if other.written:
                self.written = simplify('(' + self.expression(0).strip() + ') + (' + str(other.written) + ')').evalf(3)
                self.formulae = Func.scope(self.written)
                self.di = []
            else:
                for kk, vv in other.di.items():
                    try:
                        self.di[kk] += vv
                    except KeyError:
                        self.di[kk] = vv
                self.domain.intersect(other.domain)
        else:
            if self.written:
                self.written = simplify(str(self.expression(0)) + ' + ' + str(other)).evalf(3)
                self.formulae = Func.scope(self.written)
            else:
                # int or float
                try:
                    self.di[0] += other
                except KeyError:
                    self.di[0] = other
        return self

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        nfu = self.concat()
        nfu -= other
        return nfu

    def __isub__(self, other):
        if isinstance(other, Func):
            if other.written:
                self.written = simplify('(' + str(self.expression(0)).strip() + ') - (' + str(other.written) + ')').evalf(3)
                self.formulae = Func.scope(self.written)
                self.di = []
            else:
                for kk, vv in other.di.items():
                    try:
                        self.di[kk] -= vv
                    except KeyError:
                        self.di[kk] = -vv
            self.domain.intersect(other.domain)
        else:
            if self.written:
                self.written = simplify(str(self.expression(0)) + str(-other)).evalf(3)
                self.formulae = Func.scope(self.written)
            else:
                # int or float
                try:
                    self.di[0] -= other
                except KeyError:
                    self.di[0] = -other
        return self

    # return new
    def __neg__(self):
        if self.written:
            return Func(simplify('- (' + self.expression(0).strip() + ')').evalf(3), domain=domain_initializer(self.domain))
        else:
            di = {}
            for kk, vv in self.di.items():
                di[kk] = -vv
            return Func(di, domain=domain_initializer(self.domain))

    def __rsub__(self, other):
        # can only be number - self
        return -self + other

    def __mul__(self, other):
        nfu = self.concat()
        nfu *= other
        return nfu

    def __imul__(self, other):
        ndi = {}
        if isinstance(other, Func):
            if other.written:
                self.written = simplify('(' + self.expression(0).strip() + ') * (' + other.written + ')').evalf(3)
                self.formulae = Func.scope(self.written)
                self.di = []
            else:
                self.part()
                other.part()
                for term1 in self:
                    for term2 in other:
                        t1 = term1.single()
                        t2 = term2.single()
                        kk = t1[0] + t2[0]
                        vv = t1[1] * t2[1]
                        try:
                            ndi[kk] += vv
                        except KeyError:
                            ndi[kk] = vv
            self.domain.intersect(other.domain)
        else:
            if self.written:
                self.written = simplify('(' + str(self.expression(0)) + ') * ' + str(other)).evalf(3)
                self.formulae = Func.scope(self.written)
            else:
                # int or float
                for kk, vv in self.di.items():
                    ndi[kk] = vv * other
                self.domain *= other
        self.di = ndi
        return self

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        nfu = self.concat()
        nfu /= other
        return nfu

    def __itruediv__(self, other):
        if isinstance(other, Func):
            if other.written:
                self.written = simplify('(' + self.expression(0).strip() + ') / (' + other.written + ')').evalf(3)
                self.formulae = Func.scope(self.written)
                self.di = []
            else:
                k1, v1 = self.leading_term().single()
                k2, v2 = other.leading_term().single()
                term = Func({k1 - k2: v1 / v2})
                rest = term * other
                remain = self - rest
                if remain > self:
                    raise TypeError(f'Sorry, we cannot divide <{remain}> by <{other}>')
                elif remain.is_zero():
                    return term
                else:
                    term += remain / other
                self.assign(term)
            self.domain.intersect(other.domain)
        else:
            if self.written:
                self.written = simplify('(' + str(self.expression(0)) + ') / ' + str(other)).evalf(3)
                self.formulae = Func.scope(self.written)
            else:
                # int or float
                ndi = {}
                for kk, vv in self.di.items():
                    ndi[kk] = vv / other
                self.di = ndi
                self.domain /= other
        return self

    def __pow__(self, power, modulo=None):
        nfu = self.concat()
        nfu **= power
        return nfu

    def __ipow__(self, power):
        if (not self.write) and power > 0 and isinstance(power, int):
            other = int(power)
            if self.is_single():
                di = {}
                kk, vv = self.single()
                di[int(kk * other)] = vv ** other
                self.di = di
            else:
                self.part()
                term = self.pop()
                # (self + term)^other
                res = Func()
                for c1, coe in enumerate(pascal(other)):
                    c2 = other - c1
                    res += coe * self ** c1 * term ** c2
                return res
            self.domain **= power
        elif isinstance(power, Func):
            self.written = simplify('(' + self.expression(0).strip() + ') ** (' + power.expression(0) + ')').evalf(3)
            self.formulae = Func.scope(self.written)
            self.di = []
            self.domain.intersect(power.domain)
        else:
            self.written = simplify('(' + str(self.expression(0)) + ') ** (' + str(power) + ')').evalf(3)
            self.formulae = Func.scope(self.written)
            self.di = []
        return self

    # return new Func object
    def derivative(self):
        if self.written:
            return Func(diff(self.written).evalf(3), domain=domain_initializer(self.domain))
        else:
            di = {}
            for kk, vv in self.di.items():
                if kk != 0:
                    di[kk - 1] = vv * kk
            return Func(di, domain=domain_initializer(self.domain))

    # point = [x, y]
    def integral(self, point=None):
        if self.written or self.is_abnormal():
            func = Func(simplify(integrate(self.expression(0))).evalf(3), domain=domain_initializer(self.domain))
        else:
            di = {}
            for kk, vv in self.di.items():
                di[kk + 1] = vv / (kk + 1)
            func = Func(di, domain=domain_initializer(self.domain))
        if point:
            return func.calc_constant(point)
        else:
            return func

    def is_abnormal(self):
        for kk, vv in self.di.items():
            if kk < 0:
                return True
        return False

    # calculation
    def formula(self, x, ignore_domain=False):
        if isinstance(x, list) or isinstance(x, tuple):
            return [self.formula(x_, ignore_domain=ignore_domain) for x_ in x]
        else:
            if self.written:
                expr = self.formulae
            else:
                expr = ExponentialParabola.hook(Func.write(self.di))
            if ignore_domain or x in self.domain:
                return expr(x)
            return None

    def has_constant(self):
        if self.written:
            raise Func.IrregularError('has_constant')
        self.part()
        try:
            self.di[0] = self.di[0]
            return True
        except KeyError:
            return False

    @property
    def constant(self):
        if self.written:
            raise Func.IrregularError('has_constant')
        return self.di[0]

    # point = [x, y]
    def calc_constant(self, point):
        if self.written:
            self.written += ' + ' + str(point[1] - self.formula(point[0]))
        else:
            if self.has_constant():
                cc = self.constant
            else:
                cc = 0
            self.di[0] = cc + point[1] - self.formula(point[0])
        return self

    def tangent(self, xx):
        nf = Func({1: self.derivative().formula(xx)}, domain=domain_initializer(self.domain))
        return nf.calc_constant([xx, self.formula(xx)])

    def normal(self, xx):
        tangent = self.tangent(xx)
        coe = tangent.coe
        return Func({1: -1 / coe[0]}, domain=domain_initializer(self.domain)).calc_constant([xx, self.formula(xx)])

    def sample(self, n, x_start=None, x_end=None, ignore_discontinuity=False) -> Vectors:
        if isinstance(n, list):
            return Vectors(Vector(x_val=n, y_val=[self.formula(xx, ignore_domain=True) for xx in n]))
        else:
            if ignore_discontinuity:
                domain = self.domain
            else:
                domain = self.domain_with_discontinuity
            if x_start is None:
                if x_end is None:
                    # [None, None]
                    domain = domain.concat()
                else:
                    # [None, x_end]
                    domain = domain.slice_right_(x_end)
            else:
                if x_end is None:
                    # [x_start, None]
                    domain = domain.slice_left_(x_start)
                else:
                    # [x_start, x_end]
                    domain = domain.slice_left_(x_start).slice_right(x_end)
            xs = domain.linespace(n)
            if isinstance(xs[0], list):
                return Vectors(*[Vector(x_val=xs[ii], y_val=[self.formula(xx, ignore_domain=True) for xx in xs[ii]]) for ii in range(len(xs))])
            else:
                return Vectors(Vector(x_val=xs, y_val=[self.formula(xx, ignore_domain=True) for xx in xs]))

    def roots(self):
        if self.written:
            res = []
            for es in solve(self.written):
                if es.is_real:
                    va = es.evalf()
                    if va in self.domain:
                        res.append(float(va))
            return res
        else:
            rts = np.roots(self.coe)
            nrt = rts[np.isreal(rts)]
            return self.domain.filter(nrt.real.tolist())[0]

    def intersect(self, other):
        xs = (self - other).roots()
        ys = [self.formula(xx) for xx in xs]
        return Vector(x_val=xs, y_val=ys).single()

    # set kwargs to pass into plotting graph
    def set(self, **kwargs):
        self.kwargs.set(**kwargs)
        return self

    def get(self, key):
        return self.kwargs.get(key)

    def graph(self, n=50, fig=None, ax=None, cartesian=False, square=False):
        return GraphFunc(self, n, fig=fig, ax=ax, cartesian=cartesian, square=square)

    @property
    def asymptotes(self):
        try:
            n, d = fraction(self.expression(0))
            return Func(d).roots()
        except Exception:
            return []

    """
    if you know a discontinuity value that the program is not able to calculate
    in form of a list, a domain (Boundary or Lim), or a numeric value, set it here
    then it will be taken into calculation of domain_with_discontinuity property
    and reflect in graph
    """
    def discontinuity(self, *va):
        self.discontinuities = va
        return self

    @property
    def domain_with_discontinuity(self):
        return self.domain.concat().exclude(self.asymptotes, *self.discontinuities)


class Segment:
    def __init__(self, *funcs):
        for func in funcs:
            if not isinstance(func, Func):
                raise TypeError('<Segment> construct with array of functions')
        self.funcs = [func for func in funcs]

    def append(self, func):
        if not isinstance(func, Func):
            raise TypeError('<Segment> append takes a Func object as parameter')
        self.funcs.append(func)

    def get_domain(self):
        dm = self.funcs[0].domain
        for func in self.funcs[1:]:
            dm.union(func.domain)
        return dm

    def sort(self):
        # sort by domain
        funcs = []
        inds = []
        for func in self.funcs:
            inds.append(func.domain.left)
        while len(inds) != 0:
            mi = inds.index(min(inds))
            funcs.append(self.funcs.pop(mi))
            inds.pop(mi)
        self.funcs = funcs
        return self

    def __str__(self):
        ss = '<Segment\n'
        for func in self.funcs:
            ss += '\t' + str(func) + '\n'
        ss += '>'
        return ss

    def concat(self):
        return Segment(*[func.concat() for func in self.funcs])

    def __add__(self, other):
        nsg = self.concat()
        nsg += other
        return nsg

    def __iadd__(self, other):
        for func in self.funcs:
            func += other
        return self

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        nsg = self.concat()
        nsg -= other
        return nsg

    def __isub__(self, other):
        for func in self.funcs:
            func -= other
        return self

    def __neg__(self):
        nsg = self.concat()
        for func in nsg.funcs:
            func.assign(-func)
        return nsg

    def __rsub__(self, other):
        return - self + other

    def __mul__(self, other):
        nsg = self.concat()
        nsg *= other
        return nsg

    def __imul__(self, other):
        for func in self.funcs:
            func *= other
        return self

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        nsg = self.concat()
        nsg /= other
        return nsg

    def __itruediv__(self, other):
        for func in self.funcs:
            func /= other
        return self

    def __pow__(self, power, modulo=None):
        nsg = self.concat()
        nsg **= power
        return nsg

    def __ipow__(self, other):
        for func in self.funcs:
            func **= other
        return self

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.funcs[item]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.funcs[key] = value

    def __iter__(self):
        for func in self.funcs:
            yield func

    def sample(self, n, x_start=None, x_end=None, ignore_discontinuity=False) -> Vectors:
        if isinstance(n, list):
            # return Vectors(Vector(x_val=n, y_val=[self.formula(xx, ignore_domain=True) for xx in n]))
            return Vectors(*[Vector(x_val=n, y_val=[func.formula(xx, ignore_domain=True) for xx in n]) for func in self.funcs])
        else:
            sg = self.concat()
            lengths = []
            for func in sg:
                if func.domain.has_infinity():
                    if func.domain.infinity_both():
                        func.domain.slice_left(x_start).slice_right(x_end)
                    elif func.domain.infinity_left():
                        func.domain.slice_left(x_start)
                    else:
                        func.domain.slice_right(x_end)
                lengths.append(func.domain.length())
            total = sum(lengths)
            # vectors
            vectors = []
            for func in sg:
                amt = round(func.domain.length() / total * n)
                if amt < 1:
                    amt = 1
                vectors.append(func.sample(n=amt, ignore_discontinuity=ignore_discontinuity))
            return Vectors(*vectors)

    def graph(self, n=50, fig=None, ax=None, cartesian=False, square=False):
        return GraphSegment(self, n, fig=fig, ax=ax, cartesian=cartesian, square=square)

    def domain(self, domain):
        nd = domain_initializer(domain)
        for func in self.funcs:
            func.domain = nd.concat()
        return self

    def roots(self):
        return one_d([func.roots() for func in self.funcs])

    def intersects(self):
        return one_d([f1.intersect(f2) for f1, f2 in roll(*self.funcs)])[0].single()


class GraphFunc(GraphStatic):
    def __init__(self, func, n, fig=None, ax=None, cartesian=False, square=False):
        super(GraphFunc, self).__init__(fig=fig, ax=ax, cartesian=cartesian, square=square)
        self.func = func
        self.n = n
        self.func.set(label_shift_xy=(0, 0))

    def __get_color(self, kwargs):
        # priority
        # kwargs > set > theme
        try:
            cc = kwargs['color']
            del kwargs['color']
            return cc
        except KeyError:
            try:
                return self.func.get('color')
            except KeyError:
                return self.get_color(0, 1)[0]

    def plot(self, domain=None, **kwargs):
        if domain is not None:
            self.func.set_domain(domain)
        try:
            self.func.set(color=kwargs['color'])
        except KeyError:
            pass
        di = {}
        di.update(self.func.kwargs.param())
        di.update(kwargs)
        self.func.sample(n=self.n).graph(fig=self.fig, ax=self.ax).plot(labels=str(self.func), color=self.__get_color(di), **di)
        return self

    def fill_between(self, xs=None, ys1=None, ys2=None, f=None, **kwargs):
        if f and isinstance(f, Func):
            nf = f.concat()
            if xs is None:
                nf.domain.intersect(self.func.domain)
                xs = nf.domain.linespace(self.n)
            ys1 = [self.func.formula(xx) for xx in xs]
            ys2 = [f.formula(xx) for xx in xs]
        return super(GraphFunc, self).fill_between(xs, ys1, ys2, **kwargs)

    def scatter(self, n=None, domain=None, **kwargs):
        if domain is not None:
            self.func.set_domain(domain)
        try:
            self.func.set(color=kwargs['color'])
        except KeyError:
            pass
        di = {}
        di.update(self.func.kwargs.param())
        di.update(kwargs)
        if n:
            n_ = n
        else:
            n_ = self.n
        self.func.sample(n=n_).graph(fig=self.fig, ax=self.ax).scatter(labels=[str(self.func)], color=self.__get_color(di), **di)
        return self

    def domain(self, label=True, rit=2, label_shift_xy=(0, 0), **kwargs):
        if self.func.get('label_shift_xy') != (0, 0):
            label_shift_xy = self.func.get('label_shift_xy')
        mk = self.func.domain.marker()
        for xx in mk['solid']:
            yy = self.func.formula(xx, True)
            self.ax.scatter(xx, yy, color=self.__get_color(kwargs), **kwargs)
            if label:
                self.ax.text(s=f"({round(xx, rit)}, {round(yy, rit)})", x=xx + label_shift_xy[0], y=yy + label_shift_xy[1])
        for xx in mk['empty']:
            yy = self.func.formula(xx, True)
            self.ax.scatter(xx, yy, edgecolors=self.__get_color(kwargs), facecolors='none', **kwargs)
            if label:
                self.ax.text(s=f"({round(xx, rit)}, {round(yy, rit)})", x=xx + label_shift_xy[0], y=yy + label_shift_xy[1])
        return self

    def roots(self, rit=2, label_shift_xy=(0, 0), **kwargs):
        if self.func.get('label_shift_xy') != (0, 0):
            label_shift_xy = self.func.get('label_shift_xy')
        xs = self.func.roots()
        vts = Vectors(Vector(x_val=xs, y_val=self.func.formula(xs))).concat().round(rit)
        vts.graph(fig=self.fig, ax=self.ax).scatter(color=self.__get_color(kwargs), **kwargs).label(label_shift_xy=label_shift_xy)
        return self

    def intercepts_x(self, rit=2, label_shift_xy=(0, 0), **kwargs):
        if self.func.get('label_shift_xy') != (0, 0):
            label_shift_xy = self.func.get('label_shift_xy')
        return self.roots(rit=rit, label_shift_xy=label_shift_xy, **kwargs)

    def intercepts_y(self, rit=2, label_shift_xy=(0, 0), **kwargs):
        if self.func.get('label_shift_xy') != (0, 0):
            label_shift_xy = self.func.get('label_shift_xy')
        Vectors(Vector(x_val=[0], y_val=[self.func.formula(0)])).round(rit).graph(fig=self.fig, ax=self.ax).scatter(color=self.__get_color(kwargs), **kwargs).label(label_shift_xy=label_shift_xy)
        return self

    def xlim(self, xs=None, padding=0):
        if xs is None:
            super(GraphFunc, self).xlim([self.func.domain.left - padding, self.func.domain.right + padding])
        else:
            super(GraphFunc, self).xlim(xs)
        return self

    def ylim(self, ys=None, padding=0):
        if ys is None:
            arr = [self.func.formula(xx) for xx in one_d(self.func.domain.linespace(50))]
            super(GraphFunc, self).ylim([min(arr) - padding, max(arr) + padding])
        else:
            super(GraphFunc, self).ylim([ys[0], ys[1]])
        return self

    def lim(self, arr=None, padding=0):
        return self.xlim(xs=arr, padding=padding).ylim(ys=arr, padding=padding)

    def suit_bezier(self, n=None):
        if n:
            n_ = n
        else:
            n_ = self.n
        return self.func.sample(n=n_).graph(fig=self.fig, ax=self.ax).suit_bezier().add_theme(*self.themes)

    def suit_linear(self, n=None):
        if n:
            n_ = n
        else:
            n_ = self.n
        return self.func.sample(n=n_).graph(fig=self.fig, ax=self.ax).suit_linear().add_theme(*self.themes)


class GraphSegment(GraphStatic):
    def __init__(self, segment, n, fig=None, ax=None, cartesian=False, square=False):
        super(GraphSegment, self).__init__(fig=fig, ax=ax, cartesian=cartesian, square=square)
        self.segment = segment
        self.n = n

    def plot(self, **kwargs):
        colors = self.__get_color(kwargs)
        for ii, func in enumerate(self.segment.funcs):
            di = {'color': colors[ii]}
            di.update(func.kwargs.param())
            di.update(kwargs)
            func.graph(n=self.n, fig=self.fig, ax=self.ax).plot(**di)
        return self

    def scatter(self, n=None, **kwargs):
        colors = self.__get_color(kwargs)
        for ii, func in enumerate(self.segment.funcs):
            di = {'color': colors[ii]}
            di.update(func.kwargs.param())
            di.update(kwargs)
            if n:
                n_ = n
            else:
                n_ = self.n
            func.graph(n=n_, fig=self.fig, ax=self.ax).scatter(**di)
        return self

    def fill_between(self, ind1, ind2, xs=None, **kwargs):
        if xs:
            Data(
                xs,
                [
                    one_d([vt.y for vt in self.segment[ind1].sample(xs)]),
                    one_d([vt.y for vt in self.segment[ind2].sample(xs)]),
                ]
            ).graph(fig=self.fig, ax=self.ax).fill_between(0, 1, **kwargs)
        else:
            Vectors(
                self.segment[ind1].sample(self.n),
                self.segment[ind2].sample(self.n)
            ).graph(fig=self.fig, ax=self.ax).fill_between(0, 1, **kwargs)
        return self

    def domain(self, funcs=None, label=True, rit=2, label_shift_xy=(0, 0), **kwargs):
        for ii, func in enumerate(self.segment.funcs):
            if funcs is not None:
                if ii in funcs:
                    func.graph(n=self.n, fig=self.fig, ax=self.ax).domain(label=label, rit=rit,
                                                                          label_shift_xy=label_shift_xy, **kwargs)
            else:
                func.graph(n=self.n, fig=self.fig, ax=self.ax).domain(label=label, rit=rit,
                                                                      label_shift_xy=label_shift_xy, **kwargs)
        return self

    def __get_color(self, kwargs):
        # priority
        # kwargs > set > theme
        try:
            cc = kwargs['color']
            del kwargs['color']
            return cc
        except KeyError:
            colors = []
            for ii, func in enumerate(self.segment.funcs):
                try:
                    colors.append(func.get('color'))
                except KeyError:
                    colors.append(self.get_color(ii, 1)[0])
            return colors

    def intersects(self, label=True, label_shift_xy=(0, 0), **kwargs):
        x_val = []
        y_val = []
        for func1, func2 in roll(*self.segment.funcs):
            vt = func1.intersect(func2)
            x_val += vt.x
            y_val += vt.y
        vtg = Vectors(Vector(x_val=x_val, y_val=y_val).single()).graph(fig=self.fig, ax=self.ax).scatter(color=self.__get_color(kwargs)[0], **kwargs)
        if label:
            vtg.label(label_shift_xy=label_shift_xy)
        return self

    def roots(self, funcs=None, rit=2, label_shift_xy=(0, 0), **kwargs):
        for ii, func in enumerate(self.segment.funcs):
            if funcs is not None:
                if ii in funcs:
                    func.graph(fig=self.fig, ax=self.ax).roots(rit=rit, label_shift_xy=label_shift_xy, **kwargs)
            else:
                func.graph(fig=self.fig, ax=self.ax).roots(rit=rit, label_shift_xy=label_shift_xy, **kwargs)
        return self

    def intercepts_x(self, funcs=None, rit=2, label_shift_xy=(0, 0), **kwargs):
        for ii, func in enumerate(self.segment.funcs):
            if funcs is not None:
                if ii in funcs:
                    func.graph(fig=self.fig, ax=self.ax).intercepts_x(rit=rit, label_shift_xy=label_shift_xy, **kwargs)
            else:
                func.graph(fig=self.fig, ax=self.ax).intercepts_x(rit=rit, label_shift_xy=label_shift_xy, **kwargs)
        return self

    def intercepts_y(self, funcs=None, rit=2, label_shift_xy=(0, 0), **kwargs):
        for ii, func in enumerate(self.segment.funcs):
            if funcs is not None:
                if ii in funcs:
                    func.graph(fig=self.fig, ax=self.ax).intercepts_y(rit=rit, label_shift_xy=label_shift_xy, **kwargs)
            else:
                func.graph(fig=self.fig, ax=self.ax).intercepts_y(rit=rit, label_shift_xy=label_shift_xy, **kwargs)
        return self

    def xlim(self, xs=None, padding=0):
        if xs is None:
            dm = self.segment.get_domain()
            super(GraphSegment, self).xlim([dm.left - padding, dm.right + padding])
        else:
            super(GraphSegment, self).xlim(xs)
        return self

    def ylim(self, ys=None, padding=0):
        if ys is None:
            arr = one_d([one_d([self.segment[ii].formula(xx) for xx in self.segment[ii].domain.linespace(50)]) for ii in range(len(self.segment.funcs))])
            super(GraphSegment, self).ylim([min(arr) - padding, max(arr) + padding])
        else:
            super(GraphSegment, self).ylim([ys[0], ys[1]])
        return self

    def lim(self, arr=None, padding=0):
        return self.xlim(xs=arr, padding=padding).ylim(ys=arr, padding=padding)

    def suit_bezier(self, n=None):
        if n:
            n_ = n
        else:
            n_ = self.n
        vts = Vectors(*[func.sample(n_) for func in self.segment])
        return vts.graph(fig=self.fig, ax=self.ax).suit_bezier().add_theme(*self.themes)

    def suit_linear(self, n=None):
        if n:
            n_ = n
        else:
            n_ = self.n
        vts = Vectors(*[func.sample(n_) for func in self.segment])
        return vts.graph(fig=self.fig, ax=self.ax).suit_linear().add_theme(*self.themes)


def oblique(dt1, dt2, domain=None):
    try:
        k = (dt2[1] - dt1[1]) / (dt2[0] - dt1[0])
        # b = y - kx
        b = dt2[1] - k * dt2[0]
        return Func({1: k, 0: b}, domain=domain)
    except ZeroDivisionError:
        # y = 0
        return Func(domain=domain)


def least_square_alg(vector):
    ax = vector.x
    ay = vector.y
    cx = sum(ax) / len(ax)
    cy = sum(ay) / len(ay)
    dx = [xx - cx for xx in ax]
    dy = [yy - cy for yy in ay]
    sdx = [xx ** 2 for xx in dx]
    dxy = [dy[ii] * xx for ii, xx in enumerate(dx)]
    b1 = sum(dxy) / sum(sdx)
    nf = Func({1: b1})
    return nf.calc_constant([cx, cy])


class RegressFunc(Vectors):
    def __init__(self, *args, auto_domain=True, padding=0):
        self.auto_domain = auto_domain
        self.padding = padding
        self.caches = []
        super(RegressFunc, self).__init__(*args)

    # do not call it outside of class, it is used to record procedure for std variance
    def add_cache(self, val):
        self.caches.append(val)

    def clean_cache(self):
        self.caches = []

    def simulate(self, other):
        for di in self.caches:
            kk = list(di.keys())[0]
            vv = list(di.values())[0]
            kk(other, *vv['args'], **vv['kwargs'])
        return self

    def record(foo):
        def wrapper(self, *args, **kwargs):
            self.add_cache({foo: {'args': args, 'kwargs': kwargs}})
            return foo(self, *args, **kwargs)
        return wrapper

    def add_formula(self, func):
        if self.auto_domain:
            xs = []
            for vt in self:
                xs += vt.x_val
            func.set_domain([min(xs) - self.padding, max(xs) + self.padding])
        self.formulas.append(func)

    @record
    def linear(self, least_square=True):
        self.formulas = []
        if least_square:
            for vt in self:
                self.add_formula(least_square_alg(vt))
        else:
            for vt in self:
                coe = linear_regression(
                    x=vt.x,
                    y=vt.y,
                ).coe
                self.add_formula(Func({1: coe['k'], 0: coe['b']}))
        return self

    @record
    def parabola(self, depth=8):
        for vt in self:
            coe = parabola_regression(x=vt.x, y=vt.y, depth=depth).coe
            self.add_formula(Func({2: coe['a'], 1: coe['b'], 0: coe['c']}))
        return self

    @record
    def cubic(self, depth=8):
        for vt in self:
            coe = cubic_regression(x=vt.x, y=vt.y, depth=depth).coe
            self.add_formula(Func({3: coe['a'], 2: coe['b'], 1: coe['c'], 0: coe['d']}))
        return self

    @record
    def quadratic(self, depth=8):
        for vt in self:
            coe = quadratic_regression(x=vt.x, y=vt.y, depth=depth).coe
            self.add_formula(Func({4: coe['a'], 3: coe['b'], 2: coe['c'], 1: coe['d'], 0: coe['e']}))
        return self

    @record
    def exponential(self, x_exp, depth=8):
        # y = ax^n + bx^(n-1) + cx^(n-2) ...
        for vt in self:
            coe = exponential_parabola_regression(x_exp=x_exp, x=vt.x, y=vt.y, depth=depth).coe
            self.add_formula(Func(coe_decode(coe)))
        return self

    # y^k = product / (ax^n + bx^(n-1) + cx^(n-2) + ...)
    @record
    def inverse_exponential(self, product, y_exp, x_exp, depth=8):
        for vt in self:
            expr = inverse_exponential_regression(product=product, y_exp=y_exp, x_exp=x_exp, x=vt.x, y=vt.y,
                                                  depth=depth)
            self.add_formula(Func(expr.write))
        return self

    # x = None,
    # y = None,
    # dots = None,
    # x_power_range = (1, 2, 3, 4),
    # y_power_range = (1, 2, 3, 4),
    # product_range = (1, 2, 3, 4),
    @record
    def regression(
            self,
            x_power_range=(1, 2, 3, 4),
            y_power_range=(1, 2, 3, 4),
            product_range=(1, 2, 3, 4),
    ):
        for ii, xs in enumerate(self.xs):
            ys = self.ys[ii]
            expr = regression(x=xs, y=ys, x_power_range=x_power_range, y_power_range=y_power_range, product_range=product_range)
            if expr.category == InverseExponentialParabola:
                self.add_formula(Func(expr.write))
            else:
                self.add_formula(Func(coe_decode(expr.coe)))
        return self


class GraphVectors(GraphData):
    ROUND = 2

    def __init__(self, vectors, fig=None, ax=None, cartesian=False, square=False):
        super(GraphVectors, self).__init__(vectors, fig=fig, ax=ax, cartesian=cartesian, square=square)

    def __get_xlim(self):
        xxs = []
        for xx in self.data.xs:
            xxs.append(min(xx))
            xxs.append(max(xx))
        return [min(xxs), max(xxs)]

    def xlim(self, xs=None, padding=0):
        if xs is None:
            xs = self.__get_xlim()
            xs[0] -= padding
            xs[1] += padding
        plt.xlim(xs)
        return self

    def label(self, label_shift_xy=(0, 0)):
        for jj, [xs, ys] in enumerate(zip(self.data.xs, self.data.ys)):
            for ii, xx in enumerate(xs):
                yy = ys[ii]
                if label_shift_xy == (0, 0):
                    try:
                        label_shift_xy = self.data[jj].get('label_shift_xy')
                    except KeyError:
                        pass
                self.ax.text(s=f"({round(xx, GraphData.ROUND)}, {round(yy, GraphData.ROUND)})", x=xx + label_shift_xy[0],
                             y=yy + label_shift_xy[1])
        return self

    def fill_between(self, ind1, ind2, **kwargs):
        return GraphStatic.fill_between(self, self.data.xs[ind1], self.data.ys[ind1], self.data.ys[ind2], **kwargs)

    def bar(self, width, color=None, label=False, xy_up=(0, 0), xy_down=(0, 0), **kwargs):
        n = len(self.data.ys)
        for ii, shift in enumerate(commute(width, n)):
            xs = self.data.xs[ii]
            yy = self.data.ys[ii]
            di = {}
            if color:
                if isinstance(color, str) or (isinstance(color, tuple) and len(color) == 3):
                    di['color'] = color
                else:
                    di['color'] = color
            else:
                di['color'] = self.get_color(ii, len(yy))
            try:
                di['width'] = self.data[ii].kwargs.get('width')
            except KeyError:
                di['width'] = width
            di.update(self.data[ii].kwargs.param())
            di.update(kwargs)
            vertical = self.ax.bar([xx + shift for xx in xs], yy, **di)
            if label:
                if xy_up == (0, 0):
                    try:
                        xy_up = self.data[ii].get('xy_up')
                    except KeyError:
                        pass
                if xy_down == (0, 0):
                    try:
                        xy_down = self.data[ii].get('xy_down')
                    except KeyError:
                        pass
                GraphData.auto_label_bar(vertical_=vertical, colors=di['color'], xy_up=xy_up, xy_down=xy_down)
        return self

    def errorbar(self, error, label=True, label_shift_xy=(0, 0), **kwargs):
        for ii, yy in enumerate(self.data.ys):
            colors = self.get_color(ii, 1)
            xs = self.data.xs[ii]
            self.ax.errorbar(xs, yy, yerr=error, color=colors[0], **kwargs)
            if label:
                if label_shift_xy == (0, 0):
                    try:
                        label_shift_xy = self.data[ii].get('label_shift_xy')
                    except KeyError:
                        pass
                for jj, x_ in enumerate(xs):
                    y_ = yy[jj]
                    self.ax.text(s=f"({round(x_, GraphData.ROUND)}, {round(y_, GraphData.ROUND)})",
                                 x=x_ + label_shift_xy[0], y=y_ + label_shift_xy[1])
        return self

    def plot(self, labels=None, color=None, **kwargs):
        if labels is None:
            labels = [None for ii in range(len(self.data.ys))]
        elif isinstance(labels, str):
            labels = [labels]
            for ii in range(len(self.data.ys) - 1):
                labels.append(None)
        for ii, yy in enumerate(self.data.ys):
            di = {'label': labels[ii]}
            if color is None:
                di['color'] = self.get_color(ii, 1)[0]
            else:
                di['color'] = color
            di.update(self.data[ii].kwargs.param())
            di.update(kwargs)
            self.ax.plot(self.data.xs[ii], yy, **di)
        return self

    def scatter(self, color=None, labels=None, **kwargs):
        if labels is None:
            labels = [None for ii in range(len(self.data.ys))]
        for ii, yy in enumerate(self.data.ys):
            di = {}
            if color is None:
                di['color'] = self.get_color(ii, len(yy))
            else:
                di['color'] = color
            di.update(self.data[ii].kwargs.param())
            di.update(kwargs)
            if color is None:
                self.ax.scatter(self.data.xs[ii], yy, label=labels[ii], **di)
            else:
                self.ax.scatter(self.data.xs[ii], yy, label=labels[ii], **di)
        return self

    def suit_bezier(self):
        return SuitVectorsBezier(self.data, self.fig, self.ax)

    def suit_linear(self):
        return SuitVectorsLinear(self.data, self.fig, self.ax)

    def suit_regress(self):
        return SuitVectorsRegress(self.data, self.fig, self.ax)


class SuitVectorsRegress(SuitRegress, GraphVectors):
    pass


class SuitVectorsBezier(GraphVectors):
    def static(self, color=None, n=100):
        for vt in self.data:
            if color is None:
                try:
                    cc = vt.get('color')
                except KeyError:
                    cc = Theme().random_negative().active(1)[0]
            else:
                cc = color
            bezier_draw(self.fig, self.ax, points=vt.dots, n=n, color=cc)
        return self

    def animate(self, color=None, n=100):
        for vt in self.data:
            if color is None:
                try:
                    cc = vt.get('color')
                except KeyError:
                    cc = Theme().random_negative().active(1)[0]
            else:
                cc = color
            self.add_cache(bezier_sketch(fig=self.fig, points=vt.dots, n=n, color=cc))
        return self

    def animate_partial(self, depth, n=100, interval=50):
        for vt in self.data:
            self.add_cache(bezier_illustrate(fig=self.fig, points=vt.dots, interval=interval, n=n, depth=depth))
        return self

    def animate_full(self, n=100, interval=50):
        for vt in self.data:
            self.add_cache(bezier_illustrate(fig=self.fig, points=vt.dots, interval=interval, n=n, depth=len(vt)))
        return self


class SuitVectorsLinear(GraphVectors):
    def linear(self, error, label=True, label_shift_xy=(0, 0)):
        self.themes = []
        self.grid()
        for ii, func in enumerate(self.data.regress().linear().formulas):
            yy = self.data.ys[ii]
            xs = [self.data[ii].x[0], self.data[ii].x[-1]]
            Data(xs, [func.formula(xx) for xx in xs]).graph(self.fig, self.ax).add_theme(Theme().gradient_negative(0)).plot(labels=[func.abbr(2)])
            self.add_theme(Theme().gradient_negative(30)).errorbar(error=error, label=label, label_shift_xy=label_shift_xy)
            # up to down
            oblique1 = oblique([xs[0], yy[0] + error], [xs[-1], yy[-1] - error])
            # down to up
            oblique2 = oblique([xs[0], yy[0] - error], [xs[-1], yy[-1] + error])
            Data(xs, [yy[0] + error, yy[-1] - error]).graph(self.fig, self.ax).add_theme(Theme().gradient_positive(0)).plot(labels=[oblique1.abbr(2)], linestyle='-.')
            Data(xs, [yy[0] - error, yy[-1] + error]).graph(self.fig, self.ax).add_theme(Theme().gradient_positive(0)).plot(labels=[oblique2.abbr(2)], linestyle='-.')
        return self

    def bar(self, width, label=False, xy_up=(0, 0), xy_down=(0, 0), **kwargs):
        self.themes = []
        themes = either(Theme().gradient_positive(-10), Theme().gradient_negative(10), n=len(self.data.ys))
        for theme in themes:
            self.add_theme(theme)
        super(SuitVectorsLinear, self).bar(width=width, label=label, xy_up=xy_up, xy_down=xy_down, **kwargs)
        return self

    def barh(self, tags, labels, axis='y'):
        if axis == 'y':
            Data(None, self.data.ys).graph(self.fig, self.ax).suit_linear().barh(tags, labels)
        elif axis == 'x':
            Data(None, self.data.xs).graph(self.fig, self.ax).suit_linear().barh(tags, labels)
        else:
            raise ValueError('barh axis must be either x or y')
        return self

    def scatter(self, labels=None, label_hline='avg', label_avg_plot=None):
        if labels is None:
            labels = [None for ii in range(len(self.data.ys))]
        for theme in either(Theme().gradient_positive(-10), Theme().gradient_negative(10), n=len(self.data.ys)):
            self.add_theme(theme)
        super(SuitVectorsLinear, self).scatter(labels=labels).average_line(label=label_hline).average_plot(label=label_avg_plot)
        data_avg = self.data.average()
        fill_color = Theme().random_positive().active(1)
        self.ax.fill_between(data_avg.xs[0], sum(data_avg.ys[0]) / len(data_avg.ys[0]), data_avg.ys[0], color=fill_color, alpha=0.3)
        return self






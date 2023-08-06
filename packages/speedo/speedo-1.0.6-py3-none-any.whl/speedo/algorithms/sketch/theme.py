import random
from speedo.algorithms.calculations.common import linespace


class Scheme:
    @staticmethod
    def restrict(val):
        # if outside [0, 1], assign to edge value
        res = val
        if val < 0:
            res = 0
        elif val > 1:
            res = 1
        return res

    def __init__(self, r, g, b, a=None):
        self.r = Scheme.restrict(r)
        self.g = Scheme.restrict(g)
        self.b = Scheme.restrict(b)
        if a is None:
            self.a = 1
        else:
            self.a = Scheme.restrict(a)
        self.kwargs = {}

    # return [0, 1]
    def __str__(self):
        return f'Scheme(r: {round(self.r, 2)}, g: {round(self.g, 2)}, b: {round(self.b, 2)}, a: {round(self.a, 2)})'

    # return [0, 255]
    def __repr__(self):
        return f'Scheme(r: {round(self.r * 255, 2)}, g: {round(self.g * 255, 2)}, b: {round(self.b * 255, 2)}, a: {round(self.a, 2)})'

    def rgb(self):
        return tuple([self.r, self.g, self.b])

    def rgba(self):
        return tuple([self.r, self.g, self.b, self.a])

    def __setitem__(self, key, value):
        self.kwargs[key] = value

    def __getitem__(self, item):
        return self.kwargs[item]

    def set_amount(self, amount):
        self.__setitem__('amount', amount)

    # private: generate random rgb based on hierarchy st, en -> [0, 255]
    @staticmethod
    def __generate(st, en):
        return random.randint(st, en) / 255

    @staticmethod
    def random():
        return Scheme(r=Scheme.__generate(0, 255), g=Scheme.__generate(0, 255), b=Scheme.__generate(0, 255))

    # random parser, return Scheme object
    @staticmethod
    def light():
        return Scheme(r=Scheme.__generate(170, 255), g=Scheme.__generate(170, 255), b=Scheme.__generate(170, 255))

    @staticmethod
    def medium():
        return Scheme(r=Scheme.__generate(85, 170), g=Scheme.__generate(85, 170), b=Scheme.__generate(85, 170))

    @staticmethod
    def dark():
        return Scheme(r=Scheme.__generate(0, 85), g=Scheme.__generate(0, 85), b=Scheme.__generate(0, 85))

    def concat(self):
        return Scheme(r=self.r, g=self.g, b=self.b, a=self.a)

    # return new Scheme instance
    def add(self, other):
        return Scheme(r=self.r + other, g=self.g + other, b=self.b + other, a=self.a)

    def add_opacity(self, other):
        return Scheme(r=self.r, g=self.g, b=self.b, a=self.a + other)

    def reduce(self, n, rgb):
        res = [self]
        for ii in range(n - 1):
            res.append(res[-1].add(rgb / 255))
        return res

    def reduce_opacity(self, n, alpha):
        res = [self]
        for ii in range(n - 1):
            res.append(res[-1].add_opacity(alpha))
        return res

    # return [tuple]
    @staticmethod
    def rgba_mapper(color_func):
        def wrapper(*args, **kwargs):
            return [tm.rgba() for tm in color_func(*args, **kwargs)]
        return wrapper

    def complementary(self):
        return Scheme(r=1-self.r, g=1-self.g, b=1-self.b)

    def reduce_complementary(self, n):
        return [Scheme(*aa) for aa in zip(*[linespace(cc, n) for cc in zip(self.rgb(), self.complementary().rgb())])]


class Color:
    # color series -> [rgb]
    @staticmethod
    @Scheme.rgba_mapper
    def color_light(n, rgb):
        return Scheme.light().reduce(n, rgb)

    @staticmethod
    @Scheme.rgba_mapper
    def color_medium(n, rgb):
        return Scheme.medium().reduce(n, rgb)

    @staticmethod
    @Scheme.rgba_mapper
    def color_dark(n, rgb):
        return Scheme.dark().reduce(n, rgb)

    @staticmethod
    @Scheme.rgba_mapper
    def opacity_light(n, alpha):
        sm = Scheme.dark()
        sm.a = 0.1
        return sm.reduce_opacity(n, alpha)

    @staticmethod
    @Scheme.rgba_mapper
    def opacity_medium(n, alpha):
        sm = Scheme.medium()
        sm.a = 0.5
        return Scheme.medium().reduce_opacity(n, alpha)

    @staticmethod
    @Scheme.rgba_mapper
    def opacity_dark(n, alpha):
        sm = Scheme.light()
        sm.a = 0.9
        return Scheme.dark().reduce_opacity(n, alpha)

    @staticmethod
    @Scheme.rgba_mapper
    def random_light(n):
        return [Scheme.light() for ii in range(n)]

    @staticmethod
    @Scheme.rgba_mapper
    def random_medium(n):
        return [Scheme.medium() for ii in range(n)]

    @staticmethod
    @Scheme.rgba_mapper
    def random_dark(n):
        return [Scheme.dark() for ii in range(n)]

    @staticmethod
    @Scheme.rgba_mapper
    def complementary(n):
        return Scheme.random().reduce_complementary(n)


class Theme:
    def __init__(self):
        def template(n):
            return n
        self.active = template
        self.desc = 0
        self.params = {}

    def is_empty(self):
        return self.desc == 0

    def __setitem__(self, key, value):
        self.params[key] = value

    def __getitem__(self, item):
        return self.params[item]

    def __default(self, n):
        self['n'] = n
        return [self['color'] for ii in range(self['n'])]

    def default(self, color='k'):
        self['color'] = color
        self.active = self.__default
        self.desc = f'default color: {color}'
        return self

    def __gradient_positive(self, n):
        self['n'] = n
        return Color.color_light(self['n'], self['rgb'])

    def gradient_positive(self, rgb):
        self['rgb'] = rgb
        self.active = self.__gradient_positive
        self.desc = f'gradient positive <rgb: {rgb}>'
        return self

    def __gradient_negative(self, n):
        self['n'] = n
        return Color.color_dark(self['n'], self['rgb'])

    def gradient_negative(self, rgb):
        self['rgb'] = rgb
        self.active = self.__gradient_negative
        self.desc = f'gradient negative <rgb: {rgb}>'
        return self

    def __opacity_positive(self, n):
        self['n'] = n
        return Color.opacity_light(self['n'], self['alpha'])

    def opacity_positive(self, alpha):
        self['alpha'] = alpha
        self.active = self.__opacity_positive
        self.desc = f'opacity positive <rgb: {alpha}>'
        return self

    def __opacity_negative(self, n):
        self['n'] = n
        return Color.opacity_dark(self['n'], self['alpha'])

    def opacity_negative(self, alpha):
        self['alpha'] = alpha
        self.active = self.__opacity_negative
        self.desc = f'opacity negative <rgb: {alpha}>'
        return self

    def __random_positive(self, n):
        self['n'] = n
        return Color.random_light(self['n'])

    def random_positive(self):
        self.active = self.__random_positive
        self.desc = 'random positive'
        return self

    def __random_medium(self, n):
        self['n'] = n
        return Color.random_medium(self['n'])

    def random_medium(self):
        self.active = self.__random_medium
        self.desc = 'random medium'
        return self

    def __random_negative(self, n):
        self['n'] = n
        return Color.random_dark(self['n'])

    def random_negative(self):
        self.active = self.__random_negative
        self.desc = 'random negative'
        return self

    def __complementary(self, n):
        self['n'] = n
        return Color.complementary(self['n'])

    def complementary(self):
        self.active = self.__complementary
        self.desc = 'complementary'
        return self


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    import matplotlib
    matplotlib.use('TkAgg')

    xs = [xx for xx in range(10)]
    ys = [yy * random.randint(4, 7) / 10 for yy in range(10)]

    plt.bar(xs, ys, color=Theme().complementary().active(10))
    plt.show()

    # plt.bar(xs, ys, color=Color.random_light(10))
    # plt.bar(xs, ys, color=Color.color_dark(10, 20))

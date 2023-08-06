"""
application programming interface

for each function, either pass in x and y values or [[x, y], [x, y]..] dots value
"""


from speedo.algorithms.regression.funcs import *
from speedo.algorithms.regression.describe import Write
from speedo.algorithms.regression.modules import Comparison, ready


@ready
def linear_regression(x=None, y=None, dots=None, depth=8):
    rgr = Linear(
        x_val=x,
        y_val=y,
        dots=dots,
        many=depth,
    )
    rgr.induce()
    ep = rgr.deduce()
    ep.set_write(Write.linear)
    return ep


@ready
def exponential_parabola_regression(x_exp, x=None, y=None, dots=None, depth=8):
    rgr = ExponentialParabola(
        exp=x_exp,
        x_val=x,
        y_val=y,
        dots=dots,
        many=depth,
    )
    rgr.induce()
    ep = rgr.deduce()
    ep.set_write(Write.exponential_parabola)
    return ep


@ready
def parabola_regression(x=None, y=None, dots=None, depth=8):
    return exponential_parabola_regression(
        x_exp=2,
        x=x,
        y=y,
        dots=dots,
        depth=depth,
    )


@ready
def cubic_regression(x=None, y=None, dots=None, depth=8):
    return exponential_parabola_regression(
        x_exp=3,
        x=x,
        y=y,
        dots=dots,
        depth=depth,
    )


@ready
def quadratic_regression(x=None, y=None, dots=None, depth=8):
    return exponential_parabola_regression(
        x_exp=4,
        x=x,
        y=y,
        dots=dots,
        depth=depth,
    )


@ready
def inverse_exponential_regression(product, y_exp, x_exp, x=None, y=None, dots=None, depth=8):
    epp = InverseExponentialParabola(
        pro=product,
        y_exp=y_exp,
        x_exp=x_exp,
        x_val=x,
        y_val=y,
        dots=dots,
        many=depth,
    )
    epp.induce()
    ep = epp.deduce()
    ep.set_write_variable(Write.inverse_exponential_parabola)
    return ep


@ready
def truncus_regression(x=None, y=None, dots=None, depth=8):
    return inverse_exponential_regression(
        product=1,
        y_exp=1,
        x_exp=2,
        x=x,
        y=y,
        dots=dots,
        depth=depth,
    )


"""
    just do it function
    x|y_power_range indicate a list of possible highest power of x|y, can only be integer
    product_range: if the function has inverse property, which xy = k, then product indicate possible k
"""


class Cache:
    EXPS = []

    @staticmethod
    def store(exp):
        Cache.EXPS.append(exp)

    @staticmethod
    def assign():
        Comparison.EXPRESSIONS = Cache.EXPS

    @staticmethod
    def clean():
        Cache.EXPS = []


@ready
def regression(
        x=None,
        y=None,
        dots=None,
        x_power_range=(1, 2, 3, 4),
        y_power_range=(1, 2, 3, 4),
        product_range=(1, 2, 3, 4),
):
    linear_regression(
        x=x,
        y=y,
        dots=dots,
    )

    if Comparison.compare().efficiency == 0:
        res = Comparison.compare()
        restart_regression_with_new_data()
        Cache.clean()
        return res

    for ii in x_power_range:
        try:
            Cache.store(exponential_parabola_regression(
                x_exp=ii,
                x=x,
                y=y,
                dots=dots,
            ))
        except ValueError:
            pass

    Cache.assign()
    if Comparison.compare().efficiency == 0:
        res = Comparison.compare()
        restart_regression_with_new_data()
        Cache.clean()
        return res

    for pro in product_range:
        for yy in y_power_range:
            for xx in x_power_range:
                try:
                    Cache.store(inverse_exponential_regression(
                        product=pro,
                        y_exp=yy,
                        x_exp=xx,
                        x=x,
                        y=y,
                        dots=dots,
                    ))
                    Cache.assign()
                    if Comparison.compare().efficiency == 0:
                        return Comparison.compare()

                except IndexError:
                    pass
                except ZeroDivisionError:
                    pass
    res = Comparison.compare()
    restart_regression_with_new_data()
    Cache.clean()
    return res


# clear past result
def restart_regression_with_new_data():
    Comparison.forget()
    Expression.DATA = None
    Expression.SIZE = 20
    Expression.INITIAL = None


# settings, needs to be called at the very start, after restart_regression_with_new_data, before regression
def set_sample_size(num):
    Expression.SIZE = num


if __name__ == '__main__':
    pass

    # expr = linear_regression(
    #     x=[1, 4, 12],
    #     y=[5, 5, 7]
    # )
    # print(expr)
    # print(expr.write)
    # print(expr.formula(2))

    # expr = linear_regression(
    #     x=[x for x in range(10)],
    #     y=[2 * y for y in range(10)],
    # )
    # print(expr)
    # print(expr.write)
    # print(expr.formula(2))

    # expr = parabola_regression(
    #     x=[x for x in range(10)],
    #     y=[2 * x ** 2 + 3 * x + 1 for x in range(10)],
    # )
    # print(expr)
    # print(expr.write)
    # print(expr.formula(2))

    # expr = exponential_parabola_regression(
    #     x_exp=5,
    #     x=[x for x in range(10)],
    #     y=[3 * x ** 5 + 2 * x ** 2 + 3 * x + 1 for x in range(10)],
    # )
    # print(expr)
    # print(expr.write)
    # print(expr.formula(2))

    # expr = cubic_regression(
    #     x=[x for x in range(10)],
    #     y=[6 * x ** 3 + 2 * x ** 2 + 3 * x + 1 for x in range(10)],
    # )
    # print(expr)
    # print(expr.write)
    # print(expr.formula(2))

    # expr = quadratic_regression(
    #     x=[x for x in range(10)],
    #     y=[10 * x ** 4 + 6 * x ** 3 + 2 * x ** 2 + 3 * x + 1 for x in range(10)],
    # )
    # print(expr)
    # print(expr.write)
    # print(expr.formula(2))

    # expr = inverse_exponential_regression(
    #     product=2,
    #     x_exp=2,
    #     y_exp=1,
    #     x=[x for x in range(20)],
    #     y=[2 / (4 * x ** 2 - 4 * x + 1) for x in range(20)],
    # )
    # print(expr)
    # print(expr.write)
    # print(expr.formula(2))

    # expr = truncus_regression(
    #     x=[x for x in range(20)],
    #     y=[1 / ((x + 2) ** 2) for x in range(20)],
    # )
    # print(expr)
    # print(expr.write)
    # print(expr.formula(2))

    # expr = regression(
    #     x=[x for x in range(20)],
    #     y=[1 / ((x + 2) ** 2) for x in range(20)],
    # )
    # print(expr.formula(2))


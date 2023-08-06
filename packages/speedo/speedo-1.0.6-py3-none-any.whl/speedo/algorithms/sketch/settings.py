from speedo.algorithms.regression.describe import Write
from speedo.algorithms.regression.modules import Expression


def set_precision(decimal_place: int):
    Write.DEFAULT = decimal_place


# sample rate is used to evaluate how efficient the expression is
# default to 10
# the result is sampled to this value and testified by
# passing x in formula and compare with expected y
def set_sample_rate(rate=10):
    Expression.SAMPLE_RATE = rate

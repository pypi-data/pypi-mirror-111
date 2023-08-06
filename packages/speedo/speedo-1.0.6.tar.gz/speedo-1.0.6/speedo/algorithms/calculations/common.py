import re


def reduce(n):
    a = 1
    for ii in range(n):
        a *= ii + 1
    return a


def pascal(n):
    for ii in range(n + 1):
        yield int(reduce(n) / reduce(ii) / reduce(n - ii))


def linespace(arr, n):
    st = arr[0]
    en = arr[1]
    step = (en - st) / (n - 1)
    res = []
    for ii in range(n):
        res.append(st + ii * step)
    return res


def updown(flt: float, n: int):
    val = round(flt)
    if val != flt:
        flag = True
        if val < flt:
            for ii in range(n):
                if flag:
                    yield val
                else:
                    yield val + 1
                flag = not flag
        else:
            for ii in range(n):
                if flag:
                    yield val
                else:
                    yield val - 1
                flag = not flag
    else:
        for ii in range(n):
            yield val


def alphabet_range(n):
    return [chr(i) for i in range(ord('a'), ord('a') + n)]


# 0 0
# 1 -width
# 2 width
# 3 2width
# 4 -2width
# 5 3width
# 6 -3width
# commute(20, 7)
# [0, -20, 20, -40, 40, -60, 60]
def commute(width, n):
    for ii in range(n):
        aa = (ii + 1) // 2
        if (ii % 2) == 0:
            yield aa * width
        else:
            yield -aa * width


# round dictionary values
def round_dict(di, rit):
    nd = {}
    for kk, vv in di.items():
        nd[kk] = round(vv, rit)
    return nd


# iterator([1, 2, 3], [4, 5, 6], [7, 8, 9], n=5)
# 1, 4, 7, 2, 5
def abstract(*args, n):
    ll = len(args)
    for ii in range(n):
        yield args[ii % ll][ii // ll]


# print([ii for ii in either(1, 2, 3, n=5)])
# [1, 2, 3, 1, 2]
def either(*args, n):
    ll = len(args)
    for ii in range(n):
        yield args[ii % ll]


# decode alphabetical coefficients to dictionary
def coe_decode(coe):
    if 'k' in list(coe.keys()):
        return {1: coe['k'], 0: coe['b']}
    n = len(list(coe.keys()))
    di = {}
    for ii, aa in enumerate(alphabet_range(n)):
        di[n - ii - 1] = coe[aa]
    return di


def string_list(text, n):
    return [text + ' ' + str(ii + 1) for ii in range(n)]


# merge dictionaries
def merge(*args):
    res = {}
    for di in args:
        for k, v in di.items():
            try:
                res[k].update(v)
            except KeyError:
                res[k] = v
    return res


def exponents(exp):
    return [int(m.group(1)) for m in re.finditer(r'\*\*\s*(-?\d+)', exp)]


# [1, 2, 3, 4] -> [1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]
def roll(*args):
    res = []
    for ii in range(len(args)):
        for jj in range(ii):
            res.append([args[jj], args[ii]])
    return res


def one_d(li):
    if isinstance(li[0], list):
        nli = []
        for ll in li:
            nli += ll
        return nli
    return li


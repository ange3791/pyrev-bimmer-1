from toolz.curried import pipe, map, filter, reduce
from math import modf

def list_diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

def list_count(list_in):
    list_out = list()
    for i in set(list_in):
        list_out.append([i, list_in.count(i)])

    return list_out

def iff(test, a, b):
    if test:
        return a
    else:
        return b


def conc(*args):
    #for arg in args
    x = pipe(   args,
                map(lambda x: iff(x is None, "", x)),
                tuple)

    return reduce(lambda a, b: a+b, x)


def left(str, num):
    if str is not None:
        return str[:num]
    else:
        return ""


def strfind(needle, haystack):
    if haystack is not None and needle in haystack:
        return True
    else:
        return False


def type_of(object, attribute):
    return getattr(object, attribute)


def between(n, n1, n2):
    if (n > n1 and n < n2) or (n < n1 and n > n2):
        return True
    else:
        return False


def round_to(x, nearest):
    n = modf(x)
    return n[1] + round(n[0] / nearest) * nearest


def make_key(x):
    return abs(hash(x) % (10 ** 8))

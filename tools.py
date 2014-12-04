import itertools
import math
import operator

import primes


def digits(n):
    return [int(i) for i in str(n)]


def sumOfDigits(n):
    return sum(digits(n))


def divisors(n):
    """Finds divisors by trying all possibilities"""
    sqrt = math.sqrt(n)
    yield 1
    for i in range(2, int(sqrt)+1):
        q, r = divmod(n, i)
        if r == 0:
            yield i
            yield q


def divisors2(n):
    """Finds divisors by taking all combinations of prime factors

    This is probably(?) faster than `divisors` for large numbers
    but slower for small ones
    """
    factors = primes.findFactors(n)
    divisors = set([1])
    for i in range(1, int(len(factors) / 2) + 1):
        for j in itertools.combinations(factors, i):
            p = product(j)
            if p in divisors:
                continue
            divisors.add(p)
            divisors.add(n / p)
    return divisors


def sumOfDivisors(n):
    return sum(divisors(n))


def product(array):
    return reduce(operator.mul, array)

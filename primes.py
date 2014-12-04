import heapq
import itertools
import math
import operator


def findFactors(target):
    sqrt = math.sqrt(target)
    primes = itertools.takewhile(lambda p: p <= sqrt, SieveOfEratosthenes())
    for p in primes:
        quotient, remainder = divmod(target, p)
        if remainder == 0:
            prime_factors = [p]
            prime_factors.extend(findFactors(quotient))
            r = reduce(operator.mul, prime_factors)
            assert r == target, (prime_factors, r, target)
            return sorted(prime_factors)
    return [target]


class SieveOfEratosthenes(object):
    CACHE = [2, 3, 5, 7]
    def __init__(self, max_value=None):
        self.i = -1
        self.primes = self.CACHE
        self.compositegenerators = [CompositeGenerator(p) for p in self.primes]
        self.wheel = WheelIncrementer()
        self.max_value = max_value
        
    def __iter__(self):
        return self
    
    def next(self):
        self.i += 1
        if self.i < len(self.primes):
            return self.primes[self.i]
        while True:
            found = True
            candidate = self.wheel.next()
            if self.max_value and candidate > self.max_value:
                raise StopIteration
            if candidate < self.primes[-1]:
                continue
            while self.compositegenerators[0].value <= candidate:
                cg = heapq.heappop(self.compositegenerators)
                if cg.value == candidate:
                    found = False
                cg.update(candidate)
                heapq.heappush(self.compositegenerators, cg)
            if found:
                heapq.heappush(self.compositegenerators, CompositeGenerator(candidate))
                SieveOfEratosthenes.CACHE.append(candidate)
                return candidate


class WheelIncrementer(object):
    def __init__(self):
        # source: http://www.cs.hmc.edu/~oneill/papers/Sieve-JFP.pdf - for 2, 3, 5, 7
        self.start = 11
        self.increments = itertools.cycle([
            2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2, 4,
            8, 6, 4, 6, 2, 4, 6, 2, 6, 6, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 10, 2, 10
        ])
        
    def __iter__(self):
        return self
    
    def next(self):
        value = self.start
        self.start += next(self.increments)
        return value


class CompositeGenerator(object):
    def __init__(self, base, max_p=None):
        self.base = base
        self.value = base * base
        
    def update(self, above=None):
        self.value += self.base
        if above:
            while self.value < above:
                self.value += self.base
        
    def __cmp__(self, other):
        return cmp(self.value, other.value)

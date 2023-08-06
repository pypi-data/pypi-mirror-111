from __future__ import annotations
from typing import Iterable, Iterator, TypeVar, Generic, Callable, List, List, Dict, Optional, Any

T = TypeVar('T')
A = TypeVar('A')
K = TypeVar('K')

class IterPiper(Generic[T]):
    def __init__(self, wrapped: Iterable[T]) -> None:
        self.wrapped = wrapped

    def runIt(self) -> Iterable[T]:
        return self.wrapped

    def run(self) -> List[T]:
        return list(self.wrapped)

    def filter(self, predicate: Callable[[T], bool]) -> IterPiper[T]:
        return IterPiper((x for x in self.wrapped if predicate(x)))

    def map(self, f: Callable[[T], A]) -> IterPiper[A]:
        return IterPiper((f(x) for x in self.wrapped))

    def flatMap(self, f: Callable[[T], IterPiper[A]]) -> IterPiper[A]:
        return IterPiper((y for x in self.wrapped for y in f(x)))

    def flatten(self):
        return self.flatMap(lambda x: x)

    def sorted(self, by=lambda x: x, ascending=True) -> IterPiper[T]:
        res = self.run()
        res.sort(key=by, reverse=(not ascending))
        return IterPiper(res)

    def group(self, agg: Callable[[List[T]], A], by:Callable[[T], K]) -> IterPiper[A]:
        d: Dict[K, List[T]] = {}
        for el in self.wrapped:
            key = by(el)
            d[key] = d.get(key, [])
            d[key].append(el)

        return IterPiper([agg(vs) for vs in d.values()])

    def fold(self, initial: A, combine: Callable[[A, T], A]) -> A:
        res = initial
        for el in self.runIt():
            res = combine(res, el)
        return res

    def reduce(self, combine: Callable[[T, T], T]) -> Optional[T]:
        l = self.run()
        if len(l) == 0:
            return None
        elif len(l) == 1:
            return l[0]
        else:
            res = l[0]
            for el in l[1:]:
                res = combine(res, el)
            return res

    def headOpt(self) -> OptPiper[T]:
        m = self.run() # todo: a lazy solution is much preferable
        if len(m) > 0:
            return OptPiper(m[0])
        else:
            return OptPiper(None)

    def concat(self, other: IterPiper[T]) -> IterPiper[T]:
        m = self.run() # todo: a lazy solution is much preferable
        o = other.run()
        return IterPiper(m + o)

    def __iter__(self) -> Iterator[T]:
        return self.wrapped.__iter__()


class OptPiperIterator(Iterator[T]):
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __next__(self):
        cur = self.wrapped
        if cur is None:
            raise StopIteration
        else:
            self.wrapped = None
            return cur


class OptPiper(Generic[T]):
    def __init__(self, wrapped: Optional[T]) -> None:
        self.wrapped = wrapped

    def run(self) -> Optional[T]:
        return self.wrapped

    def isNone(self) -> bool:
        return self.wrapped is None

    def __iter__(self) -> Iterator[T]:
        return OptPiperIterator(self.wrapped)

    def filter(self, predicate: Callable[[T], bool]) -> OptPiper[T]:
        if self.wrapped is None:
            return self
        elif predicate(self.wrapped):
            return self
        else:
            return OptPiper(None)

    def map(self, f: Callable[[T], A]) -> OptPiper[A]:
        if self.wrapped is None:
            return OptPiper(None)
        else:
            return OptPiper(f(self.wrapped))

    def flatMap(self, f: Callable[[T], OptPiper[A]]) -> OptPiper[A]:
        if self.wrapped is None:
            return OptPiper(None)
        else:
            return f(self.wrapped)

    def flatMapOpt(self, f: Callable[[T], Optional[A]]) -> OptPiper[A]:
        return self.flatMap(lambda x: pipeOpt(f(x)))

    def getOrElseF(self, defaultF: Callable[[], T]) -> T:
        if self.wrapped is None:
            return defaultF()
        else:
            return self.wrapped

    def getOrElse(self, default: T) -> T:
        return self.getOrElseF(lambda: default)

def pipe(wrapped: Iterable[T]) -> IterPiper[T]:
    return IterPiper(wrapped)

def pipeOpt(wrapped: Optional[T]) -> OptPiper[T]:
    return OptPiper(wrapped)

def mustRaise(_: Any) -> Any:
    return None


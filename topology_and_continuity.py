from functions_and_set_theory import *
from itertools import combinations
from typing import Callable, Any, Set

"""Requires other file functions_and_set_theory.py"""


class TopologicalSpace:
    """A topology on some set. Must satisfy the three requirements for a topology.

    Since we are working with finite sets only, will just mandate closure under finite union and
    finite intersection, instead of closure under arbitrary union and finite intersection
    like usual."""

    def __init__(self, X: frozenset[Any], open_sets: Set[frozenset[Any]]):
        if not is_topology(X, open_sets):
            raise ValueError("The open sets do not form a topology on your underlying set.")
        else:
            self.underlying_set = X
            self.topology = open_sets

    def __eq__(self, X: TopologicalSpace):
        return self.underlying_set == X.underlying_set and self.topology == X.topology

class DiscreteTopology(TopologicalSpace):
    """Takes a set and endows it with the discrete topology."""
    def __init__(self, X: frozenset[Any]):
        open_sets = powerset(X)
        TopologicalSpace.__init__(self, X, open_sets)

class IndiscreteTopology(TopologicalSpace):
    """Takes a set and endows it with the indiscrete topology."""
    def __init__(self, X: frozenset[Any]):
        open_sets = {frozenset(), X}
        TopologicalSpace.__init__(self, X, open_sets)

def is_topology(X: frozenset[Any], open_sets: Set[frozenset[Any]]) -> bool:
    """Return true if open_sets defines a topology on X."""
    empty = frozenset()

    """Make sure the """
    if X not in open_sets or empty not in open_sets:
        return False

    """Check closure under unions and intersections (Pairwise is sufficient for finite
    topologies)"""

    for A in open_sets:
        for B in open_sets:
            if union(A, B) not in open_sets or intersection(A, B) not in open_sets:
                return False

    return True

"""Functions between topological spaces"""

class TopologicalFunction(Function):
    """A function between two topological spaces, instead of just sets.

    Attributes:
        domain (TopologicalSpace): Domain of the function, with a topology.
        codomain (TopologicalSpace): Codomain of the function, with a topology. Required this
        time, unlike a function between sets.
        rule (Callable[[Any], Any]): Rule that the function follows, as a function
        from the underlying set of domain to the underlying set of codomain.

    Hidden Attributes:
        _underlying_function (Function): A function of the underlying sets.
    """

    def __init__(self, rule: Callable[[Any], Any], domain: TopologicalSpace,
        codomain: TopologicalSpace):

        self.domain = domain
        self.codomain = codomain
        self.rule = rule

        underlying_domain = domain.underlying_set
        underlying_codomain = codomain.underlying_set

        f = Function(rule, underlying_domain, underlying_codomain)

        self._underlying_function = f

    def __call__(self, x: Any) -> Any:
        f = self._underlying_function

        return f(x)

    def __eq__(self, g: TopologicalFunction):
        F = self._underlying_function
        G = g._underlying_function

        return self.domain == g.domain and self.codomain == g.codomain and F == G

    def is_injective(self) -> bool:
        f = self._underlying_function

        return f.is_injective()

    def is_surjective(self) -> bool:
        f = self._underlying_function

        return f.is_surjective()

    def is_bijective(self) -> bool:
        return self.is_injective() and self.is_surjective()

    def image(self) -> Set[Any]:
        f = self._underlying_function

        return f.image()

    def preimage(self, A: frozenset[Any]) -> Set[Any]:
        f = self._underlying_function

        return f.preimage(A)

    def graph(self) -> Set[Any]:
        f = self._underlying_function

        return f.graph()

    def is_continuous(self) -> bool:
        """The only new helper for TopologicalFunctions, returns if the function
        is continuous based on the topological definition of continuity."""
        for open_set in self.codomain.topology:
            if frozenset(self.preimage(open_set)) not in self.domain.topology:
                return False

        return True

    def is_homeomorphism(self) -> bool:
        """Returns whether or not the function is a homeomorphism (continuous, bijective
        with continuous inverse)"""

        if not self.is_continuous():
            return False
        elif not self.is_bijective():
            return False
        else:
            f = self._underlying_function
            for open_set in self.domain.topology: # Check f is an open mapping (homeomorphisms are
                   # continuous bijective open mappings)
                new = set()

                for x in open_set:
                    new.add(f(x))

                if frozenset(new) not in self.codomain.topology:
                    return False

            return True


"""Miscellaneous"""

def powerset(X: frozenset[Any]) -> Set[frozenset[Any]]:
    """Returns the power set P(X) of X."""
    s = list(X)
    result = []

    for r in range(len(s) + 1):
        for combo in combinations(s, r):
            result.append(frozenset(combo))

    return set(result)


if __name__ == "__main__":
    def rule(a: int) -> int:
        return 3 * a

    A = {0, 1, 2}
    open_sets = {frozenset({}), frozenset({0}), frozenset(A)}

    print(powerset(A))

from typing import Callable, Set, Any

"""Functions"""

class Function:
    """A function f: A -> B, with domain A and codomain B.

    Attributes:
        domain (Set[Any]): Domain of the function
        codomain (Set[Any]): Codomain of the function. If not specified, use image
        of the function as codomain (automatically surjective).
        rule (Callable[[Any],Any]: A PYTHON function taking elements of domain to elements in
        codomain, which will act as the rule for the mathematical function.
    """

    def __init__(self, rule: Callable[[Any], Any], domain: Set[Any],
                 codomain: Set[Any] | None = None):

        self.rule = rule

        self.domain = domain

        image = self.image()

        if codomain is None:
            self.codomain = image
        elif not image <= codomain:
            raise ValueError("Function maps outside of codomain.")
        else:
            self.codomain = codomain

    def __call__(self, x: Any) -> Any:
        if x not in self.domain:
            raise ValueError("Value not in function domain.")
        else:
            return self.rule(x)

    def __eq__(self, f: Any) -> Any:
        if not isinstance(f, Function):
            return False

        return f.domain == self.domain and f.codomain == self.codomain and f.graph() == self.graph()

    def is_injective(self) -> bool:
        """Returns True if the function is injective, False otherwise."""
        return len(self.image()) == len(self.domain)

    def is_surjective(self) -> bool:
        """Returns True if the function is surjective, False otherwise."""
        return self.image() == self.codomain

    def is_bijective(self) -> bool:
        """Returns True if the function is bijective, False otherwise."""
        return self.is_injective() and self.is_surjective()

    def image(self) -> Set[Any]:
        image = set()

        for x in self.domain:
            try:
                image.add(self.rule(x))
            except Exception as e:
                raise ValueError("Rule is not defined on domain.")

        return image

    def preimage(self, A: Set[Any]) -> Set[Any]:
        """Returns the preimage of a function given a set in the codomain. Raise ValueError
        if A is not contained in the function's codomain."""
        preimage = set()

        if not A <= self.codomain:
            raise ValueError("Set is not contained in function codomain.")

        for x in self.domain:
            if self.rule(x) in A:
                preimage.add(x)

        return preimage

    def graph(self) -> Set[tuple[Any, Any]]:
        graph = set()
        for x in self.domain:
            graph.add((x, self.rule(x)))

        return graph

class Identity(Function):
    """Identity mapping on any set."""

    def __init__(self, domain: Set[Any]):
        def identity(x: Any) -> Any:
            return x

        Function.__init__(self, identity, domain)

"""External PYTHON functions, that act on Function objects"""

def inverse(f: Function) -> Function:
    """Return a function that is the inverse of f. Raise an error if f is not bijective."""

    if not f.is_bijective():
        raise ValueError("Function is not bijective.")

    def inverse_rule(y: Any) -> Any:
        preimage = f.preimage({y}) # Should only contain one element as f is bijective
        x = next(iter(preimage))

        return x

    g = Function(inverse_rule, f.codomain, f.domain)
    return g

def composition(f: Function, g: Function) -> Function:
    """Returns the function f composed g, if the operation is valid (g's codomain must be
    contained in f's domain)"""

    if not g.codomain <= f.domain:
        raise ValueError("Composition not valid.")

    def rule(x: Any) -> Any:
        return f(g(x))

    h = Function(rule, g.domain, f.codomain)
    return h

def restriction(f: Function, A: Set[Any]) -> Function:
    """Return the restriction of f on A. A must be a subset of f's domain."""
    if not A <= f.domain:
        raise ValueError("A is not a subset of f's domain.")

    g = Function(f.rule, A)
    return g

"""Set Theory"""

def cartesian_product(A: Set[Any], B: Set[Any]) -> Set[tuple[Any,Any]]:
    """Returns the Cartesian product of A and B, A x B."""

    AxB = set()

    for a in A:
        for b in B:
            AxB.add((a,b))

    return AxB

def intersection(A: Set[Any], B: Set[Any]) -> Set[Any]:
    """Returns the intersections of sets A and B."""

    AandB = set()

    for a in A:
        if a in B:
            AandB.add(a)

    return AandB

def union(A: Set[Any], B: Set[Any]) -> Set[Any]:
    """Returns the union of A and B."""

    return A.union(B)

if __name__ == "__main__":
    A = {1,2,3,4,5,6}
    B = {1,2,3, 12}

    print(union(A, B))
    print(A)

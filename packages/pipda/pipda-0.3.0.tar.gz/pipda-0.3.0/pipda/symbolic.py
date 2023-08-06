"""Provides Symbolic and Reference classes"""
from abc import ABC, abstractmethod
from typing import ClassVar, Optional, Any

import varname.helpers

from .utils import Expression, evaluate_expr
from .context import ContextBase, ContextError
from .function import Function

class Reference(Expression, ABC):
    """The Reference class, used to define how it should be evaluated
    according to the context for references, for example, `f.A`, `f['A']` or
    the references of them (i.e. `f.A.B`, `f.A['b']`, etc)

    Args:
        parent: The parent of this reference. For example: `f.A` for `f.A.B`
        ref: The reference. For example: `B` for `f.A.B`
        context: Defaults to `None`, which should not be specified while
            instansiation. Because these types of expressions are independent.
            A context should be passed to `evaluate` to evaluate the expression.
    """
    def __init__(self,
                 parent: Any,
                 ref: Any) -> None:

        self.parent = parent
        self.ref = ref

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'parent={self.parent!r}, ref={self.ref!r})'
        )

    def __call__(self, *args, **kwargs):
        """Allow `f.a.b` to be a function, so that one can do `f.a.b(1)`"""
        return Function(self, args, kwargs, False)

    @abstractmethod
    def _pipda_eval(
            self,
            data: Any,
            context: Optional[ContextBase] = None
    ) -> Any:
        """Evaluate the reference according to the context"""
        if context is None:
            # needs context to be evaluated
            raise ContextError(
                f"Cannot evaluate {repr(self)} "
                "object without a context."
            )


class ReferenceAttr(Reference):
    """Attribute references, for example: `f.A`, `f.A.B` etc."""
    # Whether it's a direct reference
    direct: ClassVar[bool] = False

    def _pipda_eval(
            self,
            data: Any,
            context: Optional[ContextBase] = None
    ) -> Any:
        """Evaluate the attribute references"""
        # if we don't have a context here, assuming that
        # we are calling `f.a.b(1)`, instead of evaluation
        super()._pipda_eval(data, context)
        parent = evaluate_expr(self.parent, data, context)

        return context.getattr(parent, self.ref, self.__class__.direct)

class ReferenceItem(Reference):
    """Subscript references, for example: `f['A']`, `f.A['B']` etc"""
    direct: ClassVar[bool] = False

    def _pipda_eval(
            self,
            data: Any,
            context: Optional[ContextBase] = None
    ) -> Any:
        """Evaluate the subscript references"""
        super()._pipda_eval(data, context)
        parent = evaluate_expr(self.parent, data, context)
        ref = evaluate_expr(self.ref, data, context.ref)
        return context.getitem(parent, ref, self.__class__.direct)

class DirectRefAttr(ReferenceAttr):
    """The direct attribute reference, such as `f.A`"""
    direct: ClassVar[bool] = True

class DirectRefItem(ReferenceItem):
    """The direct attribute reference, such as `f['A']`"""
    direct: ClassVar[bool] = True

@varname.helpers.register
class Symbolic(Expression):
    """The symbolic class, works as a proxy to represent the data

    In most cases it is used to construct the Reference objects.
    """
    def __getattr__(self, name: str) -> Any:
        """Create a DirectRefAttr object"""
        return DirectRefAttr(self, name)

    def __getitem__(self, item: Any) -> Any:
        """Create a DirectRefItem object"""
        return DirectRefItem(self, item)

    def __repr__(self) -> str:
        return f"<Symbolic:{self.__varname__}>"

    def _pipda_eval(
            self,
            data: Any,
            context: Optional[ContextBase] = None
    ) -> Any:
        """When evaluated, this should just return the data directly"""
        return data

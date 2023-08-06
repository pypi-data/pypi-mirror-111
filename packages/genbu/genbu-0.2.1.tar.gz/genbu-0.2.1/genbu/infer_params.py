"""Infer Genbu Params from function signature."""

import inspect
import typing as t

from . import combinators as comb
from .params import Param
from .infer import infer_parser


class UnsupportedCallback(ValueError):
    """Unsupported Genbu callback (e.g. no signature)."""
    def __init__(self, callback: t.Any):
        super().__init__(callback)
        self.callback = callback


def infer_parser_from_parameter(parameter: inspect.Parameter) -> comb.Parser:
    """Infer parser from signature.

    Handles var arguments and unannotated parameters.
    Throws UnsupportedType.
    """
    hint: t.Any = str
    if parameter.annotation is not parameter.empty:
        hint = parameter.annotation
    if parameter.kind == parameter.VAR_POSITIONAL:
        hint = t.Tuple[hint, ...]
    elif parameter.kind == parameter.VAR_KEYWORD:
        hint = t.Dict[str, hint]
    return infer_parser(hint)


def infer_params_from_signature(function: t.Callable[..., t.Any],
                                ) -> t.List[Param]:
    """Infer Genbu Params from function signature.

    Creates named options by default.
    Throws UnsupportedCallback or UnsupportedType.
    """
    try:
        signature = inspect.signature(function)
    except (TypeError, ValueError) as exc:
        raise UnsupportedCallback(function) from exc

    return [
        Param(
            dest=p.name,
            optargs=[f"--{p.name}"],
            parser=infer_parser_from_parameter(p),
        )
        for p in signature.parameters.values()
    ]

from typing import Union, TypeVar, Type, Iterable, Tuple, Callable
from typing_extensions import ParamSpec as CallableParamSpec

T = TypeVar("T")
G = TypeVar("G")
P = CallableParamSpec("P")


def tuple_wrap(thing: Union[T, Iterable[T]], wrap_type: Type[T]) -> Tuple[T, ...]:
    if isinstance(thing, wrap_type):
        return (thing,)
    elif isinstance(thing, Iterable):
        return tuple(thing)
    else:
        raise Exception


def tuple_wrap_kwargs(*kwargs_to_wrap: str, wrap_type: Type):
    def kwarg_wrapper(func: Callable[P, G]) -> Callable[P, G]:
        def func_wrapper(*args: P.args, **kwargs: P.kwargs) -> G:
            to_wrap_kwargs = {
                key: value for key, value in kwargs.items() if key in kwargs_to_wrap
            }
            wrapped_kwargs = {
                key: tuple_wrap(value, wrap_type=wrap_type)
                for key, value in to_wrap_kwargs.items()
            }
            kwargs.update(wrapped_kwargs)
            return func(*args, **kwargs)

        return func_wrapper

    return kwarg_wrapper

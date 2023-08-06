from functools import wraps, partial
from types import FunctionType
from inspect import stack


def replace(with_):
    assert callable(with_), "You must specify a Callable to replace with."

    def wrapper(f):
        f._repl = with_
        return f
    return wrapper


def no_recursion(function_or_namespace=None):
    def replace(self, f):
        if hasattr(self, "_repl"):
            raise Exception("You can't set more that one replacement to a particular function")
        setattr(self, "_repl", f.__name__)
        return f

    if isinstance(function_or_namespace, FunctionType):
        @wraps(function_or_namespace)
        def wrapper(*args, **kwargs):
            f_name = stack()[1].function
            if f_name == getattr(function_or_namespace, "_repl", None):
                raise Exception("You can't call the original function from the replacement function")
            elif f_name != function_or_namespace.__name__:
                return function_or_namespace(*args, **kwargs)
            else:
                if hasattr(function_or_namespace, "_repl"):
                    if callable(function_or_namespace._repl):
                        return function_or_namespace._repl(*args, **kwargs)
                    return function_or_namespace.__globals__[function_or_namespace._repl](*args, **kwargs)  # noqa

                if hasattr(function_or_namespace.__globals__[f_name], "_nr_f"):
                    raise Exception(
                        "You must define another function *below* your decorated function, "
                        "*with the same name as the decorated function or decorated by `@function.replace` "
                        "where `function` is the current decorated function*, which will be used to replace "
                        "the recursion calls with."
                    )
                return function_or_namespace.__globals__[f_name](*args, **kwargs)
        wrapper._nr_f = True
        wrapper.replace = partial(replace, function_or_namespace)
        return wrapper
    elif isinstance(function_or_namespace, dict):
        def _wrapper(f):
            new_f = FunctionType(
                code=f.__code__,
                globals=function_or_namespace,
            )

            @wraps(f)
            def i_wrapper(*args, **kwargs):
                f_name = stack()[1].function
                callback = new_f
                if f_name != new_f.__name__:
                    if not function_or_namespace.get(new_f.__name__):
                        if not hasattr(f, "_repl"):
                            raise Exception(
                                "There is no function named '{}' in the provided namespace".format(new_f.__name__)
                            )
                    else:
                        assert callable(function_or_namespace[new_f.__name__]),\
                            "You must provide a Callable and not '{}'".format(
                                type(function_or_namespace[new_f.__name__]).__name__
                            )
                        if hasattr(f, "_repl"):
                            raise Exception(
                                "There is a collision! "
                                "you provided both a replacement function and a valid Callable in the namespace!"
                            )
                    if hasattr(f, "_repl"):
                        callback = f.__globals__[f._repl] if not callable(f._repl) else f._repl # noqa
                    return callback(*args, **kwargs)
                else:
                    raise Exception(
                        "The function '{0}' in the namespace you provided is the same as the current '{0}' function. "
                        "Which it leads to recursion. Try providing another namespace".format(f_name)
                    )
            i_wrapper._nr_f = True
            i_wrapper.replace = partial(replace, f)
            return i_wrapper
        return _wrapper
    else:
        raise ValueError("You must specify either a namespace")


__all__ = ["no_recursion", "replace"]

# Copyright (c) 2021 Avery
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import inspect
from typing import Callable, Coroutine

base_exceptions = (
    AssertionError,
    AttributeError,
    EOFError,
    FloatingPointError,
    GeneratorExit,
    ImportError,
    IndexError,
    KeyError,
    KeyboardInterrupt,
    MemoryError,
    NameError,
    NotImplementedError,
    OSError,
    OverflowError,
    ReferenceError,
    RuntimeError,
    StopIteration,
    SyntaxError,
    IndentationError,
    TabError,
    SystemError,
    SystemExit,
    TypeError,
    UnboundLocalError,
    UnicodeError,
    UnicodeEncodeError,
    UnicodeDecodeError,
    UnicodeTranslateError,
    ValueError,
    ZeroDivisionError,
)

def tri(func: Callable):
    """
    Provides a wrapper around the function given that allows it to take the
    same arguments, but will return a tuple of `(error, result)` instead of
    throwing any errors. If there is no error, `error` will be `None`.

    This intentionally does not handle native exceptions. For that, use `bi`.

    Parameters
    ----------
    func : Callable
        The function to wrap
    """
    def _wrapper(*args, **kwargs):
        try:
            return None, func(*args, **kwargs)
        except BaseException as err:
            if isinstance(err, base_exceptions):
                raise err
            # If it is a built-in exception, don't override
            return err, None
    
    return _wrapper


async def atri(func: Coroutine):
    """
    Similar to :func:`tri`, but instead takes coroutines or awaitable
    functions and awaits them, providing the same return. Unlike
    `tri`, you do not need to wrap the function and then call the result,
    you can just give the coroutine directly. For example:

    ```python
    error, result = atri(my_coroutine(param1, param2))
    error, result = atri(my_coroutine_without_params)
    ```

    This intentionally does not handle native exceptions. For that, use `abi`.

    Parameters
    ----------
    func : Coroutine
        The function to raise

    Returns
    -------
    (Exception, Any)
        The error-result tuple

    Raises
    ------
    TypeError
        If the function is not a coroutine function or awaitable
    BaseException
        Any built in exception
    """
    if inspect.iscoroutinefunction(func):
        func = func()
    else:
        # It may not be an async function but it is awaitable
        if not inspect.isawaitable(func):
            raise TypeError("Function must be coroutine")

        # It's an async function, but not yet started
        func = func()
    
    try:
        return None, await func
    except BaseException as err:
        # If it is a built-in exception, don't override
        if isinstance(err, base_exceptions):
            raise err
        return err, None

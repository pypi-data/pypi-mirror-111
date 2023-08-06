# Copyright (c) 2021 Avery
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import Callable, Coroutine
from .tri import atri

def bi(func: Callable):
    """
    Provides a wrapper around the function given that allows it to take the
    same arguments, but will return a tuple of `(error, result)` instead of
    throwing any errors. If there is no error, `error` will be `None`.

    This handles native exceptions. If this is not what you want, use `tri`.

    Parameters
    ----------
    func : Callable
        The function to wrap
    """
    def _wrapper(*args, **kwargs):
        try:
            return None, func(*args, **kwargs)
        except BaseException as err:
            return err, None
    
    return _wrapper


async def abi(func: Coroutine):
    """
    Similar to :func:`tri`, but instead takes coroutines or awaitable
    functions and awaits them, providing the same return. Unlike
    `tri`, you do not need to wrap the function and then call the result,
    you can just give the coroutine directly. For example:

    ```python
    error, result = atri(my_coroutine(param1, param2))
    error, result = atri(my_coroutine_without_params)
    ```

    This handles `BaseException`s. For that, use `abi`.

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
    try:
        return await atri(func)
    except BaseException as err:
        return err, None

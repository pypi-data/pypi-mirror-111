# Tri/bi
This package provides wrappers around functions that nicely handle errors. Reducing code clutter and allowing better responses to uses. This package is inspired by [tri-fp](https://www.npmjs.com/package/tri-fp)

[![](https://img.shields.io/pypi/v/tribi.svg)](https://pypi.org/project/tribi/)
[![](https://img.shields.io/pypi/implementation/tribi.svg)](https://pypi.org/project/tribi/)

## Tri
Tri still lets native exceptions (usually more severe errors) throw, but catches any other errors
```python
>>> from tri import tri, bi
>>> def my_function():
...    return 1 / 0 # Zero division error!

>>> # This function raises a "native" exception
>>> tri(my_function)()
Traceback (most recent call last):
   ...
ZeroDivisionError: division by zero

>>> def my_other_function():
...    raise Exception

>>> # This only raises a standard exception, so doesn't fail
>>> tri(my_other_function)()
(Exception(), None)
```


### Bi
Bi, on the contrary, handles all errors blindly. This should only be used if you know what you're doing.
```python
>>> bi(my_function)()
(ZeroDivisionError('division by zero'), None)
```


## Async
Both `tri` and `bi` support async.

### Tri
```python
>>> # Assuming running in async
>>> from tri import atri, abi
>>> async def divide(a, b):
...     return a / b

>>> # Let's try to divide by zero
>>> await atri(divide(1, 0))
Traceback (most recent call last):
   ...
ZeroDivisionError: division by zero

>>> # And with abi?
>>> await abi(divide(1, 0))
(ZeroDivisionError('division by zero'), None)

>>> # If the function takes no params, we can just pass the function name
>>> async def func():
...     return "hello"

>>> await atri(func)
(None, "hello")
```


## Real life example
Some examples include...

### Safer JSON loading
```python
from tri import bi

safer_loads = bi(json.loads)
error, result = safer_loads(data)

if error:
   # Error handling JSON
   print("Invalid JSON")
```

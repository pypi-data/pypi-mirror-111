### This module helps you to get rid of recursions when you want to rename a builtin function, or a function that already exists.


usage:
```python
from no_recursion import no_recursion, replace

@no_recursion
@replace(bin)
def bin(n: int):
    return bin(n)
```
> The decorator `replace` must be **below** `no_recursion`. 


it will replace each recursive call to `bin` with a call to the "original" `bin`.

You can also set a namespace where it will try to find the original function in,
>the original function must be named the same as the decorated function.

You can specify a particular namespace in `@no_recursion`.
```python
from no_recursion import no_recursion, replace

@no_recursion(vars(__builtins__))
def bin(n: int):
    return bin(n)
```
In this example, it will take the builtin `bin`.

The namespace must be a dict that contains the function.

You can also use `decorated_f.replace` (not the global `replace` function) to set a replacement function.

```python
import builtins
from no_recursion import no_recursion, replace


@no_recursion
def bin(n: int):
    return bin(n)


@bin.replace
def replace_bin(n: int):
    return builtins.bin(n)
```

All examples above will produce the same result.
```python
print(bin(12))
# 0b1100
```

NOTES:
> when you call `no_recursion` with parentheses, you must specify a namespace (`@no_recursion({})`. Otherwise just do `@no_recursion`.
> Exception can be raised.
 
> The decorator `replace` must be **below** `no_recursion`. 

> In the namespace dictionary, the original function must be named the same as the decorated function.

# Decorators to log function calls with parameter and timing

Decorators to track down function call with indent.
Both logging function and indent characters are configurable
**Decorate a function**:

```
@log_call()
def method1(arg1, arg2):
    return arg1 + arg2
method1(3, 4)
```

Output:

```
...CALL: method1(3, 4)
...'method1' RETURN: 7
...'method1' FINISHED in 0.000003 secs
```

**Customize indent characters**:

```
@log_call(indent='\_\_\_')
def method1(arg1, arg2):
return arg1 + arg2
method1(3, 4)

```

Output:

```

**_CALL: method1(3, 4)
_**'method1' RETURN: 7
\_\_\_'method1' FINISHED in 0.000006 sec

```

```

```

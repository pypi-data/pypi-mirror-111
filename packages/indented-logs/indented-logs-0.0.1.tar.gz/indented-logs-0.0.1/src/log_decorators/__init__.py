import time

indent_arr = []


def log_call(logger_func=print, indent="...", param_max_length=1000, log_time=True):
    def inner(func):
        def wrapper(*args, **kwargs):
            indent_arr.append(indent)
            indent_str = "".join(indent_arr)

            logger_func("")
            logger_func(
                f"{indent_str}CALL: {func.__name__}({get_all_args_str(args, kwargs)})"
            )

            start_time = time.perf_counter()

            result = func(*args, *kwargs)

            end_time = time.perf_counter()
            run_time = end_time - start_time  # 3

            logger_func(
                f"{indent_str}{func.__name__!r} RETURN: {repr_with_length(result, param_max_length)}"
            )
            if log_time:
                logger_func(
                    f"{indent_str}{func.__name__!r} FINISHED in {run_time:.6f} secs"
                )
            logger_func("")
            indent_arr.pop()
            return result

        def get_all_args_str(args, kwargs):
            args_str = ", ".join(
                map(lambda a: repr_with_length(a, param_max_length), args)
            )

            kwargs_str = ""
            if kwargs:
                kwargs_str = ", " + ", ".join(
                    map(
                        lambda k: f"{k}={repr_with_length(kwargs[k], param_max_length)}",
                        kwargs,
                    )
                )

            return f"{args_str}{kwargs_str}"

        return wrapper

    return inner


def repr_with_length(arg, length):
    return str(arg)[:length] if length else arg


def log_call_cls(logger_func=print, indent="...", param_max_length=50):
    def inner(func):
        return _log_call_cls(
            cls=func,
            logger_func=logger_func,
            indent=indent,
            param_max_length=param_max_length,
        )

    return inner


class _log_call_cls:
    """Decorator that decorate log_call to class methods"""

    def __init__(
        self, cls, logger_func=print, indent="...", param_max_length=50, log_time=True
    ):
        self.cls = cls
        self.logger_func = logger_func
        self.indent = indent
        self.param_max_length = param_max_length
        self.log_time = log_time

    def __call__(self, *args, **kwargs):
        obj = self.cls(*args, **kwargs)
        for func_name in dir(obj):
            func = getattr(obj, func_name)
            if not func_name.startswith("__") and callable(func):
                wrapper_func = log_call(
                    logger_func=self.logger_func,
                    indent=self.indent,
                    param_max_length=self.param_max_length,
                    log_time=self.log_time,
                )
                setattr(obj, func_name, wrapper_func(func))
        return obj

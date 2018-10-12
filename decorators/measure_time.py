import time


def measure_time(func):
    def internal_func(*args, **kwargs):
        before_time = time.time()
        func(*args, **kwargs)
        after_time = time.time() - before_time
        print(f"{after_time:.2f}")
        return func
    return internal_func


@measure_time
def do_something(count):
    for i in range(count):
        c = 5 + 5


do_something(100000000)

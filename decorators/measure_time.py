import functools
import time
import timeit


def measure_time(func):
    def internal_func(*args, **kwargs):
        before_time = time.time()
        func(*args, **kwargs)
        after_time = time.time() - before_time
        print("{0:.2f}".format(after_time))
        return func
    return internal_func


@measure_time
def do_something(count):
    for i in range(count):
        c = 5 + 5


do_something(100000000)


def decorator_with_arguments(number):
    def my_decorator(func):
        def internal_func(*args, **kwargs):
            print("In the decorator!")
            if number == 13:
                print("Not running the function!")
            else:
                tic = timeit.default_timer()
                func(*args, **kwargs)
                toc = timeit.default_timer() - tic
                print('Total time for func is:', round(toc, 8))
            print("After the decorator!")
        return internal_func
    return my_decorator


@decorator_with_arguments(111)
def my_function(x, y):
    print(x+y)


my_function(50, 50)

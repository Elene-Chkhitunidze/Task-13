##Task 1
import time

def decorator(func):
    def wrapper(x):
        if x<0:
            raise ValueError ("Please enter a positive number")
        else:

            return func(x)
    return wrapper


@decorator
def number (x):
    return x

try:
    print(number(7))
except Exception as e:
    print(e)

##Task 2

class CheckNumber:
    def __call__(self, func):
        def wrapper (x):
            if x<0:
                raise ValueError ("Please enter a positive number")
            else:
                return func(x)
        return wrapper

decorator = CheckNumber()

@decorator
def num (x):
    return x

try:
    print(num(-5))
except Exception as e:
    print(e)


##Task 3

def time_dec(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        result_time = end_time - start_time
        return result_time
    return wrapper


@time_dec
def time_func (x):
    return time.sleep(x)


print (time_func(5))

##Task 4

class LoggingMeta(type):
    def __new__(cls, name, bases, methods):

        new_class = super().__new__(cls, name, bases, methods)

        method_list = [i for i in methods if callable(methods[i]) and not i.startswith("__")]
        print(f"Class '{name}' methods: {method_list}")
        return new_class


class Class_1(metaclass=LoggingMeta):
    def method_1(self):
        pass

    def method_2(self):
        pass


class Class_2(metaclass=LoggingMeta):
    def method_1(self):
        pass
import random
import string


def get_random_value(numbers=False, length=5):
    if not numbers:
        return "".join([random.choice(string.ascii_letters) for i in range(length)])
    else:
        return int("".join([random.choice(string.digits) for i in range(length)]))

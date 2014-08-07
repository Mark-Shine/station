from queue import Queue 
from functools import wraps
import time
def add(a,b):
    print ("-begin111")
    time.sleep(1)
    print ("-end")
    return a+b

class Async:
    def __init__(self, func, args):
        self.func = func 
        self.args = args

def later(gen, result_queue):
    def wrapped(result):
        print ("in wrapped")
        a = gen.send(result)
        print ("and after")
        result_queue.put((result, a))
    return wrapped


def inlined_async(func): 

    @wraps(func)
    def wrapper(*args): 
        f = func(*args)
        result_queue = Queue() 
        result_queue.put(None) 
        while True:
            result = result_queue.get() 
            try:
                apply_async(f.send, result, callback=later(f, result_queue)) 
            except StopIteration:
                break 
    return wrapper

@inlined_async
def test():
    for n in range(10):
        r = yield Async(add, (n, n))
        print(r)

        print ("begin")
        time.sleep(3)   
        print ("end")

    print('Goodbye')


if __name__ == '__main__':
    import multiprocessing
    pool = multiprocessing.Pool()
    apply_async = pool.apply_async
# Run the test function
    test()

# coding:utf-8
import time
import thread

gen = None


def long_io():
    def fun():
        global gen
        print('io')
        cnt = 0
        while cnt < 5:
            time.sleep(1)
            cnt += 1
            print('.')
        print('io finish')
        ret = 'io ret'

        try:
            gen.send(ret)
        except Exception as e:
            print e

    thread.start_new_thread(fun)


def gen_coroutine(fun):
    def wrapper(*arg, **kargs):
        global gen
        gen = fun()
        gen.next()
    return wrapper


@gen_coroutine
def req_a():
    print('处理请求a')
    ret = yield long_io()
    print('请求a exit')


def req_b():
    print('处理b')
    cnt = 0
    while cnt < 2:
        time.sleep(1)
        cnt += 1
        print('x')

    print('处理b finish')


def main():
    req_a()
    req_b()
    while True:
        pass

if __name__ == '__main__':
    main()

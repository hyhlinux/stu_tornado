# coding:utf-8
import time
import thread


def long_io():
    print('io')
    cnt = 0
    while cnt < 5:
        time.sleep(1)
        cnt += 1
        print('.')
    print('io finish')
    ret = 'io ret'
    yield ret

# gen_coroutine
#   直接和epoll练习.
#
#


def gen_coroutine(fun):
    def wrapper(*arg, **kargs):
        gen = fun()
        gen_long_io = gen.next()

        def fun(g):
            ret = g.next()
            try:
                g.send(ret)  # ret --> io ret
            except Exception as e:
                print e
        # 延时操作， 仍给了新线程.
        thread.start_new_thread(fun, (gen_long_io,))

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

# coding:utf-8
import time
import thread


def long_io(callback):
    def fun(callback):
        print('io')
        cnt = 0
        while cnt < 5:
            time.sleep(1)
            cnt += 1
            print('.')
        print('io finish')
        ret = 'io ret'
        # return ret
        callback(ret)

    thread.start_new_thread(fun, (callback,))


def on_finish(ret):
    print ret
    print('on_finish bg')


def req_a():
    print('处理请求a')
    ret = long_io(on_finish)
    # 拆分req_a
    # 1.当处理Io时，主线程返回.
    # 2.需要处理io的部分，作为回调.
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
        time.sleep(1)
        print('m')

if __name__ == '__main__':
    main()

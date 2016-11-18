# coding:utf-8
from datetime import datetime
import sys


def get_head_info():
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
        file_name = f.f_code.co_filename
        file_now = str(datetime.now())
        file_lineno = str(f.f_lineno)
        file_co_name = f.f_code.co_name
        return '{} mod:{} func:{} line:{} '.format(file_now, file_name, file_co_name, file_lineno)


def main():
    print get_head_info()

if __name__ == '__main__':
    main()

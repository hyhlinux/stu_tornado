# coding:utf-8

with open('t.txt', 'wb') as f:
    f.write('xxx\naa')

print('writ ok')

with open('t.txt', 'rb') as f:
    print(f.read())

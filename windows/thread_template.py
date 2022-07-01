# 동시에 두가지 태스크
from threading import Thread
import time


class publisher(Thread):
    def __init__(self):
        Thread.__init__(self)
        print('publisher 스레드 시작')

    def run(self):
        i = 0
        while True:
            print(f'{i} published')
            i += 1
            time.sleep(0.1)


if __name__ == '__main__':
    thPub = publisher()
    thPub.start()

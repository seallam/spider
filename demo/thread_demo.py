import threading
from multiprocessing import Process
import time


def loop(num):
	for i in range(0, 20):
		print("当前线程:%s,输出:%s" % (num, i))
		time.sleep(2)


if __name__ == '__main__':
	thread_1 = Process(target=loop(1), name='thread_1')
	thread_2 = Process(target=loop(2), name='thread_2')
	thread_1.start()
	thread_2.start()
	thread_1.join()
	thread_2.join()


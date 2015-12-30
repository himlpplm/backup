#-*- coding:utf-8 -*-
import thread
import time

global event
event = {}

#����event
def signal(sign, *args, **kwargs):
	global event
	for func in event.get(sign, []):
		if hasattr(func, '__call__'):
			func(*args, **kwargs)

#event��Ӧ
def connect(sign, func):
	global event
	event.setdefault(sign, [])
	event[sign].append(func)


def achieve_timer(func, interval, *args):
	while 1:
		func(*args)
		time.sleep(interval)
	thread.exit_thread()

#��ʱ��
def timer(func, args, interval):
	thread.start_new_thread(achieve_timer, (func, interval) + args)
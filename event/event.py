#-*- coding:utf-8 -*-

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

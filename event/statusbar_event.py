#-*- coding:utf-8 -*-
from event import connect


#���·�ʽ
#��ʱˢ�� ���ݽ�����Ϣ
#������ֹ ����״̬��Ϣ

global num
num = 1

def statusbar_1(*args, **kwargs):
	self = args[0]
	self.children[-1].text = str(num)
connect('statusbar_timer_event', statusbar_1)

def statusbar_2(*args, **kwargs):
	self = args[0]
	self.children[-2].text = str(num * 2)
connect('statusbar_timer_event', statusbar_2)

def statusbar_num(*args, **kwargs):
	global num
	num += 1
connect('statusbar_timer_event', statusbar_num)

def statusbar_3(*args, **kwargs):
	pass

def statusbar_4(*args, **kwargs):
	pass


def statusbar_init(*args, **kwargs):
	w = [180, 180, 60, 40]
	self = args[0]
	self.insert(width=w)
	self.timer() #������ʱ��
connect('statusbar_init', statusbar_init)

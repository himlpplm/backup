#-*- coding:utf-8 -*-

#���·�ʽ
#��ʱˢ�� ���ݽ�����Ϣ
#������ֹ ����״̬��Ϣ

global num
num = 1

def status_1(self):
	global num
	self.text = str(num)
	num += 1

def status_2(self):
	pass

def status_3(self):
	pass

def status_4(self):
	pass


statusbar_mark = [None, None, 3, 4] #NoneΪ��ʱˢ��
statusbar_event = [status_1, status_2, status_3, status_4]
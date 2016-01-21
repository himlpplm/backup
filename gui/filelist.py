#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from kivy.core.window import Window

from clickmenu import ClickMenu
from background import BackGround
from hoverbehavior import HoverBehavior
import time

from kivy.logger import Logger
from tools import *


class AttributeFileLabel(Label):
	def insert(self, **kwargs):
		insert_args(self, **kwargs)

	def delete(self, **kwargs):
		delete_args(self, parent=True, **kwargs)

	def update(self, **kwargs):
		insert_args(self, **kwargs)


class FileLabel(BackGround, GridLayout, HoverBehavior):
	@apply_insert(AttributeFileLabel)
	def insert(self, **kwargs):
		pass

	@apply_delete
	def delete(self, **kwargs):
		pass

	@apply_update
	def update(self, **kwargs):
		pass

	@apply_destroy
	def destroy(self, **kwargs):
		pass

	def on_touch_down(self, touch):
		#���ѡ����ֱ�Ӵ�ѡ����
		#���δѡ�����������ѡ�ѡ����Ȼ���ѡ����
		if self.collide_point(touch.x, touch.y):
			if touch.button == 'left':
				if self.select == 0 or self.select == 1:
					self.selected(2)
				elif self.select == 2:
					self.selected(1)
			elif touch.button == 'right':
				if self.select == 0 or self.select == 1:
					for child in self.parent.children:
						if child.select:
							child.selected(0)
					self.selected(2)

	def on_enter(self, *args):
		#��������Ҽ��˵�����ѡ��
		try:
			if not self.parent.enable:
				return
			#FileList��click_menu
			if self.parent.click_menu.status:
				return
		except: pass
		#ѡ��ǰ��������ѡ�е����
		for child in self.parent.children:
			if child.select == 1:
				child.selected(0)
		if self.select == 0:
			self.selected(1)

	def on_leave(self, *args):
		if self.select == 1:
			self.selected(0)


class FileList(GridLayout):
	enable = True

	@apply_insert(FileLabel)
	def insert(self, **kwargs):
		pass

	@apply_delete
	def delete(self, **kwargs):
		pass

	@apply_update
	def update(self, **kwargs):
		pass

	@apply_destroy
	def destroy(self, **kwargs):
		pass

	def clear(self, **kwargs):
		for child in self.children[::-1]:
			child.destroy()

	click_menu = ClickMenu()

	def on_touch_down(self, touch):
		if not self.click_menu:
			return
		#δ�򿪲˵�����
		if not self.click_menu.status or touch.button not in ['scrollup', 'scrolldown', 'middle']:
			super(FileList, self).on_touch_down(touch) #�ȵ����ӽڵ���¼�����selectֵ
		#Logger.info(str(touch.button))
		if touch.button not in ['scrollup', 'scrolldown', 'middle']:
			self.click_menu.close()
		if self.collide_point(touch.x, touch.y):
			if touch.button == 'right':
				self.click_menu.open(Window.mouse_pos) #touch������Ϊ�������
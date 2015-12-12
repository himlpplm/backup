#-*- coding:utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import NumericProperty

from kivy.core.window import Window

from clickmenu import BackGround, ClickMenu
from hoverbehavior import HoverBehavior
import time

from kivy.logger import Logger
from tools import *

from kivy.lang import Builder
Builder.load_file('filemanager.kv')


class AttributeFileLabel(Label):
	def insert(self, **kwargs):
		insert_args(self, **kwargs)

	def delete(self, **kwargs):
		delete_args(self, **kwargs)

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

	def on_touch_down(self, touch):
		#如果选中则直接打开选项栏
		#如果未选中则清空其它选项并选择该项，然后打开选项栏
		if self.collide_point(touch.x, touch.y):
			if touch.button == 'left':
				if self.select == 0 or self.select == 1:
					self.selected(2)
				elif self.select == 2:
					self.selected(0)
			elif touch.button == 'right':
				if self.select == 0 or self.select == 1:
					for child in self.parent.children:
						if child.select:
							child.selected(0)
					self.selected(2)

	def on_enter(self, *args):
		#如果打开了右键菜单，则不选中
		try:
			if not self.parent.enable:
				return
			#ListLabel的click_menu
			if self.parent.click_menu.status:
				return
		except: pass
		#选中前，将其它选中的清空
		for child in self.parent.children:
			if child.select == 1:
				child.selected(0)
		if self.select == 0:
			self.selected(1)

	def on_leave(self, *args):
		if self.select == 1:
			self.selected(0)


class AttributeTitleLabel(Label):
	reverse = NumericProperty(0)
	def insert(self, **kwargs):
		insert_args(self, **kwargs)
		if isinstance(self.parent, TitleLabel):
			if len(self.parent.children) == 1: #开始时第一列初始化排序方式
				self.reverse = 1

	def delete(self, **kwargs):
		delete_args(self, **kwargs)

	def update(self, **kwargs):
		insert_args(self, **kwargs)


#调节宽度，改变排列顺序等功能
class TitleLabel(GridLayout):
	def __init__(self, **kwargs):
		Window.bind(mouse_pos=self.on_mouse_pos)
		super(TitleLabel, self).__init__(**kwargs)

	filelist = None

	#将标题栏和文件列表关联起来
	def mapping(self, filelist):
		self.filelist = filelist

	@apply_insert(AttributeTitleLabel)
	def insert(self, **kwargs):
		pass

	@apply_update
	def update(self, **kwargs):
		pass

	#第num个标题后的分隔线向右移动distance个单位
	def stretch(self, num, distance):
		width_min = 40 #最小宽度
		if distance == 0: #移动0距离时直接返回
			return
		children = self.children[::-1]
		if num < 0 or num > len(children):  #超出范围
			return
		children[num].width += distance
		if children[num].width < width_min:
			children[num].width = width_min

		#调节子标题后重新设置宽度
		self.width = sum([child.width for child in self.children])

		if self.filelist:
			for filelabel in self.filelist.children:
				children = filelabel.children[::-1]
				children[num].width += distance
				if children[num].width < width_min:
					children[num].width = width_min
				filelabel.width = sum([child.width for child in filelabel.children])

	#将第num个标题插入到position之后
	def change(self, num, position):
		children = self.children[::-1]
		if num < 0 or num > len(children):  #超出范围
			return
		if position < 0 or position > len(children):  #超出范围
			return

		if num == position: #相同位置，无须移动
			return
		move_label = children.pop(num)
		children = children[:position] + [move_label] + children[position:]
		self.children = children[::-1]

		if self.filelist:
			for filelabel in self.filelist.children:
				children = filelabel.children[::-1]
				if num == position: #相同位置，无须移动
					return
				move_label = children.pop(num)
				children = children[:position] + [move_label] + children[position:]
				filelabel.children = children[::-1]

	#根据reverse值进行排序
	def auto_sort(self):
		children = self.children[::-1]
		if self.filelist:
			for num, child in enumerate(children):
				if child.reverse != 0:
					def compare(x, y):
						try: #如果为数字，则转换为数字比较
							return cmp(float(x), float(y))
						except:
							return cmp(x, y)
					key = lambda x: x.children[::-1][num].text
					if child.reverse == 1:
						reverse = True
					else:
						reverse = False
					#reverse=True，从小到大，reverse=False，从大到小
					self.filelist.children = sorted(self.filelist.children, cmp=compare, key=key, reverse=reverse)
					break

	#将文件列表按num的compare顺序排列
	def sort(self, num):
		children = self.children[::-1]
		if num < 0 or num > len(children):  #超出范围	
			return

		if self.filelist:
			child_reverse = children[num].reverse
			#清空其它的reverse
			for child in children:
				child.reverse = 0

			if child_reverse <= 0:
				children[num].reverse = 1
			else:
				children[num].reverse = -1
			
			self.auto_sort()

	#事件类型
	move_type = 0
	#操作编号
	move_num = -1
	move_position = -1
	#上一个点
	move_pos = None
	#点击的控件初始位置
	move_base = None
	#点击之间是否有移动，无移动释放时则是排序事件
	is_move = False

	#判定宽度
	split_width = 10

	def get_type(self):
		pos = Window.mouse_pos[0]
		children = self.children[::-1]
		for child in children:
			split_line = child.x + child.width
			if split_line - self.split_width < pos < split_line + self.split_width:
				return 1
		return 2

	def get_num(self):
		pos = Window.mouse_pos[0]
		children = self.children[::-1]
		for num, child in enumerate(children):
			if num == self.move_num:
				continue
			if child.x < pos <= child.x + child.width:
				split_left = child.x + self.split_width
				split_right = child.x + child.width - self.split_width
				if child.x < pos <= split_left:
					side = -1
				elif split_right < pos <= child.x + child.width:
					side = 1
				else:
					side = 0
				return (num, side)
		return (self.move_num, 0)

	def on_mouse_pos(self, *args):
		if self.filelist.click_menu.status:
				return
		try:
			import win32api
			import win32con
			if self.move_type == 1 or (self.move_type != 2 and self.get_type() == 1 and self.y < Window.mouse_pos[1] < self.y + self.height):
				win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_SIZEWE))
			#else:
			#	win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_ARROW))
		except:
			pass

	#调节宽度事件，move_type = 1
	#移动位置事件，move_type = 2
	def on_touch_down(self, touch):
		#判断鼠标位置，靠近右边界进入调节宽度状态，其它位置进入移动位置状态
		super(TitleLabel, self).on_touch_down(touch)
		if not self.collide_point(touch.x, touch.y):
			return
		if touch.button != 'left':
			return
		self.move_type = self.get_type()
		self.move_num, side = self.get_num()
		if side == -1: #在左侧时拉伸上一个
			self.move_num -= 1
		self.move_pos = int(round(touch.x)), int(round(touch.y))
		self.move_base = list(self.children[::-1][self.move_num].pos)
		self.is_move = False
		self.filelist.enable = False
		self.on_mouse_pos()
		self.filelist.click_menu.close() #关闭右键菜单

	def on_touch_move(self, touch):
		super(TitleLabel, self).on_touch_move(touch)
		self.is_move = True
		#移动时鼠标可能移出范围
		if touch.button != 'left':
			return
		pos = int(round(touch.x)), int(round(touch.y))
		if self.move_type == 1:
			self.stretch(self.move_num, pos[0] - self.move_pos[0])
		elif self.move_type == 2:
			num, side = self.get_num()
			child = self.children[::-1][self.move_num]
			child.x += pos[0] - self.move_pos[0]
			if side:
				self.move_position = num
		self.move_pos = pos
		self.on_mouse_pos()

	def on_touch_up(self, touch):
		super(TitleLabel, self).on_touch_up(touch)
		if touch.button != 'left':
			return
		num, side = self.get_num()
		child = self.children[::-1][self.move_num]
		if self.move_type == 2:
			if not self.is_move:
				self.sort(self.move_num)
			else:
				child.pos = self.move_base
				self.change(self.move_num, self.move_position)
				
		self.move_type = 0
		self.move_num = -1
		self.move_position = -1
		self.move_pos = None
		self.move_base = None
		self.is_move = False
		self.filelist.enable = True
		self.on_mouse_pos()


class ListLabel(GridLayout):
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

	click_menu = None

	def on_touch_down(self, touch):
		if not self.click_menu:
			return
		#未打开菜单或不是
		if not self.click_menu.status or touch.button not in ['scrollup', 'scrolldown', 'middle']:
			super(ListLabel, self).on_touch_down(touch) #先调用子节点的事件更新select值
		#Logger.info(str(touch.button))
		if touch.button not in ['scrollup', 'scrolldown', 'middle']:
			self.click_menu.close()
		if self.collide_point(touch.x, touch.y):
			if touch.button == 'right':
				self.click_menu.open(Window.mouse_pos) #touch的坐标为相对坐标

class FileManager(GridLayout):
	def __init__(self, **kwargs):
		super(FileManager, self).__init__(**kwargs)
		#文件列表
		self.filelist = ListLabel()
		self.filelist.click_menu = ClickMenu()
		self.filelist.bind(minimum_height=self.filelist.setter('height'), minimum_width=self.filelist.setter('width'))

		#标题栏
		self.titlelabel = TitleLabel()
		self.titlelabel.mapping(self.filelist)

		#滚动条
		self.scrollview = ScrollView()
		self.scrollview.add_widget(self.filelist)

		self.add_widget(self.titlelabel)
		self.add_widget(self.scrollview)

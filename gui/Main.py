#-*- coding:utf-8 -*-
from kivy.app import App
from kivy.uix.button import Button

class Main(App):
    def build(self):
        return Button(text='Hello World')

Main().run()
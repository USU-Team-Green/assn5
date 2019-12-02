import tkinter
import time
from sqliDetector import *



class View():
  children = []

  def clear(self):
    for child in self.children:
      child.destroy()


class Signup(View):
  def __init__(self, master, go_success, go_login):
    super().__init__()
    self.children = [
      tkinter.Label(master, text="What would you like to test?"),
      tkinter.Button(master, text="ItemName", command=go_success),
      tkinter.Button(master, text="Username and Password", command=go_login),
    ]
    for child in self.children:
      child.pack()


class Success(View):
  def generate(self):
    query = 'SELECT ItemDescription, ItemPrice\nFROM Items\nWHERE ItemName = {};'.format(self.password.get())
    self.score, self.messages = test_for_general_danger_patterns(query)
    result = ''
    result += 'The score is {} ({}%)'.format(self.score, self.score * 100)
    result += '\n'
    for mes in self.messages:
      if mes:
        result += mes + '\n'
    self.errorText.set(result)

  def __init__(self, master, go_main):
    super().__init__()
    self.password = tkinter.Entry(master)
    self.errorText = tkinter.StringVar(master)
    self.errors = tkinter.Label(master, textvariable=self.errorText)
    self.children = [
      tkinter.Label(master, text="ItemName"),
      self.password,
      tkinter.Button(master, text="calculate", command=self.generate),
      tkinter.Button(master, text="main screen", command=go_main),
      self.errors
    ]
    for child in self.children:
      child.pack()


class Login(View):
  def generate(self):
    uname = self.username.get()
    pas = self.username.get()
    query = 'SELECT Accounts\nFROM Users\nWHERE Username={} AND Password={};'.format(uname, pas)
    self.score, self.messages = test_for_general_danger_patterns(query)
    result = ''
    result += 'The score is {} ({}%)'.format(self.score, self.score * 100)
    result += '\n'
    for mes in self.messages:
      if mes:
        result += mes + '\n'
    self.errorText.set(result)

  def __init__(self, master, go_main):
    super().__init__()
    self.username = tkinter.Entry(master)
    self.password = tkinter.Entry(master)
    self.errorText = tkinter.StringVar(master)
    self.errors = tkinter.Label(master, textvariable=self.errorText)
    self.children = [
      tkinter.Label(master, text="Username"),
      self.username,
      tkinter.Label(master, text="Password"),
      self.password,
      tkinter.Button(master, text="calculate", command=self.generate),
      tkinter.Button(master, text="main screen", command=go_main),
      self.errors
    ]
    for child in self.children:
      child.pack()


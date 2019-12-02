import tkinter
from views import Signup, Login, Success

class MainLoopClass():
    top = tkinter.Tk()

    def __init__(self):
        self.top.geometry("800x480")
        self.go_main()
        self.top.mainloop()

    def clear(self):
        if hasattr(self,'children'):
            self.children.clear()

    def go_main(self):
        self.clear()
        self.children = Signup(self.top, self.go_user, self.go_item)

    def go_item(self):
        self.clear()
        self.children = Login(self.top, self.go_main)

    def go_user(self):
        self.clear()
        self.children = Success(self.top, self.go_main)

if __name__ == '__main__':
    main = MainLoopClass()

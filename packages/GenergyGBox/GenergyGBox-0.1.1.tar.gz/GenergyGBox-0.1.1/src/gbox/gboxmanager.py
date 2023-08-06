from gbox.gpio import GPIOController


class GBox(object):
    def __init__(self):
        print("This is a init function")

    @staticmethod
    def method():
        print("This is my method")
        gpio = GPIOController()
        gpio.method()

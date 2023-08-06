import os


class MADApp:

    def __init__(self):
        os.system("pip install ../utils/FARM --quiet")

    def mad_print(self, text):
        print(text)

import os


class MADApp:

    def __init__(self):
        parent_path = self.get_parent_dir(os.getcwd())
        farm_util = parent_path + "/utils/FARM"
        print(farm_util)
        os.system(f"pip install {farm_util}")

    def get_parent_dir(self, directory):
        return os.path.dirname(directory)

    def mad_print(self, text):
        print(text)

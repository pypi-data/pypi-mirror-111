import os


class MADApp:

    def __init__(self):
        print("INFO: Initializing MAD Framework")
        print("INFO: Installing required packages and models.")
        self.install_farm()
        self.pretrained_model()
        
    
    def install_farm(self):
        try:
            os.system("pip install git+https://github.com/imdiptanu/FARM.git --quiet")
        except Exception as e:
            print("ERROR: Installing FARM! Error:", e)


    def pretrained_model(self):
        try:
            print("INFO: Downloading mad-bert-uncased model from remote.")
            os.system("wget https://www.dropbox.com/s/sfvwyn3bw49x93j/mad-bert-uncased.zip")
            cur_path = os.getcwd()
            model_path = cur_path + "/mad-bert-uncased.zip"
            os.system(f"unzip {model_path}")
            print("INFO: Model downloaded Successfully.")
        except Exception as e:
            print("ERROR: Downloading pre-trained model! Error:", e)


    def mad_print(self, text):
        print(text)

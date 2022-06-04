import os
import pandas as pd


def read_config() -> pd.DataFrame:
        data = pd.read_csv('../config/config.txt', sep="=", index_col=0, header=None)
        data.columns = ["value"]
        return data  

def tesseract_file_path():
    confList = read_config()
    return os.path.join(confList.loc['tesseract'][0], 'tesseract.exe')

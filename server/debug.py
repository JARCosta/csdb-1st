
import json
import os
from datetime import datetime


def save_temp(STEAMID: str, js:dict):
    file_name ="saves/"+ STEAMID + "/.temp.json"
    
    file = open(file_name,'w',encoding='utf-8')
    file.write(json.dumps(js, indent=4))
    file.close()
    print("saving :", file_name)




def load_last_save(STEAMID: str):
    dir_path = './saves/' + STEAMID
    files = sorted(os.listdir(dir_path))
    files.reverse()
    print(files)

    try:
        print("loading last save:", files[0])
        file = open(dir_path + "/" + files[0], 'r',encoding='utf-8')
        js = json.load(file)
        file.close()
        return js
    except:
        print(f"No files found in {dir_path}")
    


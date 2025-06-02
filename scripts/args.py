import os
import datetime

def make_results_folder():
    changes = input("変更点を入力してください: ")
    date = datetime.datetime.now().strftime("%m-%d-%H-%M")
    folder_name = f"{date}_{changes}"
    folder_path = os.path.join("results", folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

results_path = make_results_folder()
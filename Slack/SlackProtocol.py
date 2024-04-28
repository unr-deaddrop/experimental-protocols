import logging
import os
import requests
from slack_sdk import WebClient

with open("TOKEN.txt", "r") as f:
    SLACK_TOKEN = f.read()


#logging.basicConfig(level=logging.DEBUG)
client = WebClient(SLACK_TOKEN)


auth_test = client.auth_test()
bot_user_id = auth_test["user_id"]
print(f"App's bot user: {bot_user_id}")

def upload_test():
    new_file = client.files_upload_v2(
        title="My Test Text File",
        filename="test.txt",
        content="Hi there! This is a text file!",
    )

    files = client.files_list(user=bot_user_id)
    file_url = new_file.get("file").get("permalink")

    new_message = client.chat_postMessage(
        channel="protocol_upload",
        text=f"Here is the file: {file_url}",
    )

def upload_local():
    for file in os.listdir("local_files"):
        with open(os.path.join("local_files", file), "rb") as f:
            data = f.read()
            
        new_file = client.files_upload_v2(
            title= file,
            filename= file,
            content= data,
        )

        files = client.files_list(user=bot_user_id)
        file_url = new_file.get("file").get("permalink")

        new_message = client.chat_postMessage(
            channel="protocol_upload",
            text=f"Here is the file: {file_url}",
        )

def read_files(): 
    files = client.files_list(user=bot_user_id)
 
    for file in files["files"]:
        fileurl = file['url_private']
        headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
        
        response = requests.get(fileurl, headers=headers)
        
        if response.status_code == 200:
            with open('./local_files/' + file['name'], 'wb') as f:
                f.write(response.content)
                print(f"{file['name']} downloaded successfully.")
        else:
            print(f"Failed to download {file['name']}. HTTP status code: {response.status_code}")
    
def delete_files():
    for page in client.files_list(user=bot_user_id):
        for file in page.get("files", []):
            client.files_delete(file=file["id"])
  

upload_local()
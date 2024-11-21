import os
import requests
# ส่วนนี้จะเป็นตัว ส่งไฟร์ 
def upload_files_to_server(local_folder, server_url):
    # Prepare the files for upload
    files = []
    for root, dirs, file_names in os.walk(local_folder):
      for file_name in file_names:
          file_path = os.path.join(root, file_name)
          
          if os.path.isfile(file_path):
              # Get the relative path for the file (relative to the local_folder)
              relative_path = os.path.relpath(file_path, local_folder)
              # Append the file and its relative path as metadata
              files.append(('files[]', (relative_path, open(file_path, 'rb'))))
    
    
    
    if len(files) == 0:
        print("No files found in the folder for uploading.")
        return
    
    try:
        # Perform the POST request to upload the files
        SaveTo = r'D:\FromCopy'
        data = {'SaveTo': SaveTo}
        response = requests.post(server_url, files=files,data=data)

        # Check for successful upload
        if response.status_code == 200:
            print("Files uploaded successfully.")
        else:
            print(f"Failed to upload files. Server responded with: {response.status_code} {response.text}")
    
    except Exception as e:
        print(f"An error occurred during the file upload: {e}")
    
    # finally:
    #     # Close all the open file objects
    #     for _, file_obj in files:
    #         file_obj.close()

if __name__ == '__main__':
    local_folder = r'G:\M_save\python\AppUploadFileToserver\static\uploads\DeployWeb_1_0_0_5'  # Folder to upload files from
    server_url = 'http://10.88.88.4:5010/transfer'  # Server URL to upload files to
    
    upload_files_to_server(local_folder, server_url)

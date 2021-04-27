import sys
import glob
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']


def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./token.pickle'):
        with open('./token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('./token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build('drive', 'v3', credentials=creds)


def do_stuff(ext, folder_id, service):
    files = glob.glob1(path, "*" + ext)
    total = len(files)
    print("Total " + ext[1:] + " files: ", total)

    for i in range(total):
        # first, define file metadata, such as the name and the parent folder ID
        g = files[i]

        file_metadata = {
            "name": g,
            "parents": [folder_id]
        }
        print("\nUploading ", g, " to gdrive.")
        media = MediaFileUpload(path + g, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print("File created, id:", file.get("id"))
        print("Uploaded ", i + 1, "/", total)


def upload_files():
    # authenticate account
    service = get_gdrive_service()
    # folder details we want to make
    folder_metadata = {
        "name": folder,
        "mimeType": "application/vnd.google-apps.folder"
    }
    # create the folder
    file = service.files().create(body=folder_metadata, fields="id").execute()
    # get the folder id
    folder_id = file.get("id")
    print("Folder ID:", folder_id)

    # upload
    FilesExts = ['.jpg', '.jpeg', '.png', '.mp4', '.mkv']
    for i in FilesExts:
        do_stuff(i, folder_id, service)


if __name__ == '__main__':

    # Input dir
    path = input('Enter path to folder: ')

    if os.path.isdir(path):
        # Output dir
        folder = input("\nWhat do you want to call the folder: ")
        upload_files()
    else:
        sys.exit(1)

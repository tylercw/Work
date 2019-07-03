from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors

import auth

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
authInst = auth.auth(SCOPES)
credentials = authInst.getCredentials()
drive_service = authInst.getservice()

def files(size):
    results = drive_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id'], item['mimeType']))

def folderID():
    page_token = None
    while True:
        response = drive_service.files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            if file.get('name') == "Nathan Graduation":
                folder_id = file.get('id')
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
##    foldid="'"+folder_id+"'"
##    query="parents in "+foldid
##    r = drive_service.files().list(q=query,pageSize=10,fields="nextPageToken, files(id,name)").execute()
##    items = r.get('files',[])
##    print(items)
    return folder_id

def filesinfolder(drive_service, folder_id):
    page_token = None
    while True:
        query = "parents in " + "'"+folder_id+"'"
        response = drive_service.files().list(q=query, spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            print(file.get('name'))
        page_token = response.get('nextpageToken', None)
        if page_token is None:
            break

filesinfolder(drive_service, folderID())

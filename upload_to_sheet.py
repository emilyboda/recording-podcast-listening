from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def auth():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service

def clear_sheet(service, sheet_id, sheet_name, last_column):

    # Call the Sheets API
    sheet = service.spreadsheets()
    
    batch_clear_values_request_body = {'ranges':[sheet_name+'!A2:'+last_column]}
    clear_result = sheet.values().batchClear(spreadsheetId=sheet_id, body = batch_clear_values_request_body).execute()
    

def update_sheet(service, sheet_id, sheet_name, last_column,values):
    # Call the Sheets API
    sheet = service.spreadsheets()
    rows = len(values)
    data = [
            {
                'range':sheet_name+'!A2:'+last_column+str(rows+1),
                'values': values
            }
        ]
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data':data
        }
    result = sheet.values().batchUpdate(spreadsheetId=sheet_id, body = body).execute()
    print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

def append_to_sheet(service,sheet_id, sheet_name,last_column,values):
   
    # get the number of rows currently in the sheet
    rng = sheet_name+'!A1:'+last_column
    result = service.spreadsheets().values().get(spreadsheetId=sheet_id,range=rng).execute()
    row_num = len(result.get('values',[]))+1
    
    # add one line of data after the current
    data = [
            {
                'range':sheet_name+'!A'+str(row_num)+':'+last_column+str(len(values)+row_num-1),
                'values': [values]
            }
        ]
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data':data
        }
    result = service.spreadsheets().values().batchUpdate(spreadsheetId=sheet_id, body = body).execute()

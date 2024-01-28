# Import necessary libraries
import googleapiclient.discovery
import pandas as pd

# Authenticate Google Drive API
drive_service = googleapiclient.discovery.build('drive', 'v3')

# Define function to get all files in a folder
def get_all_files(folder_id):
  files = []
  page_token = None
  while True:
    response = drive_service.files().list(q="'{}' in parents".format(folder_id),
                                         spaces='drive',
                                         fields='nextPageToken, files(id, name)',
                                         pageToken=page_token).execute()
    for file in response.get('files', []):
      files.append(file)
    page_token = response.get('nextPageToken', None)
    if page_token is None:
      break
  return files

# Define function to compare two dataframes
def compare_dataframes(df1, df2):
  # Compare columns
  for col in df1.columns:
    if col not in df2.columns:
      print('Column "{}" not found in both dataframes'.format(col))
    else:
      # Compare values in the column
      for i in range(len(df1)):
        if df1.loc[i, col] != df2.loc[i, col]:
          print('Values in row {} for column "{}" are different'.format(i, col))

# Define function to remove duplicates from a folder
def remove_duplicates(folder_id):
  # Get all files in the folder
  files = get_all_files(folder_id)

  # Create a dictionary to store dataframes
  dataframes = {}

  # Read data from each file and store it in the dictionary
  for file in files:
    if file['mimeType'] in ['application/vnd.google-apps.spreadsheet', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
      file_id = file['id']
      df = pd.read_csv('https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(file_id))
      dataframes[file_id] = df

  # Compare dataframes and remove duplicates

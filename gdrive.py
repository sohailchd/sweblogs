import os
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# Define the scope for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Path to your service account key file
SERVICE_ACCOUNT_FILE = '/Users/sohail/Desktop/workspace/gitio/tests/credentials.json'

# Authenticate using the service account
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Drive API client
service = build('drive', 'v3', credentials=creds)

def Download_Colab_Notebook(file_id, output_path):
    """
    Download a Google Colab notebook given its file ID.

    Parameters:
    - file_id: ID of the Google Colab notebook file.
    - output_path: Path to save the downloaded notebook file.
    """
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(output_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

    print(f"Notebook downloaded to {output_path}")

# # Example usage
# # Shareable link: "https://drive.google.com/file/d/your_file_id/view?usp=sharing"
# # Extract the file ID from the shareable link
# ## 1c_BRX7waz8nBRMFVSoJnz1SMGorFqZhS
# file_id = "1c_BRX7waz8nBRMFVSoJnz1SMGorFqZhS"
# output_path = "downloaded_notebook.ipynb"

# Download_Colab_Notebook(file_id, output_path)

# --------------------------------------------------------------------------
# Example demonstrates how to export OneDrive files into local file system
# --------------------------------------------------------------------------

import os
import tempfile

from examples import acquire_token_by_client_credentials
from office365.graph_client import GraphClient
from tests import test_user_principal_name


client = GraphClient(acquire_token_by_client_credentials)
drive = client.users[test_user_principal_name].drive  # get user's drive
with tempfile.TemporaryDirectory() as local_path:
    drive_items = drive.root.children.get().execute_query()
    file_items = [item for item in drive_items if item.file is not None]    # files only
    for drive_item in file_items:
        with open(os.path.join(local_path, drive_item.name), 'wb') as local_file:
            drive_item.download(local_file).execute_query()  # download file content
        print("File '{0}' has been downloaded".format(local_file.name))


from __future__ import print_function
import httplib2
import os
import base64
import pprint
import pdb

from apiclient import discovery, errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    store_dir = 'test'
    query = ''

    try:
        response = service.users().messages().list(userId='me',
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        if not messages:
            print('No messages found.')
        else:
            pp = pprint.PrettyPrinter(indent=4)
            for msg in messages:
                msg_id = msg['id']
                message = service.users().messages().get(userId='me', id=msg_id).execute()
                # pdb.set_trace()
                #pp.pprint(message['payload'])
                for i,part in enumerate(message['payload']['parts']):
                    #print('PAAART:')
                    #pp.pprint(part)
                    print ('ITER No. ' + str(i))
                    if part['mimeType'] == 'text/plain':
                        print('ESTA PART MOLA')
                        body_data = base64.urlsafe_b64decode(
                            part['body']['data'].encode('UTF-8'))
                        print(body_data)

                        if not os.path.exists(store_dir):
                            os.makedirs(store_dir)

                        path = store_dir + '/pepe' + str(i) + '.html'

                        aux = i
                        while os.path.isfile(path):
                            aux = aux + 1
                            path = store_dir + '/pepe' + str(aux) + '.html'
                        print('se guarda en ' + path)
                        f = open(path, 'w')
                        f.write(body_data)
                        f.close()

                    if part['filename']:
                        # pp.pprint(part)
                        attach = service.users().messages().attachments().get(
                            userId='me', messageId=msg_id, id=part['body']['attachmentId']).execute()
                        file_data = base64.urlsafe_b64decode(attach['data']
                                                             .encode('UTF-8'))
                        if not os.path.exists(store_dir):
                            os.makedirs(store_dir)
                        path = store_dir + '/' + part['filename']

                        f = open(path, 'w')
                        f.write(file_data)
                        f.close()

    except errors.HttpError, error:
        print ('An error occurred: %s') % error


if __name__ == '__main__':
    main()

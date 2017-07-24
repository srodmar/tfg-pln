from __future__ import print_function
import httplib2
import os
import base64
import pprint
import pdb
import email

from apiclient import discovery, errors, mimeparse
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from email.mime.text import MIMEText

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'
pp = pprint.PrettyPrinter(indent=4)


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
    store_dir = 'storage'
    query = ''

    try:
        response = service.users().messages().list(userId='me',
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me', q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        if not messages:
            print('No messages found.')
        else:
            for msg in messages:
                msg_id = msg['id']
                message = service.users().messages().get(userId='me', id=msg_id).execute()
                #print('MESSAGEEE:')
                #pp.pprint(get_subject(message['payload']['headers']))
                iter_part(message['payload'], store_dir, service, msg_id)

    except errors.HttpError, error:
        print ('An error occurred: %s') % error


def get_subject(headers):
    for item in headers:
        if item['name'] == 'Subject':
            return item['value']


def iter_part(payload, store_dir, service, msg_id):
    #print('PAYLOAD', payload)
    if 'parts' in payload:
        for i, part in enumerate(payload['parts']):
            if part['mimeType'] == 'text/plain':
                save_text(part['body']['data'], msg_id,
                        get_subject(payload['headers']), store_dir)

            elif part['mimeType'] == 'multipart/alternative':
                print ('IF MALIGNOOOOOOOOO')
                iter_part(part, store_dir, service, msg_id)

            # if part['filename']:
            #    save_file(part, msg_id, store_dir, service)
    elif payload['mimeType'] == 'text/plain':
        save_text(payload['body']['data'], msg_id, get_subject(payload['headers']), store_dir)

    elif payload['mimeType'] == 'multipart/alternative':
        print ('IF MALIGNOOOOOOOOO')
        iter_part(payload, store_dir, service, msg_id)


def save_text(text_data, msg_id, subject, store_dir):
    store_dir = store_dir + '/body_texts'
    body_data = base64.urlsafe_b64decode(text_data.encode('UTF-8'))

    if not os.path.exists(store_dir):
        os.makedirs(store_dir)

    if not subject:
        subject = 'Sin Asunto'
    if '/' in subject:
        subject = subject.replace('/', '')
    path = store_dir + '/' + subject + '_' + msg_id + '.txt'
    if not os.path.isfile(path):
        f = open(path, 'w')
        f.write(body_data)
        f.close()

    '''i = 1
    path = store_dir + '/mail_text' + str(i) + '.html'
    while os.path.isfile(path):
        i = i + 1
        path = store_dir + '/mail_text' + str(i) + '.html'
    print('se guarda en ' + path)
    f = open(path, 'w')
    f.write(body_data)
    f.close()'''


def save_file(part, msg_id, store_dir, service):
    store_dir = store_dir + '/attachments'
    attach = service.users().messages().attachments().get(
        userId='me', messageId=msg_id, id=part['body']['attachmentId']).execute()
    file_data = base64.urlsafe_b64decode(attach['data'].encode('UTF-8'))
    if not os.path.exists(store_dir):
        os.makedirs(store_dir)

    path = store_dir + '/' + msg_id + '_' + part['filename']
    if not os.path.isfile(path):
        f = open(path, 'w')
        f.write(file_data)
        f.close()

def delete_mails(query):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    try:
        response = service.users().messages().list(userId='me',
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me', q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        if not messages:
            print('No messages found.')
        else:
            for i, msg in enumerate(messages):
                msg_id = msg['id']
                message = service.users().messages().trash(userId='me', id=msg_id).execute()
                print ('Deleted Message: %s' % message['id'])
                print ('Deleted message #', i, ' of ', len(messages))

    except errors.HttpError, error:
        print ('An error occurred: %s') % error

def send_trec():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    trec_dir = 'trec07p/data'
    files = os.listdir(trec_dir)

    for i, file in enumerate(files[:120]):
        with open(trec_dir + '/' + file, 'r') as current_file:
            #text = current_file.read()
            message = email.message_from_file(current_file)
        #message = MIMEText(text, 'html')
        del message['To']
        message['To'] = 'test.tfg.pln@gmail.com'
        sub = message['Subject']
        del message['Subject']
        message['Subject'] = sub + ' - Trec Spam'
        #pp.pprint(message.as_string())
        body = {'raw': base64.urlsafe_b64encode(message.as_string())}

        try:
            message_sent = (service.users().messages().send(userId='me', body=body).execute())
            print ('Message Id: %s' % message_sent['id'])
            print ('Sent message #', i, ' of ', len(files))
        except errors.HttpError, error:
            print ('An error occurred: %s' % error)

    delete_mails('from:nobody@gmail.com')        

def send_enron():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    enron_dir = 'maildir/brawner-s/all_documents'
    files = os.listdir(enron_dir)

    for i, file in enumerate(files):
        with open(enron_dir + '/' + file, 'r') as current_file:
            #text = current_file.read()
            message = email.message_from_file(current_file)
        #message = MIMEText(text, 'html')
        del message['To']
        message['To'] = 'test.tfg.pln@gmail.com'
        sub = message['Subject']
        del message['Subject']
        message['Subject'] = sub + ' - Enron Mail'
        body = {'raw': base64.urlsafe_b64encode(message.as_string())}

        try:
            message_sent = (service.users().messages().send(userId='me', body=body).execute())
            print ('Message Id: %s' % message_sent['id'])
            print ('Sent message #', i, ' of ', len(files))
        except errors.HttpError, error:
            print ('An error occurred: %s' % error)

    delete_mails('from:nobody@gmail.com')        

if __name__ == '__main__':
    #send_trec()
    send_enron()

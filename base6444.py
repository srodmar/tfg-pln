import base64



file_data = base64.urlsafe_b64decode()

store_dir = 'base64'
if not os.path.exists(store_dir):
    os.makedirs(store_dir)
path = store_dir + '/baseee'

f = open(path, 'w')
f.write(file_data)
f.close()

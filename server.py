from flask import Flask, request
import threading
import garth
import urllib.request
import os

DESTDIR = os.environ['DESTDIR']

api = Flask(__name__)
api.config['debug'] = True

def save_and_upload(url):
    filename = os.path.basename(url)
    path = os.path.join(DESTDIR, filename)
    print('filename: %s' % (filename, ))
    if os.path.exists(path):
        print('file already exists')
        return
    with urllib.request.urlopen(url) as r:
        with open(path, 'wb') as f:
            f.write(r.read())
    print('saved')
    garth.login(os.environ['GARMIN_LOGIN'], os.environ['GARMIN_PASSWORD'])
    print('connected')
    with open(path, 'rb') as f:
        uploaded = garth.client.upload(f)
        print(uploaded)
    print('uploaded')

@api.route('/', methods=['GET'])
def get_root():
  return 'ok'

@api.route('/webhook', methods=['POST'])
def post_webhook():
    print('post')
    print('post')
    data = request.get_json()
    print('data', data)
    url = data['workout_summary']['file']['url']
    print('url: %s' % (url, ))
    thread = threading.Thread(target=save_and_upload, args=(url,))
    thread.start()

    return '{}'

if __name__ == '__main__':
    print('run')
    api.run('0.0.0.0', 5000, debug=True)

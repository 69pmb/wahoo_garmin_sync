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
    print('Filename: %s' % (filename, ))
    if os.path.exists(path):
        print('File already uploaded')
        return
    with urllib.request.urlopen(url) as r:
        with open(path, 'wb') as f:
            f.write(r.read())
    print('File saved')
    garth.login(os.environ['GARMIN_LOGIN'], os.environ['GARMIN_PASSWORD'])
    garth.save("~/.garth")
    print('Connected to Garmin Connect')
    try:
        with open(path, 'rb') as f:
            uploaded = garth.client.upload(f)
            print(uploaded)
        print('Workout successfully uploaded')
    except Exception as e:
        print('Upload failed:', e)

@api.route('/', methods=['GET'])
def get_root():
  return 'ok'

@api.route('/webhook', methods=['POST'])
def post_webhook():
    print('Received post')
    data = request.get_json()
    url = data['workout_summary']['file']['url']
    print('Workout url: %s' % (url, ))
    thread = threading.Thread(target=save_and_upload, args=(url,))
    thread.start()

    return '{}'

if __name__ == '__main__':
    print('run')
    api.run('0.0.0.0', 42195, debug=True)

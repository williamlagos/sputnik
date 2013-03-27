# Include the Dropbox SDK libraries
from dropbox import client, rest, session
from StringIO import StringIO

class Dropbox():
    def __init__(self):
        APP_KEY = '30pb1xxpccvhfqo'
        APP_SECRET = 'kap2qg8dt2cp7cv'
        ACCESS_TYPE = 'app_folder'
        self.sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
        request_token = 's8123g2tz0fb73a'
        request_token_secret = 'kwsa9sapz264uq5'
        access_token = 'q6lds714ncu45k3'
        access_token_secret = 'elvc3gmgbw8b99f'
        self.sess.set_request_token(request_token,request_token_secret)
        self.sess.set_token(access_token,access_token_secret)
    def upload_and_share(self,stream):
        cli = client.DropboxClient(self.sess)
        image_io = StringIO(stream)
        response = cli.put_file('/eimg.png',image_io)
        results = cli.share(response['path'])
        return results['url']

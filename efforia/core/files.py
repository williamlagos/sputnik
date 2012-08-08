# Include the Dropbox SDK libraries
import tornado,os,time,email.utils,mimetypes,stat
from datetime import datetime
from urllib2 import HTTPError
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
        response = cli.put_file('/foto.png',image_io)
        results = cli.share(response['path'])
        return results['url']
    
class FileHandler(tornado.web.StaticFileHandler):
    def get(self,path,include_body=True):
        if os.path.sep != "/":
            path = path.replace("/", os.path.sep)
        abspath = os.path.abspath(os.path.join(self.root, path))
        if not (abspath + os.path.sep).startswith(self.root):
            raise HTTPError(403, "%s is not in root static directory", path)
        if os.path.isdir(abspath) and self.default_filename is not None:
            if not self.request.path.endswith("/"):
                self.redirect(self.request.path + "/")
                return
            abspath = os.path.join(abspath, self.default_filename)
        if not os.path.exists(abspath):
            self.render("404.html")
            #raise HTTPError(404)
        if not os.path.isfile(abspath):
            pass
            #self.render(self.templates()+"404.html")
            #raise HTTPError(403, "%s is not a file", path)

        stat_result = os.stat(abspath)
        modified = datetime.fromtimestamp(stat_result[stat.ST_MTIME])

        self.set_header("Last-Modified", modified)
        if "v" in self.request.arguments:
            self.set_header("Expires", datetime.datetime.utcnow() + \
                                       datetime.timedelta(days=365*10))
            self.set_header("Cache-Control", "max-age=" + str(86400*365*10))
        else:
            self.set_header("Cache-Control", "public")
        mime_type, encoding = mimetypes.guess_type(abspath)
        if mime_type:
            self.set_header("Content-Type", mime_type)

        self.set_extra_headers(path)
        ims_value = self.request.headers.get("If-Modified-Since")
        if ims_value is not None:
            date_tuple = email.utils.parsedate(ims_value)
            if_since = datetime.fromtimestamp(time.mktime(date_tuple))
            if if_since >= modified:
                self.set_status(304)
                return

        if not include_body:
            return
        file = open(abspath, "rb")
        try:
            self.write(file.read())
        finally:
            file.close()

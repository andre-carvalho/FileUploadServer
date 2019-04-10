import os, errno, base64
import fnmatch
from PIL import Image
from io import BytesIO


class B64Utils():

   #constructor
    def __init__(self, path, base64_string=None):
        self.b64 = base64_string
        self.path = path
        if not os.path.exists(path):
            os.mkdir(path)

    def base64Decode(self):
        """Add missing padding to string and return the decoded base64 string."""
        self.b64 = str(self.b64).strip()
        try:
            return base64.b64decode(self.b64)
        except TypeError:
            padding = len(self.b64) % 4
            if padding == 1:
                return ''
            elif padding == 2:
                self.b64 += b'=='
            elif padding == 3:
                self.b64 += b'='
            return base64.b64decode(self.b64)

    def writeToBinary(self, sufix):
        b64out = self.base64Decode()
        im = Image.open(BytesIO(b64out))
        file_ext = im.format.lower()
        path = '{0}/image{1}.{2}'.format(self.path, sufix, file_ext)
        output_file = open(path,'wb')
        output_file.write(b64out)
        output_file.close()

    def readFromBinary(self, sufix):
        file_name = mimetype = ''
        try:
            file_name, mimetype = self.__getFileName(sufix)
        except FileNotFoundError as error:
            raise error
        path = '{0}/{1}'.format(self.path, file_name)
        output_file = open(path,'rb')
        binary = output_file.read()
        output_file.close()        
        return BytesIO(binary), file_name, mimetype

    def __getFileName(self, sufix):
        file_pattern = 'image{0}'.format(sufix)
        file_name = mimetype = ''
        for file in os.listdir(self.path):
            if fnmatch.fnmatch(file, '{0}.*'.format(file_pattern)):
                ext = file.split('.')
                file_name = '{0}.{1}'.format(file_pattern, ext[1])
                mimetype = 'image/{0}'.format(ext[1])
                break
        if file_name == '':
            raise FileNotFoundError(errno.ENOENT, 'Image file not found')
        
        return file_name, mimetype
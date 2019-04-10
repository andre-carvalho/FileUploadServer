#!/usr/bin/python3

class logWriter:

    #constructor
    def __init__(self, path, filename='service_error.log'):
        self.path = path
        self.filename = filename
        
    def write(self, msg):

        path = self.path + '/' + self.filename

        log_file = open(path,'a')
        msg = msg+'\n'
        log_file.write(msg)
        log_file.close()
import os


class AutoReply(object):

    file_name = 'isOpenAutoReply.txt'

    def __init__(self):
        with open(self.file_name, 'r') as f:
            file_text = f.read()
            if file_text == '' or file_text != '1':
                with open(self.file_name, 'w+') as f2:
                    f2.write('0')

    def is_open_auto_reply(self):
        with open(self.file_name, 'r') as f:
            file_text = f.read()
            if file_text == '' or file_text != '1':
                return False
            else:
                return True

    def open(self):
        with open(self.file_name, 'w+') as f:
            f.write('1')

    def close(self):
        with open(self.file_name, 'w+') as f:
            f.write('0')

if __name__ == '__main__':
    A = AutoReply()
    print(A.is_open_auto_reply())
    A.open()
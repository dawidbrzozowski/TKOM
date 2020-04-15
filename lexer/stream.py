class Source:
    def read_line(self):
        pass

    def is_end_of_text(self, last_line=None):
        pass


class FileSource(Source):
    def __init__(self, path):
        self.fs = open(path, 'r')
        self.eof = False

    def read_line(self):
        return self.fs.readline()

    def is_end_of_text(self, last_line=None):
        last_pos = self.fs.tell()
        line = self.read_line()
        self.fs.seek(last_pos)
        return True if line == "" else False

    def __del__(self):
        self.fs.close()


class StdInSource(Source):
    def read_line(self):
        text = input('> ')
        return text

    def is_end_of_text(self, last_line=None):
        return last_line == 'DONE'

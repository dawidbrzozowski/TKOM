STDIN_EOT_TEXT = 'DONE'


class Source:
    def read_line(self):
        pass

    def is_end_of_text(self):
        pass


class FileSource(Source):
    def __init__(self, path):
        self.fs = open(path, 'r')
        self.eof = False

    def read_line(self):
        line = self.fs.readline()
        if not line:
            self.eof = True
        return line

    def is_end_of_text(self):
        return self.eof

    def __del__(self):
        self.fs.close()


class StdInSource(Source):
    def __init__(self):
        self.text = None

    def read_line(self):
        self.text = input('stdin code > ')
        return self.text

    def is_end_of_text(self):
        return self.text == STDIN_EOT_TEXT

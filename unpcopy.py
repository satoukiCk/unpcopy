import sys
import os
import subprocess
import re
import mimetypes
unpackers = []


def register_unpacker(cls): # cls对于classmethod，第一个参数不是self而是cls
    unpackers.append(cls)
    return cls


def fnmatch(pattern, filename):
    filename = os.path.basename(os.path.normcase(filename))
    pattern = os.path.normcase(pattern)
    bits = '(%s)' % re.escape(pattern).replace('\\*', ')(.*?)(')
    return re.match('^%s$', filename)


def which(name):
    path = os.environ.get('PATH')
    if path:
        for p in path.split(os.pathsep):  # os.pathsep在Linux中为’:‘，Windows中为':'
            p = os.path.join(p, name)  # os.path.join将p和name合并为一个路径
            if os.access(p, os.X_OK):  # X_OK能否执行
                return p


def increment_string(string):
    m = re.match('(.*?)(\d+)$', string)
    if m is None:
        return string + '-2'
    return m.group(1) + str(int(m.group(2)) + 1)


def get_mimetype(filename):
    file_executable = which("file")
    if file_executable is not None:
        rv = subprocess.Popen(['file','-b','--mime-type',filename],stdout=subprocess.PIPE,stderr=subprocess.PIPE)\
        .communicate()[0].strip()
        if rv:
            return rv
    return mimetypes.guess_type(filename)[0]


def line_parser(request_format):
    pass

class StreamProcessor:
    def __init__(self, request_format, stream):
        self.regex = re.compile(request_format)
        self.stream = stream

    def process(self, p):
        stream = getattr(p, self.stream)
        while True:
            line = stream.readline()
            if not line:
                break
            match = self.regex.search(line)
            if match is not None:
                yield match.group(1)

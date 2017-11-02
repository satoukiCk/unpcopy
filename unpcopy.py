import sys
import os
unpackers = []

def register_unpacker(cls): # cls对于classmethod，第一个参数不是self而是cls
    unpackers.append(cls)
    return cls

def which(name):
    path = os.environ.get('PATH')
    if path:
        for p in path.split(os.pathsep):# os.pathsep在Linux中为’:‘，Windows中为':'
            p = os.path.join(p,name)# os.path.join将p和name合并为一个路径
            if os.access(p,os.X_OK): # X_OK能否执行
                return p
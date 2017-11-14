__author__ = 'Liujuhao'
import os

dir_name = 'filename'

if os.path.isdir(dir_name):
    print 'this is a old project'
    rootdir = dir_name
    os.walk()
else:
    os.mkdir(r'/path/dir_name')
    print 'create a new project: %s' %(dir_name)
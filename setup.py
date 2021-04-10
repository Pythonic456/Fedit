from setuptools import setup
import os
import sys

if(len(sys.argv)>=1 and sys.argv[1] == 'install'):
    os.system('rm -r /usr/share/fedit && rm /usr/share/applications/fedit.desktop')
    os.system('mkdir /usr/share/fedit')
    setup(name='Fedit',
      version='0.0.1.6',
      description='A simple text editor in python with tkinter',
      author='Pythonic456',
      data_files=[
        ('/usr/share/applications', ['data/fedit.desktop']),
        ('/usr/share/fedit/',['main.py']),
        ('/usr/share/fedit/',['data/fedit.png']),
        ('/usr/share/fedit/',['tktools.py'])
        ]
    )
if(len(sys.argv)>=1 and sys.argv[1] == 'remove'):
    os.system('rm -r /usr/share/fedit && rm /usr/share/applications/fedit.desktop')

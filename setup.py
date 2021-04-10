from setuptools import setup
import os
import sys

if(len(sys.argv)>=1 and sys.argv[1] == 'install'):
    os.system('sudo rm -r /usr/share/fedit &&  sudo rm /usr/share/applications/fedit.desktop')
    os.system('sudo mkdir /usr/share/fedit')
    setup(name='Fedit',
      version='0.0.1.6',
      description='A simple text editor in python with tkinter',
      author='Pythonic456',
      data_files=[
        ('/usr/share/applications', ['fedit.desktop']),
        ('/usr/share/fedit/',['fedit.py']),
        ('/usr/share/fedit/',['fedit.png']),
        ('/usr/share/fedit/',['tktools.py'])
        ]
    )
if(len(sys.argv)>=1 and sys.argv[1] == 'remove'):
    os.system('sudo rm -r /usr/share/fedit &&  sudo rm /usr/share/applications/fedit.desktop')

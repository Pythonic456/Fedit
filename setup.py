from setuptools import setup
params = {}
params['scripts'] = ['bin/fedit']
setup(name='Fedit',
      version='0.0.1.5',
      description='A simple text editor in python with tkinter',
      author='Pythonic456',
      packages=['tktools'],
      data_files=[
        ('/usr/share/pixmaps', ['data/fedit.png']),
        ('/usr/share/applications', ['data/fedit.desktop'])
        ],
      **params
 )

import setuptools
setuptools.setup(name='atto',
                version='1.0.0',
                description='Simple curses text editor',
                long_description_content_type='text/markdown',
                long_description=
"""
## atto - Simple curses text editor

### Installation
```
pip install atto
```
### Usage
#### As script
```
[user@localhost ~] atto "<filename>"
```
#### In your code
```python
import atto 
atto.edit('filename.txt')
```
### Keys
i to switch to insert mode
ESC to return from insert mode
F4 to exit without saving
F2 to save
F10 to save and exit
Arrow keys to move cursor

### License
atto is licensed under **GPL License**
### Requirements
1. `cursor`: Cross-platform library for showing and hiding cursor
""",
                install_requires=['cursor'],
                packages=['atto'],
                classifiers=[
                    "Development Status :: 3 - Alpha",
                    "Environment :: Console :: Curses",
                    "Intended Audience :: End Users/Desktop",
                    "License :: OSI Approved :: GNU General Public License (GPL)",
                    "Operating System :: OS Independent",
                    "Programming Language :: Python :: 3",
                    "Topic :: Text Editors",
                    ],
                entry_points={
                    'console_scripts':['atto = atto:edit']
                    },
                author='Adam Jenca',
                author_email='jenca.adam@gmail.com',
                url='https://pypi.org/project/atto/',
                )



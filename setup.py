# -*- coding: utf-8 -*-

import os
import pypandoc
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
readmefile = os.path.join(here, 'README.md')
readme = pypandoc.convert(readmefile, 'rst', encoding='utf-8')
readme = readme.replace('\r', '')


setup(
    name='keyctl',
    version='0.3',
    description='Wrapper to use keyctl command in Python',
    long_description=readme,
    author='Martin Becker',
    author_email='tuxberlin@gmail.com',
    url='https://github.com/tuxberlin/python-keyctl',
    license='GPL-3.0',
    packages=['keyctl', 'keyctl.gui'],
    package_data={
        'keyctl.gui': ['addkey.ui', 'keylist.ui'],
    },
    install_requires=['PySide'],
    entry_points={
        'console_scripts': [
            'keyctlgui=keyctl.gui:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Environment :: X11 Applications :: Qt',
        'Topic :: Utilities',
    ]
)

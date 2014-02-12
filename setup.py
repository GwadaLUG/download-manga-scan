# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='download-manga-scan',
    version=__import__("download_manga_scan").__version__,
    description=u'client de téléchargement de scan de manga',
    long_description=open('README.txt').read(),
    author='Laurent Vergerolle - Gwadalug',
    author_email='lvergerolle@gmail.com',
    url='https://github.com/GwadaLUG/download-manga-scan',
    license=open('COPYING.txt').read(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python"
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points = {
        'console_scripts': [
            'download-manga = download_manga_scan:main',
        ],
    },
)

'''
Buildozer
'''

from setuptools import setup
from os.path import dirname, join
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))


def find_version(*file_paths):
    with codecs.open(os.path.join(here, *file_paths), 'r', 'utf-8') as f:
        version_file = f.read()

    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='kdpp',
    version=find_version('kdpp', '__init__.py'),
    description='Generic kivydev plugins platform',
    author='nkiiiiid',
    url='http://github.com/nkiiiiid/kdpp',
    license='MIT',
    packages=[
        'kdpp', 'kdpp.tools', 'kdpp.scripts'
        ],
    package_data={'kdpp': ['kdpp.nt','default.p4a']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'kdpp=kdpp.scripts.client:main'
        ]
    })

import re
from os.path import join, dirname

from setuptools import setup


PACKAGENAME = 'slda'

# reading package's version (same way sqlalchemy does)
with open(join(dirname(__file__), f'{PACKAGENAME}.py')) as f:
    version = re.match('.*__version__ = \'(.*?)\'', f.read(), re.S).group(1)


dependencies = [
    'yhttp',
    'redis',
    'hashids',
]


setup(
    name=PACKAGENAME,
    version=version,
    description='Url shortener web application',
    long_description=open('README.md').read(),
    install_requires=dependencies,
    py_modules=[PACKAGENAME],
    license='MIT',
)

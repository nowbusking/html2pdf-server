from __future__ import with_statement

import re
import urllib.parse

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


def readme():
    try:
        with open('README.rst') as f:
            content = f.read()
    except (IOError, OSError):
        pass
    base_url = 'https://github.com/spoqa/html2pdf-server/raw/master/'
    return re.sub(
        r'((?:^|\n)..\s+image::\s+)((?!https?://).+)(\n|$)',
        lambda m: (
            m.group(1) +
            urllib.parse.urljoin(base_url, m.group(2)) +
            m.group(3)
        ),
        content
    )


setup(
    name='html2pdf-server',
    version='1.2.0',
    description='HTTP server that renders HTML to PDF',
    long_description=readme(),
    url='https://github.com/spoqa/html2pdf-server',
    author='Spoqa',
    author_email='dev' '@' 'spoqa.com',
    maintainer='Spoqa',
    maintainer_email='dev' '@' 'spoqa.com',
    license='AGPLv3 or later',
    py_modules=['html2pdfd'],
    install_requires=[
        'aiohttp >= 1.0.5, < 1.1.0',
        'aiohttp-wsgi == 0.6.3',
        'Wand >= 0.4.2',
        'WeasyPrint >= 0.22',
        'Werkzeug >= 0.9'
    ],
    scripts=['html2pdfd.py'],
    entry_points='''
        [console_scripts]
        html2pdfd = html2pdfd:main
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved ::'
        ' GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Printing'
    ]
)

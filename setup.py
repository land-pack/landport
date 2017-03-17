"""
Landport
--------------

Python game server framework, you can easy build a virtual room by websocket!
you can talk to your member ~
"""
import re
from setuptools import setup

setup(
    name='Landport',
    version='1.1.8',
    url='https://github.com/land-pack/landport',
    license='MIT',
    author='Frank AK',
    author_email='landpack@sina.com',
    description='Game Server Framework',
    long_description=__doc__,
    packages=['landport', 'landport.core', 'landport.utils'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'tornado',
        'ujson',
        'gevent',
        'futures',
        'flask'
    ],
  
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

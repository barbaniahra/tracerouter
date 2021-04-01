import os
from setuptools import setup
from pathlib import Path

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
HOME_DIRECTORY = str(Path.home())


setup(name='tracerouter',
      version='1.0',
      description='Tracert wrapper for Windows.',
      author='Vladyslav Barbanyagra',
      author_email='mrcontego@gmail.com',
      install_requires=open(os.path.join(CURRENT_DIRECTORY, 'requirements.txt')).readlines(),
      entry_points={
            'console_scripts': ['tracerouter=main.tracerouter:main'],
      },
      packages=['main'],
      data_files=[(('tracerouter_resources'), ['resources/config.ini', 'resources/db.tcv.gz'])])

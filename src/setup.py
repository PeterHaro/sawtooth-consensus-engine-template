import subprocess

from setuptools import setup, find_packages

setup(name='sawtooth-custom-consensus',
      version="0.1",
      description='Sawtooth Custom Consensus Module',
      author='SINTEF',
      url='TBD',
      packages=find_packages(),
      install_requires=[
          'requests',
          'sawtooth-sdk',
      ],
      entry_points={})

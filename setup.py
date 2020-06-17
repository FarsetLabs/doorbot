"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['flask', 'flask_sslify', 'flask_httpauth']

setup(name='doorbot',
      version="1.0.1",
      description='Python Package Boilerplate',
      long_description=readme + '\n\n' + history,
      long_description_content_type='text/markdown',
      author='Andrew Bolster',
      author_email='bolster@farsetlabs.org.uk',
      url='https://github.com/FarsetLabs/doorbot',
      packages=find_packages(include=['doorbot', 'doorbot.*']),
      install_requires=requirements,
      license='MIT License',
      zip_safe=False,
      keywords='access control, hackerspace',
      classifiers=['Packages', 'Boilerplate'])

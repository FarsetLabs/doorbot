import setuptools
from packagename.version import Version


setuptools.setup(name='pytest-cov',
                 version=Version('1.0.0').number,
                 description='Python Package Boilerplate',
                 long_description=open('README.md').read().strip(),
                 author='Andrew Bolster',
                 author_email='me@andrewbolster.info',
                 url='https://github.com/FarsetLabs/doorbot',
                 py_modules=['doorbot'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 keywords='boilerplate package',
                 classifiers=['Packages', 'Boilerplate'])

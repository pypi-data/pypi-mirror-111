from distutils.core import Command
from setuptools import setup

from os.path import abspath, dirname, join


class NPMInstall(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.spawn(['npm', 'install'])
        self.spawn(['rm', '-rf', 'sa11y/scripts'])
        self.spawn(['mkdir', 'sa11y/scripts'])
        self.spawn(['cp', 'node_modules/axe-core/axe.min.js', 'sa11y/scripts/'])


setup(
    cmdclass={
        'npm_install': NPMInstall
    },
    name='sa11y',
    version='0.0.4',
    packages=['sa11y'],
    url='https://github.com/saucelabs/sa11y',
    download_url='https://github.com/saucelabs/sa11y/archive/v_004.tar.gz',
    license='MPL-2.0',
    author='titusfortner',
    author_email='titusfortner@gmail.com',
    keywords=['selenium', 'testing', 'accessibility', 'Deque', 'axe'],
    install_requires=[
        'selenium',
        'pytest'
    ],
    description='The Selenium Accessibility Project'
)

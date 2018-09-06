
from setuptools import setup

setup(
    name='skope.service',
    description='SKOPE services',
    version='0.1.0',
    author='Timothy McPhillips',
    author_email='tmcphillips@absoluteflow.org',
    url='https://github.com/tmcphillips/timeseries-service/python',
    license='MIT',
    packages=['skope.service'],
    package_dir={'': 'src'},
    data_files = [("", ["LICENSE.txt"])],
    install_requires=['skope==0.1.0', 'typing >= 3.6.6']
)
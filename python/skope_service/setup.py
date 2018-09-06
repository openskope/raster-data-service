
from setuptools import setup

setup(
    name='skope_service',
    description='SKOPE services',
    version='0.1.0',
    author='Timothy McPhillips',
    author_email='tmcphillips@absoluteflow.org',
    url='https://github.com/openskope/timeseries-service/tree/master/python/skope_service',
    license='MIT',
    packages=['skope_service'],
    package_dir={'': 'src'},
    data_files = [("", ["LICENSE.txt"])],
    install_requires=['skope==0.1.0', 'typing >= 3.6.6', 'Flask >= 1.0.2']
)
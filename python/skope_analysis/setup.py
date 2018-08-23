
from setuptools import setup

setup(
    name='skope_analysis',
    description='Analysis tools for SKOPE',
    version='0.1.0',
    author='Timothy McPhillips',
    author_email='tmcphillips@absoluteflow.org',
    url='https://github.com/tmcphillips/timeseries-service/python',
    license='MIT',
    packages=['skope_analysis'],
    package_dir={'': 'src'},
    data_files = [("", ["LICENSE.txt"])],
    install_requires=[
        'Flask >= 1.0.2'
    ]
)
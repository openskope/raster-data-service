
from setuptools import setup

setup(
    name='skope.analysis',
    description='SKOPE data analysis tools',
    version='0.1.0',
    author='Timothy McPhillips',
    author_email='tmcphillips@absoluteflow.org',
    url='https://github.com/tmcphillips/timeseries-service/python',
    license='MIT',
    packages=['skope.analysis'],
    package_dir={'': 'src'},
    data_files = [("", ["LICENSE.txt"])],
    install_requires=['affine >= 2.2.1', 'typing >= 3.6.6'],
    scripts=['scripts/series.py']
)
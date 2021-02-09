from setuptools import setup, find_packages

setup(
    name="skope_timeseries",
    version="1.1.0",
    description="""SKOPE timeseries-service python-gdal scripts.
                Adapted from:
                github.com:openskope/geoserver-loader/scripts/zonalinfo.py""",
    packages=find_packages(),
    install_requires=[
        'rasterio>=1.2.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    scripts=[
        'zonalinfo.py',
    ]
)

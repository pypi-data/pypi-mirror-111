"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='pyfinlab',  # Required
    version='0.0.1',  # Required
    description='Financial applications focusing on portfolio management for Python',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/nathanramoscfa/pyfinlab',  # Optional
    author='Nathan Ramos, CFA©',  # Optional
    author_email='nathan.ramos.cfa@gmail.com',  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Other classifiers
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='python, finance, portfolio-optimization, quantitative-finance, portfolio-management',  # Optional
    package_dir={'': 'src'},  # Optional
    packages=find_packages(where='src'),  # Required
    python_requires='>=3.6, <4',
    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data={  # Optional
        'sample': ['package_data.dat'],
    },
    data_files=[('my_data', ['data/data_file'])],  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'sample=sample:main',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/nathanramoscfa/pyfinlab/issues',
        'Ethereum Address': 'https://etherscan.io/address/0x5679291c949069A05E4d82A4dB24ba0200c91B20',
        'Source': 'https://github.com/nathanramoscfa/pyfinlab',
    },
)

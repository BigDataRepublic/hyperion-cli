import setuptools
from hyperion.__version__ import __version__

setuptools.setup(
    name='hyperion-cli',
    version=__version__,
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['hyperion=hyperion.cli:main']
    },
    install_requires=[
        'click==6.7'
    ],
    include_package_data=True
)

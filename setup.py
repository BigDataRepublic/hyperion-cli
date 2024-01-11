import setuptools
from hyperion.__version__ import __version__

setuptools.setup(
    name='hyperion-cli',
    version=__version__,
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['hyperion=hyperion.cli:main']
    },
    # Installs all files required
    # https://setuptools.readthedocs.io/en/latest/setuptools.html#including-data-files
    package_data={'hyperion': [
        'res/*'
    ]},
    install_requires=[
        'click==6.7',
        'colorama==0.3.9',
        'jinja2==3.1.3',
        'kubernetes>=6.0.0, <=10.0.1',
        'PyYAML>=5.4'
    ],
)

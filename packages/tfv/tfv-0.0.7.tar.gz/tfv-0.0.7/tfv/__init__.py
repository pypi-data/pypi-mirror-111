import pkg_resources

__version__ = "0.0.7"
__author__ = "toby.devlin@bmtglobal.com, jonah.chorley@bmtglobal.com"
__aus_date__ = "%d/%m/%Y %H:%M:%S"

# List of dependencies copied from requirements.txt
dependencies = \
    [
        'numpy>=1.19.0',
        'matplotlib>=3.2.2',
        'netCDF4>=1.5.3',
        'PyQt5>=5.15.0',
    ]

# Throw exception if correct dependencies are not met
pkg_resources.require(dependencies)

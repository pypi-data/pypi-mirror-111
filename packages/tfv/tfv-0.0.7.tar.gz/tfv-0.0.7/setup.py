import setuptools

with open("README.md", "r") as rm:
    long_description = rm.read()

setup = \
    {
        'name': "tfv",
        'version': '0.0.7',
        'description': "Post processing tools for TUFLOW FV results",
        'long_description': long_description,
        'long_description_content_type': "text/markdown",
        'url': "https://gitlab.com/TUFLOW/tfv",

        'author': "Toby Devlin & Jonah Chorley",
        'author_email': "support@tuflow.com",

        'packages': ['tfv'],

        'classifiers':
            [
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ],

        'python_requires': '>=3.6',
        'install_requires':
            [
                'numpy>=1.19.0',
                'matplotlib>=3.2.2',
                'netCDF4>=1.5.3',
                'PyQt5>=5.15.0',
            ]
    }

setuptools.setup(**setup)

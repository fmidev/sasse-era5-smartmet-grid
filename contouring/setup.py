from setuptools import setup, find_packages

setup(
    # Name for PyPi (never will we upload this)
    name="contouring",
    
    # Try to search for packages here
    packages=find_packages(where="src"),

    # "Just a normal distutils thing"
    # https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages
    # This defines the "root" or something like that
    package_dir={"": "src"},

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword.
    # Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # Provide a command called `contour_storm` which
    # executes the function `main` from this package when invoked:
    entry_points={
        'console_scripts': [
            'contour_storm = contouring.datareader:main',
        ],
    },

    install_requires = [
        "pytest >= 5.1",
        "aiohttp >= 3.5",
        "owslib >= 0.18"
    ]

)
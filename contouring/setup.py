from setuptools import setup, find_packages

setup(
    name="contouring",
    packages=find_packages("src"),
    package_dir={"": "src"},
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
            'sample = contouring.datareader:main',
        ],
    },
)
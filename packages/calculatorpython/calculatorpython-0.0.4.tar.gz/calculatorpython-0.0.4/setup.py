from setuptools import setup, find_packages
VERSION = '0.0.4'
DESCRIPTION = 'Basic calculator'
LONG_DESCRIPTION = 'Basic operations of mathematics.'

# Setting up
setup(
    name="calculatorpython",
    version=VERSION,
    author="Advait Shiralkar",
    author_email="advaitshiralkar2@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['Calculator', 'vidstream', 'os', 'say-hi'],
    keywords=[''],
    License='MIT',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

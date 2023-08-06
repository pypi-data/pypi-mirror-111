from setuptools import setup

VERSION = '0.0.5'
DESCRIPTION = 'This module will return whether PDF is Digital, Non-Digital or Mixed.'

# Setting up
setup(
    name="pdf_segregation",
    version=VERSION,
    author="Kishan Tongrao",
    author_email="kishan.tongs@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=['pdf_segregation'],
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)